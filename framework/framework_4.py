import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#from .data_clean import clean_data

def clean_data_with_total_time(file_path):

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
  #cleaned_data = cleaned_data[cleaned_data.apply(is_valid, axis=1)]

  return cleaned_data


def average_selection_time_and_correctness_per_trial(filename):
    # Load the CSV file
    data = clean_data_with_total_time(filename)

# 提取每个trial的结束时间
    end_time_per_trial = data[data['distortMode'] == 'undefined'].set_index('trial')['0']

    # 计算每个trial的实际持续时间
    total_time_per_trial = end_time_per_trial.diff().fillna(end_time_per_trial)

    # 计算每个trial的平均正确率
    level_performance = data.groupby('trial').agg({'correct_choice': lambda x: x.mean() * 100})

    # Plotting the total time and correctness per trial
    fig, ax1 = plt.subplots(figsize=(12, 6))
    color = 'tab:blue'
    ax1.set_xlabel('Trial')
    ax1.set_ylabel('Total Time per Trial (ms)', color=color)
    ax1.plot(total_time_per_trial.index, total_time_per_trial, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('Correctness Ratio', color=color)  
    ax2.plot(level_performance.index, level_performance['correct_choice'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title('Total Time and Correctness Ratio per Trial')
    plt.savefig('temp.png', bbox_inches='tight')


# def average_selection_time_and_correctness_per_trial(filename):

#   # Load the CSV file
#   data=clean_data(filename)

#   # Transform the DataFrame to get the time columns in a long format
#   time_columns = [str(i) for i in range(0, len(data.columns) - 12)]
#   melted_data = pd.melt(data, id_vars=['trial', 'AlienRatio', 'distortMode', 'i', 'j', 'charID', 'scale', 'rotate', 'alien', 'correct_choice'], 
#                         value_vars=time_columns, var_name='selection_round', value_name='selection_time')

#   # Remove rows where selection_time is NaN and convert selection_round to numeric
#   melted_data = melted_data.dropna(subset=['selection_time'])
#   melted_data['selection_round'] = pd.to_numeric(melted_data['selection_round'])

#   # Convert selection_time from milliseconds to seconds
#   melted_data['selection_time_sec'] = melted_data['selection_time'] / 1000

#   # Analyzing average selection time and correctness for each trial
#   performance_by_trial = melted_data.groupby('trial').agg({'selection_time_sec': 'mean'}).reset_index()

#   # 首先，我们需要提取和处理选择时间数据
#   data['selection_time'] = data.iloc[:, 9:].min(axis=1)  # 提取每个格子的最早选择时间
#   data['selection_time'] = data['selection_time'].fillna(0)  # 没有选择的格子填充为0

#   # 计算每个关卡的平均正确率
#   level_performance = data.groupby('trial').agg({'correct_choice': lambda x: x.mean() * 100})

#   # Plotting the average selection time and correctness per trial
#   fig, ax1 = plt.subplots(figsize=(12, 6))
#   color = 'tab:blue'
#   ax1.set_xlabel('Trial')
#   ax1.set_ylabel('Average Selection Time (sec)', color=color)
#   ax1.plot(performance_by_trial['trial'], performance_by_trial['selection_time_sec'], color=color)
#   ax1.tick_params(axis='y', labelcolor=color)
#   ax2 = ax1.twinx()  
#   color = 'tab:red'
#   ax2.set_ylabel('Correctness Ratio', color=color)  
#   ax2.plot(level_performance.index, level_performance['correct_choice'], color=color) # 修改此行
#   ax2.tick_params(axis='y', labelcolor=color)
#   plt.title('Average Selection Time and Correctness Ratio per Trial')
#   plt.savefig('temp.png', bbox_inches='tight')

if __name__ == "__main__":
  average_selection_time_and_correctness_per_trial('C:\\Projects\\interactive\\Term Project\\framework\\test-set5.csv')

