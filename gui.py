import tkinter as tk
import threading
from PIL import Image, ImageTk
import os
import json
import random


from framework import *


# 主GUI类
class AnalysisApp:
    def __init__(self, root):
        self.root = root
        root.title("互动媒体技术-实验分析结果可视化工具")
        root.iconbitmap('favicon.ico')
        root.geometry("1000x700")

        self.meme_list = ["buddhist_monk.jpg", "eat_with_cow.jpg", "lost_memory.jpg", "money.jpg", "xizhilang.jpg", "pipan.jpg"]

        # 临时图像文件路径
        self.temp_image_path = "./temp.png"

        # 用于存储图像的变量
        self.original_image = None

        # 设置frame
        self.options_frame = tk.Frame(root, width=230, relief="flat", bg="#DDDDDD")
        self.options_frame.pack_propagate(False)  # 防止自动调整大小
        self.image_frame = tk.Frame(root, bg="#EEEEEE")
        self.file_and_mode_frame = tk.Frame(root, bg="#DDDDDD")
        self.info_submit_frame = tk.Frame(root, bg="#DDDDDD")

        # 使用网格布局
        self.options_frame.grid(row=0, column=0, rowspan=4, sticky="ns", padx=5, pady=5)
        self.image_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.file_and_mode_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.info_submit_frame.grid(row=2, column=1, sticky="ew", padx=5, pady=5)


        # 设置网格布局的权重
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=3)


        # ------- 选项相关代码（左侧三分之一部分） -------
        # 加载选项和解释
        with open('./options_descriptions.json', 'r', encoding='utf-8') as file:
            self.options_descriptions = json.load(file)
        self.analysis_options = list(self.options_descriptions.keys())
        self.selected_analysis = tk.StringVar(value=self.analysis_options[0])

        # 初始化子选项
        self.sub_selection = "None"

        # 获取最长选项的字符长度
        index_of_longest_option = max(enumerate(self.analysis_options), key=lambda x: len(x[1]))[0]
        max_length = tk.Button(root, text=self.analysis_options[index_of_longest_option]).winfo_reqwidth()

        # 创建一个标签用于显示当前选择
        self.current_selection_label = tk.Label(self.options_frame, text="当前选择: " + self.selected_analysis.get(), width=max_length, bg="#DDDDDD")
        self.current_selection_label.pack(pady=10)

        # 创建按钮并添加到options_frame中
        for option in self.analysis_options:
            button = tk.Button(self.options_frame, text=option, width=max_length,
                            command=lambda option=option: self.update_selection(option))
            button.pack(pady=5)  # 按钮之间垂直间距为5

        # 创建一个标签用于显示当前选择的解释
        self.description_label = tk.Label(self.options_frame, text="", width=max_length, wraplength=200, bg="#DDDDDD")
        self.description_label.pack(pady=10)

        # 初始更新选项和解释
        self.update_selection(self.analysis_options[0])

        # 展示meme
        self.display_meme()


        # ------- 文件相关代码（右侧剩余部分） -------
        # ------- 图片显示区域（image_frame） -------
        self.image_label = tk.Label(self.image_frame, bg="#DDDDDD")
        self.image_label.pack(fill=tk.BOTH, expand=True)


        # ------ 文件选择，模式选择和子选项部分（file_and_mode_frame） ------
        # 添加所有的文件选项 
        directory = "./filtered_dataset"
        self.file_options = []

        # 列出文件夹中的所有文件
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                self.file_options.append(filename)

        # 创建一个标签用于提示用户选择文件
        self.file_label = tk.Label(self.file_and_mode_frame, text="选择文件: ", bg="#DDDDDD")
        self.file_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.selected_file = tk.StringVar(value=self.file_options[0])
        self.file_menu = tk.OptionMenu(self.file_and_mode_frame, self.selected_file, *self.file_options)
        self.file_menu.pack(side=tk.LEFT, padx=10)

        # 欢迎标签
        self.welcome_label = tk.Label(self.file_and_mode_frame, text="欢迎使用实验分析结果可视化工具", bg="#DDDDDD")
        self.welcome_label.pack(pady=10)

        # 展示选择的Label
        self.show_choice_label=tk.Label(self.file_and_mode_frame, text="当前选择: "+self.sub_selection, bg="#DDDDDD")
        self.show_choice_label.pack(side=tk.RIGHT, padx=5, pady=5)
        self.show_choice_label.pack_forget()

        # 存储按钮的字典
        self.option_buttons = {}

        # 创建四个按钮
        for option in ["Rotate", "Composite", "Scale", "None"]:
            # 为每个选项创建一个按钮
            button = tk.Button(self.file_and_mode_frame, text=option, command=lambda option=option: self.update_sub_selection(option))
            button.pack(side=tk.LEFT, padx=5, pady=5)
            button.pack_forget()  # 立即隐藏按钮
            # 将按钮存储在字典中
            self.option_buttons[option] = button

        # ------- 更新图表和显示文件详情按钮（info_submit_frame） -------
        self.file_info_dict = {}
        self.file_info = tk.Label(self.info_submit_frame, text="请点击右侧“显示文件详情”来查看选中文件的信息", bg="#DDDDDD")
        self.file_info.pack(side="left", padx=5, pady=10)

        self.update_button = tk.Button(self.info_submit_frame, text="更新图表", command=self.draw_plot)
        self.update_button.pack(side="right", padx=5, pady=10)

        self.cal_file_info = tk.Button(self.info_submit_frame, text="显示文件详情", command=self.show_file_info)
        self.cal_file_info.pack(side="right", padx=5, pady=10)




        # ------- 进度标签 -------
        self.progress_label = tk.Label(root, text="")
        self.progress_label.grid(row=4, column=1, pady=10)

        # ------- 事件绑定 -------
        # 绑定窗口尺寸变化事件
        root.bind('<Configure>', self.resize_frames)
        root.bind('<Configure>', self.resize_show_image)
        root.bind('<Configure>', self.schedule_resize_image)
        self.resize_pending = False

        # 绑定窗口关闭事件
        root.protocol("WM_DELETE_WINDOW", self.on_close)


    def show_file_info(self):
        def update_info():
            # 执行耗时的数据处理函数
            file_info_dict = show_data_info("./filtered_dataset/"+self.selected_file.get())

            # 使用 'after' 方法来安全地在主线程更新 GUI
            self.file_info.after(0, lambda: self.file_info.config(text="总局数:" + str(file_info_dict['total_trial']) + 
                                                                "  总数据条数：" + str(file_info_dict['total_data']) + 
                                                                "  错误选择数：" + str(file_info_dict['wrong_choice']) + 
                                                                "  正确率：" + "{:.2f}".format(file_info_dict['correct_rate'])))

        # 在开始耗时的数据处理之前更新文本为“请等待”
        self.file_info.config(text="正在分析选定的文件，请等待...")

        # 创建并启动一个新线程来执行update_info函数
        thread = threading.Thread(target=update_info)
        thread.start()



    # 显示memes
    def display_meme(self):
        meme_path = './memes/'+random.choice(self.meme_list) #self.meme_list[2]#
        max_length = 220

        if os.path.exists(meme_path):
            memeImg = Image.open(meme_path)
            resized_meme = memeImg.resize((max_length, int(memeImg.size[1]  / memeImg.size[0] * max_length)), Image.Resampling.LANCZOS)
            tk_meme = ImageTk.PhotoImage(resized_meme)
            meme_label = tk.Label(self.options_frame, image=tk_meme)
            meme_label.image = tk_meme  # 防止垃圾回收
            meme_label.pack(side=tk.BOTTOM, pady=10)
        else:
            error_label = tk.Label(self.options_frame, text="图像文件不存在")
            error_label.pack(side=tk.BOTTOM, pady=10)

    # 展示选择模式分析按钮
    def show_extra_options(self):
        self.welcome_label.pack_forget()
        for button in self.option_buttons.values():
            button.pack(side=tk.LEFT, padx=5, pady=5)

        self.show_choice_label.pack(side=tk.RIGHT, padx=5, pady=5)


    # 清除所有extra_options_frame中的按钮
    def hide_extra_options(self):
        for button in self.option_buttons.values():
            button.pack_forget()
        self.show_choice_label.pack_forget()
        self.welcome_label.pack(pady=10)


    # 更新子选项
    def update_sub_selection(self, new_sub_selection):
        self.sub_selection = new_sub_selection
        self.show_choice_label.config(text="当前选择: "+self.sub_selection)
    



    # 更新选择的函数
    def update_selection(self, new_selection):
        # 如果存在self.sub_selection_explanation的话：
        try:
            self.hide_extra_options()
        except:
            pass

        self.selected_analysis.set(new_selection)
        self.current_selection_label.config(text="当前选择: " + new_selection)
        self.description_label.config(text=self.options_descriptions[new_selection])
        if(new_selection == "选择模式分析" or new_selection == "异类错误热图" or new_selection == "正确率 / 每个异类比例"):
            self.show_extra_options()


    # 加载图像
    def load_image(self):
        if os.path.exists(self.temp_image_path):
            self.original_image = Image.open(self.temp_image_path)
        else:
            self.progress_label.config(text="图像文件不存在")

    # 延时调整图像
    def schedule_resize_image(self, event=None):
        if not self.resize_pending:
            self.root.after(500, self.resize_show_image)
            self.resize_pending = True

    # 调整图像大小
    def resize_show_image(self, event=None):
        if self.original_image is not None:
            # 获取图像标签的尺寸
            label_width, label_height = self.image_label.winfo_width(), self.image_label.winfo_height()

            # 获取原始图像尺寸
            original_width, original_height = self.original_image.size

            # 计算横向和纵向的缩放比例
            scale_width = label_width / original_width
            scale_height = label_height / original_height

            # 选择较小的比例以保持纵横比
            scale = min(scale_width, scale_height)

            # 计算新的图像尺寸
            desired_width = int(original_width * scale)
            desired_height = int(original_height * scale)


            # 调整图像大小
            img = self.original_image.resize((desired_width, desired_height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)

            # 显示图像
            self.image_label.config(image=self.photo)

        self.resize_pending = False

    # 调整各个frame尺寸
    def resize_frames(self, event=None):
        # 计算新的frame宽度为窗口宽度的0.x
        option_width = self.root.winfo_width() * 0.3
        file_height = self.root.winfo_height() * 0.2
        extra_options_height = self.root.winfo_height() * 0.1

        # 更新options_frame的宽度
        self.options_frame.config(width=option_width)
        self.file_and_mode_frame.config(height=file_height)
        self.info_submit_frame.config(height=extra_options_height)


    # 创建子进程并绘制图表
    def draw_plot(self):
        self.progress_label.config(text="绘图中...")
        threading.Thread(target=self.run_analysis, daemon=True).start()

    # 运行分析函数
    def run_analysis(self):
        file_path = "./filtered_dataset/"+self.selected_file.get()
        
        analysis_func = error_pattern

        # 如果是正确率 / 每个异类比例和异类错误热图，则需要传入子选项
        # 这里废弃了选择模式分析
        # if self.selected_analysis.get() == "选择模式分析":
        #     analysis_func = choice_pattern_analysis
        #     analysis_func(file_path, self.sub_selection)
        if self.selected_analysis.get()=="异类错误热图":
            analysis_func = heatmap_per_mode
            analysis_func(file_path, self.sub_selection)
        elif self.selected_analysis.get() == "正确率 / 每个异类比例":
            analysis_func = average_time_with_accuracy_by_specific_mode
            analysis_func(file_path, self.sub_selection)
        # 暂时废弃准确率与平均时间
        # if self.selected_analysis.get() == "准确率与平均时间":
        #     analysis_func = average_time_with_accuracy
        elif self.selected_analysis.get() == "总异类比例与正确率 / 每局":
            analysis_func = alien_ratio_and_correctness_per_trial
            analysis_func(file_path)
        elif self.selected_analysis.get() == "总错误热图":
            analysis_func = total_heatmap
            analysis_func(file_path)
        elif self.selected_analysis.get() == "错误模式":
            analysis_func = error_pattern
            analysis_func(file_path)
        elif self.selected_analysis.get() == "总耗时与正确率 / 每局":
            analysis_func = average_selection_time_and_correctness_per_trial
            analysis_func(file_path)
        elif self.selected_analysis.get() == "点选错误热图":
            analysis_func = click_incorrect_heatmap
            analysis_func(file_path)



        # 在主线程中更新GUI
        self.root.after(100, self.update_canvas)

        # 在主线程中更新进度标签
        self.root.after(0, lambda: self.progress_label.config(text="绘图完成"))

    # 根据分析函数生成的图像文件更新GUI
    def update_canvas(self):

        self.load_image() # 加载图像
        self.resize_show_image() # 调整图像大小
        self.progress_label.config(text="绘图完成")

    # 窗口关闭事件
    def on_close(self):
        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path) # 删除临时图像文件
        # 销毁窗口
        self.root.destroy()

    



# 创建并运行应用
root = tk.Tk()
app = AnalysisApp(root)
root.mainloop()

