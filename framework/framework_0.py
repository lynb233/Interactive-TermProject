from .data_clean import clean_data
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# 主要显示当前选择的文件中，存在多少局，总计多少个条数据，以及正确选择数和错误选择数的数目

def show_data_info(filename):
    df = clean_data(filename)

    # 将数据储存到一个字典中，并且作为返回值以供后续使用
    data_info = {'total_trial': df['trial'].max(), 'total_data': df.shape[0]-1,
                 'wrong_choice': df[df['correct_choice'] == 0].shape[0],
                 'correct_rate': df[df['correct_choice'] == 1].shape[0] / df.shape[0]}
    
    return data_info




if __name__ == '__main__':
    # 路径：C:\Projects\interactive\Term Project\framework\test-set4.csv
    show_data_info('C:\\Projects\\interactive\\Term Project\\framework\\test-set4.csv')
