import pandas as pd
from .data_clean import clean_data
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def total_heatmap(filename):
  # Load the provided CSV data
  data = clean_data(filename)

  # Create a new column to indicate whether the cell was chosen or not
  # data['chosen'] = data.iloc[:, 9:13].notnull().any(axis=1)

  # Create a heatmap to show the frequency of incorrect choices at different positions

  # Filtering data for incorrect choices
  incorrect_choices = data[data['correct_choice'] == False]

  # Create a pivot table for the heatmap of incorrect choices
  incorrect_heatmap_data = incorrect_choices.pivot_table(index='i', columns='j', values='correct_choice', aggfunc='count').fillna(0)

  # Plotting the heatmap of incorrect choices
  plt.figure(figsize=(10, 8))
  sns.heatmap(incorrect_heatmap_data, annot=True, fmt=".0f", cmap="Reds")
  plt.title("Frequency of Incorrect Choices at Different Positions")
  plt.xlabel("Column Position (j)")
  plt.ylabel("Row Position (i)")
  plt.savefig('temp.png', bbox_inches='tight')

# Create separate heatmaps for each distortion mode showing the frequency of incorrect choices

def heatmap_per_mode(filename, distortion_mode):
    data = clean_data(filename)
    # data['chosen'] = data.iloc[:, 9:13].notnull().any(axis=1)

    # 选择不正确的选择
    incorrect_choices = data[data['correct_choice'] == False]

    # 筛选出特定扰动模式的不正确选择
    mode_data = incorrect_choices[incorrect_choices['distortMode'] == distortion_mode]
    
    # 为热图创建数据透视表
    mode_heatmap_data = mode_data.pivot_table(index='i', columns='j', values='correct_choice', aggfunc='count').fillna(0)

    # 绘制指定扰动模式的热图
    plt.figure(figsize=(12, 6))
    sns.heatmap(mode_heatmap_data, annot=True, fmt=".0f", cmap="Reds")
    plt.title(f"Frequency of Incorrect Choices - {distortion_mode} Mode (All Trials)")
    plt.xlabel("Column Position (j)")
    plt.ylabel("Row Position (i)")

    plt.tight_layout()
    plt.savefig(f'temp.png', bbox_inches='tight')


def click_incorrect_heatmap(filename):
  # Load the provided CSV data
  data = clean_data(filename)

  # Create a new column to indicate whether the cell was chosen or not
  data['chosen'] = data.iloc[:, 9:13].notnull().any(axis=1)

  # Create a heatmap to show the frequency of incorrect choices at different positions

  # Filtering data for incorrect choices
  incorrect_choices = data[data['correct_choice'] == False]

  # Create a pivot table for the heatmap of incorrect choices
  incorrect_heatmap_data = incorrect_choices.pivot_table(index='i', columns='j', values='chosen', aggfunc='sum').fillna(0)

  # Plotting the heatmap of incorrect choices
  plt.figure(figsize=(10, 8))
  sns.heatmap(incorrect_heatmap_data, annot=True, fmt=".0f", cmap="Reds")
  plt.title("Frequency of Incorrect Choices at Different Positions")
  plt.xlabel("Column Position (j)")
  plt.ylabel("Row Position (i)")
  plt.savefig('temp.png', bbox_inches='tight')



def error_pattern(filename):
    data = clean_data(filename)

    # Analyze the error patterns based on distortion mode and choice correctness
    error_analysis_data = data.groupby(['distortMode', 'correct_choice']).size().reset_index(name='counts')

    # Create a bar plot for the error analysis data
    pivot_data = error_analysis_data.pivot(index='distortMode', columns='correct_choice', values='counts')
    pivot_data.plot(kind='bar', stacked=False)
    plt.title('Error Pattern Analysis')
    plt.xlabel('Distortion Mode')
    plt.ylabel('Counts')
    plt.savefig('temp.png', bbox_inches='tight')

  # data['chosen'] = data.iloc[:, 9:13].notnull().any(axis=1)

  # # Analyzing the multi-choice errors (choosing non-alien characters) and missed errors (failing to identify aliens)

  # # Filtering data for errors
  # multi_choice_errors = data[(data['alien'] == 0) & (data['chosen'] == True) & (data['correct_choice'] == False)]
  # missed_errors = data[(data['alien'] == 1) & (data['chosen'] == False)]

  # # Counting the errors
  # multi_choice_error_count = multi_choice_errors.groupby('distortMode').size().reset_index(name='multi_choice_errors')
  # missed_error_count = missed_errors.groupby('distortMode').size().reset_index(name='missed_errors')

  # # Combining both counts for a comprehensive error analysis
  # error_counts = pd.merge(multi_choice_error_count, missed_error_count, on='distortMode', how='outer').fillna(0)

  # # Display the combined error counts
  # print(error_counts)


if __name__ == '__main__':
  total_heatmap('test-set5.csv')
  heatmap_per_mode('test-set5.csv', 'Rotate')
  error_pattern('test-set5.csv')



