
# 本脚本用于清洗数据。清洗后的结果见末尾注释

import pandas as pd

def clean_data(file_path):

  data = pd.read_csv(file_path)

  # 仅检查每行的第2至第9列是否有未定义（NaN）值
  columns_to_check = data.columns[1:9]
  cleaned_data = data.dropna(subset=columns_to_check, axis=0, how='any')

  # 去除Dimension列
  cleaned_data = cleaned_data.drop(['Dimension'], axis=1)

  # 去除在列2和列3中包含undefined值的行
  def is_valid(row):
    return row['distortMode'] != 'undefined' and row['i'] != 'undefined'

  # 确定玩家选择是否正确
  def is_correct_choice(row):
    # 检查这个格子是否是异类
    is_alien = row['alien'] == '1'
    # 时间列以从0开始的整数命名
    time_columns = [str(i) for i in range(len(row) - 9)]  # 9 non-time columns
    has_selection = False
    for i in range(0, len(time_columns), 2):
      # 如果偶数列有数据且其后面的奇数列（如果存在）没有数据，则认为玩家选择了该字符
      if pd.notna(row[time_columns[i]]) and (i+1 >= len(time_columns) or pd.isna(row[time_columns[i+1]])):
        has_selection = True
        break
      
    # 根据是否为异类和玩家的选择来决定是否正确
    return (is_alien and has_selection) or (not is_alien and not has_selection)

  # 对每一行应用上述两个函数
  cleaned_data['correct_choice'] = cleaned_data.apply(is_correct_choice, axis=1)
  cleaned_data = cleaned_data[cleaned_data.apply(is_valid, axis=1)]

  return cleaned_data

if __name__ == '__main__':
  cleaned_data = clean_data('C:/Projects/interactive/Term Project/framework\\/test-set25.csv')
  # 将结果保存到文件
  cleaned_data.to_csv('cleaned_data_test.csv', index=False)



# 清洗后的数据包含以下列：

# trial：关卡计数。
# AlienRatio：异类比例。
# distortMode：扰动模式。
# i，j：字符位置。
# charID：字符ID。
# scale：缩放尺度。
# rotate：倾斜角。
# alien：异类标记。
# 0, 1, 2, ... 等列：表达被点选的时刻。
# correct_choice：这是新添加的列，表示玩家的选择是否正确。
