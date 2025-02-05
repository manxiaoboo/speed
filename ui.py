import tkinter as tk
import local_status
from PIL import Image, ImageTk  # 导入PIL库来处理图片

def show():
    # 更新 local_status 中的数据
    def update_status():
        display_status()

    # 实时更新状态显示区域
    def display_status():
        game_text = f"Target: {local_status.Target_1}-{local_status.Target_2}"
        status_text = f"MQTT: {local_status.MQTT_Ready}\nCamera: {local_status.Camera_Ready}"
        log_text = f"2025/02/05 1:17:20 All Ready!"
        game_label.config(text=game_text)
        status_label.config(text=status_text)
        log_label.config(text=log_text)

    # 创建主窗口
    root = tk.Tk()
    root.title("Speed Control Panel")
    root.geometry("1920x1080")  # 设置窗口大小

    # 创建一个容器分为左右两栏
    left_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=20)
    
    center_frame = tk.Frame(root)
    center_frame.grid(row=0, column=1, sticky="nw", padx=20, pady=20)

    right_frame = tk.Frame(root)
    right_frame.grid(row=0, column=2, sticky="ne", padx=20, pady=210)


    # Game Information
    game_fieldset_frame = tk.Frame(left_frame, bd=1, relief="solid", padx=20, pady=10, width=200, height=250)
    game_fieldset_frame.grid(row=0, column=0, sticky="w", pady=10)
    game_fieldset_frame.grid_propagate(False)
    
    # 添加标题
    game_fieldset_title = tk.Label(game_fieldset_frame, text="Game Information", font=("Arial", 12, "bold"))
    game_fieldset_title.grid(row=0, column=0, sticky="w")
    
    # 显示当前比赛信息的标签，确保文本左对齐
    game_label = tk.Label(game_fieldset_frame, text="", justify=tk.LEFT, anchor="w")
    game_label.grid(row=1, column=0, sticky="w", pady=10)  # 在左侧显示

    # Status Information
    status_fieldset_frame = tk.Frame(left_frame, bd=1, relief="solid", padx=20, pady=10, width=200, height=250)
    status_fieldset_frame.grid(row=1, column=0, sticky="w", pady=10)
    status_fieldset_frame.grid_propagate(False)
    
    # 添加标题
    status_fieldset_title = tk.Label(status_fieldset_frame, text="Status Information", font=("Arial", 12, "bold"))
    status_fieldset_title.grid(row=0, column=0, sticky="w")
    
    # 显示当前状态的标签，确保文本左对齐
    status_label = tk.Label(status_fieldset_frame, text="", justify=tk.LEFT, anchor="w")
    status_label.grid(row=1, column=0, sticky="w", pady=10)  # 在左侧显示

    # Log Information
    log_fieldset_frame = tk.Frame(center_frame, bd=1, relief="solid", padx=20, pady=10, width=720, height=900)
    log_fieldset_frame.grid(row=0, column=0, sticky="w", pady=10)
    log_fieldset_frame.grid_propagate(False)
    
    # 添加标题
    log_fieldset_title = tk.Label(log_fieldset_frame, text="Runtime Logs", font=("Arial", 12, "bold"))
    log_fieldset_title.grid(row=0, column=0, sticky="w")
    
    # 显示当前状态的标签，确保文本左对齐
    log_label = tk.Label(log_fieldset_frame, text="", justify=tk.LEFT, anchor="w")
    log_label.grid(row=1, column=0, sticky="w", pady=10)  # 在左侧显示

    # 表单区域：添加输入框，确保所有标签和输入框左对齐
    form_frame = tk.Frame(left_frame)
    form_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)  # 在左侧显示表单
    
    # 按钮
    button_title1 = tk.Label(left_frame, text="Status Operation", font=("Arial", 10, "bold"))
    button_title1.grid(row=2, column=0, sticky="w")
    status1_button = tk.Button(left_frame, text="State => 'Tracking'", command=update_status)
    status1_button.grid(row=3, column=0, sticky="w", pady=10)  # 在左侧显示按钮
    status2_button = tk.Button(left_frame, text="State => 'Aim'", command=update_status)
    status2_button.grid(row=4, column=0, sticky="w", pady=10)  # 在左侧显示按钮
    status3_button = tk.Button(left_frame, text="State => 'Grab'", command=update_status)
    status3_button.grid(row=5, column=0, sticky="w", pady=10)  # 在左侧显示按钮
    status4_button = tk.Button(left_frame, text="State => 'Turn Round'", command=update_status)
    status4_button.grid(row=6, column=0, sticky="w", pady=10)  # 在左侧显示按钮
    status5_button = tk.Button(left_frame, text="State => 'Tracking And Ending'", command=update_status)
    status5_button.grid(row=7, column=0, sticky="w", pady=10)  # 在左侧显示按钮

    # 加载小车图片
    try:
        car_image = Image.open("pictures/pic_now.jpg")  # 替换成你的小车图片路径
        car_image = car_image.resize((640, 480))  # 设置图片的显示大小
        car_photo = ImageTk.PhotoImage(car_image)
        car_label = tk.Label(right_frame, image=car_photo)
        car_label.image = car_photo  # 必须保留引用
        car_label.grid(row=0, column=0, sticky="n", pady=10)  # 在右侧居中显示图片
    except Exception as e:
        print("Error loading image:", e)

    # 初次显示状态
    display_status()

    # 启动主事件循环
    root.mainloop()