import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import seaborn as sns
from .data_clean import clean_data

# 暂时废弃
# "选择模式分析": "评估玩家在特定扰动模式和异类比例下的选择模式，包括他们如何应对不同的视觉扰动和'异类'频率。"
# def choice_pattern_analysis(filename, selected_distort_mode):
#   # 加载数据
#   df = clean_data(filename)

#   # 处理数据，提取和处理选择时间数据
#   df['selection_time'] = df.iloc[:, 9:].min(axis=1)  # 提取每个格子的最早选择时间
#   df['selection_time'] = df['selection_time'].fillna(0)  # 没有选择的格子填充为0

#   # 筛选特定扰动模式的数据
#   selected_data = df[df['distortMode'] == selected_distort_mode]

#   # 绘制散点图来展示玩家的选择情况
#   plt.figure(figsize=(10, 8))
#   sns.scatterplot(data=selected_data, x='i', y='j', hue='alien', style='correct_choice', size='selection_time', sizes=(20, 200))
#   plt.title(f'Player Choices with {selected_distort_mode} Distortion (All Trials)')
#   plt.xlabel('Position X')
#   plt.ylabel('Position Y')
#   plt.legend(title='Alien / Correct Choice', bbox_to_anchor=(1.05, 1), loc='upper left')
#   plt.grid(True)
#   plt.savefig(f'temp.png', bbox_inches='tight')



def alien_ratio_and_correctness_per_trial(filename):
    # 加载和清洁数据
    df = clean_data(filename)

    # 计算每个关卡的异类比例
    alien_ratio_per_trial = df.groupby('trial')['alien'].apply(lambda x: x.value_counts(normalize=True).get(1, 0) * 100)

    # 计算每个关卡的平均正确率
    correctness_per_trial = df.groupby('trial')['correct_choice'].apply(lambda x: x.mean() * 100)

    # 创建图表
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 设置x轴为关卡（trial）
    ax1.set_xlabel('Trial')

    # 第一个y轴（左边）为异类比例
    color = 'tab:blue'
    ax1.set_ylabel('Alien Ratio (%)', color=color)
    ax1.plot(alien_ratio_per_trial.index, alien_ratio_per_trial, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # 第二个y轴（右边）为正确率
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Correct Choice Rate (%)', color=color)
    ax2.plot(correctness_per_trial.index, correctness_per_trial, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Alien Ratio and Correct Choice Rate per Trial')
    plt.savefig('temp.png', bbox_inches='tight')


if __name__ == '__main__':
    # choice_pattern_analysis('test-set5.csv')
    alien_ratio_and_correctness_per_trial('test-set5.csv')

