# my_package/__init__.py

from .framework_0 import show_data_info
from .framework_1 import average_time_with_accuracy_by_specific_mode
from .framework_2 import alien_ratio_and_correctness_per_trial
from .framework_3 import total_heatmap, heatmap_per_mode, error_pattern, click_incorrect_heatmap
from .framework_4 import average_selection_time_and_correctness_per_trial

# 你可以选择性地在这里导出特定的函数或所有函数
__all__ = ['click_incorrect_heatmap', 'show_data_info', 'average_time_with_accuracy_by_specific_mode', 'alien_ratio_and_correctness_per_trial', 'total_heatmap', 'heatmap_per_mode', 'error_pattern', 'average_selection_time_and_correctness_per_trial']
