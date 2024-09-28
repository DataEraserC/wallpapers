import os
import re
import sys

def get_end_spaces(string):
    return string.rstrip(string.rstrip(' '))

def potential_names_without_number_end(filename):
    base_name, ext = os.path.splitext(filename)
    
    # 匹配末尾的"(数字)"或"_数字"以及捕获末尾的空格
    patterns = [
        r'\(\s*\d+\s*\)',  # 匹配"(数字)"在末尾
        r'_\d+$',            # 匹配"_数字"在末尾
        r' copy\s*\d*$',
    ]

    potential_names = set()

    can_strip = False
    # 检查模式并创建潜在文件名
    for pattern in patterns:
        stripped_name = re.sub(pattern, '', base_name)
        if stripped_name and base_name != stripped_name:
            potential_names.add(stripped_name + ext)  # 添加去除数字后的文件名
            potential_names.add(stripped_name.rstrip() + ext)  # 添加去除数字后的文件名
            can_strip = True

    if not can_strip:
        potential_names.add(base_name + ext)  # 添加原始文件名

    return list(potential_names)
def test_potential_names_without_number_end():
    test_cases = [
        ("file(1).txt", ["file.txt"]),
        (" file(1).txt", [" file.txt"]),
        ("file(1)", ["file"]),
        (" file (1).txt", [" file.txt", " file .txt"]),
        (" file (1 ).txt", [" file.txt", " file .txt"]),
        (" file ( 1 ).txt", [" file.txt", " file .txt"]),
        (" file ( 1).txt", [" file.txt", " file .txt"]),
        ("file (1).txt", ["file.txt", "file .txt"]),
        ("file (1)", ["file", "file "]),
        ("file_1.txt", ["file.txt"]),
        ("file_1", ["file"]),
        ("file.txt", ["file.txt"]),
        ("file1", ["file1"]),
        ("  1(  1     ) .1", ["  1 .1", "  1.1"]),
        ("1 copy.py", ["1.py"]),
        ("1 copy 2.py", ["1.py"]),
    ]

    for filename, expected in test_cases:
        actual = potential_names_without_number_end(filename)
        is_equal = sorted(actual) == sorted(expected)
        print(f"Filename: '{filename}'")
        print(f"Expected: '{expected}', Actual: '{actual}', Consistent: '{is_equal}'\n")



def file_content_equals(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

def delete_dup_files(folder_path):
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        if os.path.isfile(full_path):
            # Get potential stripped filenames
            stripped_names = [item for item in potential_names_without_number_end(filename) if item != filename]

            for stripped_name in stripped_names:
                stripped_path = os.path.join(folder_path, stripped_name)

                if not os.path.exists(stripped_path):
                    print(f"带编号的文件 '{filename}' 去除编号之后的文件 '{stripped_name}' 不存在")
                else:
                    if full_path == stripped_path:
                        print(f"带编号的文件 '{filename}' 与没带编号的 '{stripped_name}' 文件路径一致，无需删除")
                    else:
                        if file_content_equals(full_path, stripped_path):
                            print(f"带编号的文件 '{filename}' 与没带编号的 '{stripped_name}' 文件内容一致，进行删除")
                            os.remove(full_path)
                        else:
                            print(f"文件对比不一致，保留文件 {filename}")

if __name__ == "__main__":
    # test_potential_names_without_number_end()
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        # 从输入流接收目录路径
        folder_path = input("请输入目录路径: ")


    # 将相对路径转换为绝对路径
    folder_path = os.path.abspath(folder_path)
    delete_dup_files(folder_path)
