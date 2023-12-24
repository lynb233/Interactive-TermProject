import pandas as pd
import os
import re

# 定义原始CSV文件所在的目录
directory = 'dataset'

# 定义目标列名
required_columns = ['trial', 'AlienRatio', 'Dimension', 'distortMode', 'i', 'j', 'charID', 'scale', 'rotate', 'alien', '0', '1', '2']

# 定义将文件保存的新目录
new_directory = 'filtered_dataset'

# 确保新目录存在
os.makedirs(new_directory, exist_ok=True)

# 遍历目录中的所有文件
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)

            # 检查是否包含所有需要的列
            if all(column in df.columns for column in required_columns):
                # 重命名文件 - 在这里添加你的重命名逻辑
                new_file_path = os.path.join(new_directory, filename)

                # 保存到新目录
                df.to_csv(new_file_path, index=False)
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

print("筛选完成。")


# 遍历目录中的所有文件
for filename in os.listdir(new_directory):
    # 检查文件名是否符合“找异类-汉英字符x.csv”的格式
    match = re.match(r'找异类-汉英字符(\d+)\.csv', filename)
    if match:
        # 提取序号
        serial_number = match.group(1)
        # 构造新的文件名
        new_filename = f'dataset_{serial_number}.csv'
        # 重命名文件
        os.rename(os.path.join(new_directory, filename), os.path.join(new_directory, new_filename))

print("重命名完成。")




