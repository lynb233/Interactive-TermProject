from matplotlib import pyplot as plt
import seaborn as sns
from .data_clean import clean_data
import pandas as pd

# "准确率与平均时间": "测量玩家在不同关卡下，识别'异类'的平均时间和准确率。用于评估难度增加时，玩家的表现变化。",
# 暂时废弃
# def average_time_with_accuracy(file_name):
#   df=clean_data(file_name)
#   # 处理数据，计算每个关卡的平均完成时间、平均正确率
#   # 首先，我们需要提取和处理选择时间数据
#   df['selection_time'] = df.iloc[:, 9:].min(axis=1)  # 提取每个格子的最早选择时间
#   df['selection_time'] = df['selection_time'].fillna(0)  # 没有选择的格子填充为0

#   # 计算每个关卡的平均选择时间和平均正确率
#   level_performance = df.groupby('trial').agg({'selection_time': 'mean', 'correct_choice': lambda x: x.mean() * 100})

#   # 绘制每个关卡的平均完成时间和正确率的图表
#   plt.figure(figsize=(15, 6))
#   plt.subplot(1, 2, 1)
#   sns.barplot(x=level_performance.index, y='selection_time', data=level_performance, color='blue')
#   plt.title('Average Selection Time per Level')
#   plt.xlabel('Level')
#   plt.ylabel('Average Time (ms)')

#   plt.subplot(1, 2, 2)
#   sns.lineplot(x=level_performance.index, y='correct_choice', data=level_performance, marker='o', color='red')
#   plt.title('Average Correct Choice Rate per Level')
#   plt.xlabel('Level')
#   plt.ylabel('Correct Choice Rate (%)')

#   plt.tight_layout()
#   plt.savefig('temp.png', bbox_inches='tight')


def average_time_with_accuracy_by_specific_mode(file_name, specific_mode):
    df = clean_data(file_name)

    # 筛选出特定扰动模式的数据
    df = df[df['distortMode'] == specific_mode]

    # 对于 distortMode 为 undefined 的情况，将 '0' 列作为选择时间
    df.loc[df['distortMode'] == 'undefined', 'selection_time'] = df['0']


    # 将 DataFrame 转换为长格式以获取时间列
    time_columns = [str(i) for i in range(0, len(df.columns) - 12)]
    melted_data = pd.melt(df, id_vars=['trial', 'AlienRatio', 'distortMode', 'i', 'j', 'charID', 'scale', 'rotate', 'alien', 'correct_choice'], 
                          value_vars=time_columns, var_name='selection_round', value_name='selection_time')

    # 去除 selection_time 为 NaN 的行，并将 selection_round 转换为数值型
    melted_data = melted_data.dropna(subset=['selection_time'])
    melted_data['selection_round'] = pd.to_numeric(melted_data['selection_round'])

    # 将 selection_time 从毫秒转换为秒
    melted_data['selection_time_sec'] = melted_data['selection_time'] / 1000

    # 按 AlienRatio 分组，分析平均选择时间和正确率
    alien_difficulty_analysis = melted_data.groupby('AlienRatio').agg({'selection_time_sec': 'mean', 'correct_choice': 'mean'}).reset_index()
    alien_difficulty_analysis['correct_choice'] *= 100  # 转换为百分比

    # 创建双y轴图表
    fig, ax1 = plt.subplots(figsize=(15, 6))

    # 第一个y轴（左边）为平均选择时间
    color = 'tab:blue'
    ax1.set_xlabel('Alien Ratio')
    ax1.set_ylabel('Average Selection Time (sec)', color=color)
    sns.lineplot(data=alien_difficulty_analysis, x='AlienRatio', y='selection_time_sec', marker='o', ax=ax1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # 第二个y轴（右边）为正确选择率
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Correct Choice Rate (%)', color=color)
    sns.lineplot(data=alien_difficulty_analysis, x='AlienRatio', y='correct_choice', marker='o', ax=ax2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Average Selection Time and Correct Choice Rate by Alien Ratio ({specific_mode} Mode)')
    plt.tight_layout()
    plt.savefig(f'temp.png', bbox_inches='tight')






if __name__ == '__main__':
  # average_time_with_accuracy('test-set5.csv')
  average_time_with_accuracy_by_specific_mode('test-set5.csv')



