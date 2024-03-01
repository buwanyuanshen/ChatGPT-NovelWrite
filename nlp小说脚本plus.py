import asyncio
import os
from tkinter import ttk
import openai
import random
import tkinter as tk
import threading
import configparser

openai.api_base = "https://api.openai-proxy.com/v1"


# 检查配置文件是否存在，如果不存在则创建新的配置文件
if not os.path.exists('settings.config'):
    config = configparser.ConfigParser()
    config['Settings'] = {}
    config['Settings']['novel_name'] = ''
    config['Settings']['total_chapters'] = '3'
    config['Settings']['api_keys'] = ''
    config['Settings']['selected_model'] = 'gpt-3.5-turbo-0125'
    config['Settings']['temperature'] = '0.5'
    config['Settings']['max_tokens'] = '1000'
    config['Settings']['tokens_per_chapter'] = '100'

    with open('settings.config', 'w') as configfile:
        config.write(configfile)


# 读取配置文件
config = configparser.ConfigParser()
with open('settings.config', 'r') as configfile:
    config.read_file(configfile)

novel_name = config.get('Settings', 'novel_name', fallback='')
total_chapters = config.getint('Settings', 'total_chapters', fallback=3)
api_keys_entry = config.get('Settings', 'api_keys', fallback='')
selected_model = config.get('Settings', 'selected_model', fallback='gpt-3.5-turbo-0125')
temperature = config.getfloat('Settings', 'temperature', fallback=0.5)
max_tokens = config.getint('Settings', 'max_tokens', fallback=1000)
tokens_per_chapter = config.getint('Settings', 'tokens_per_chapter', fallback=100)

# 异步加载 API 密钥
async def load_api_keys():
    global api_keys_entry
    await asyncio.sleep(0.1)  # 延迟加载，避免卡住主线程
    return [key.strip() for key in api_keys_entry.split(',')]

async def main():
    global api_keys
    api_keys = await load_api_keys()

# 启动异步事件循环
loop = asyncio.get_event_loop()
loop.run_until_complete(main())


# 写入小说章节
def write_novel_chapter(api_key, model, chapter_content, chapter_number, conversation_history, max_tokens_var):
    """使用OpenAI的API模型来编写小说章节"""
    global temperature_var

    openai.api_key = api_key  # 设置当前使用的 API 密钥
    response = openai.ChatCompletion.create(
        model=model,  # 使用传入的模型
        temperature=temperature_var,
        max_tokens=max_tokens_var,
        messages=conversation_history + [
            {
                "role": "system",
                "content": f"你是一名专业的小说家，你的任务是编写小说《{novel_name}》，共有{total_chapters}章，每章{tokens_per_chapter}字，请自行构思每章章的标题和内容，开始编写第{chapter_number}章:"
            },
            {"role": "user", "content": chapter_content},
        ]
    )
    generated_text = response['choices'][0]['message']['content']
    return generated_text, response['choices'][0]['message']['role'], response['choices'][0]['index']



def write_novel():
    global novel_name, total_chapters, output_folder, selected_model, tokens_per_chapter
    chapter_number = 1
    conversation_history = []
    used_api_keys = []

    while chapter_number <= total_chapters:
        available_keys = [key for key in api_keys if key not in used_api_keys]

        if not available_keys:
            used_api_keys = []
            available_keys = api_keys[:]

        selected_api_key = random.choice(available_keys)
        used_api_keys.append(selected_api_key)

        print(f"正在编写《{novel_name}》第 {chapter_number} 章，使用的 API 密钥：{selected_api_key}")

        try:
            # 模拟章节内容，你可以根据实际需要修改
            chapter_content = f""
            tokens_per_chapter_var = tokens_per_chapter

            generated_text, _, _ = write_novel_chapter(selected_api_key, selected_model, chapter_content, chapter_number,
                                                       conversation_history, tokens_per_chapter_var)

            chapter_name = generated_text.split('\n', 1)[0]

            if "第" in chapter_name and "章" in chapter_name:
                chapter_file_name = f"{chapter_name}.txt"
            else:
                chapter_file_name = f"第{chapter_number}章：{chapter_name}.txt"

            # 去掉包含小说名称的部分
            chapter_file_name = chapter_file_name.replace(novel_name, "")

            # 去掉包含《》的部分
            if "《" in chapter_file_name and "》" in chapter_file_name:
                chapter_file_name = chapter_file_name.replace("《", "").replace("》", "")

            # 去掉多余的空格
            chapter_file_name = chapter_file_name.strip()
            chapter_file_path = os.path.join(output_folder, chapter_file_name)
            with open(chapter_file_path, 'w', encoding='utf-8') as chapter_file:
                chapter_file.write(generated_text)

            print(f"《{novel_name}》 {chapter_file_name.strip('.txt')} 编写成功，已保存至 {chapter_file_path}")
            print("-------------------------------------------------------------------")

            conversation_history = []

            if chapter_number < total_chapters:
                conversation_history.append({"role": "system", "content": generated_text})

        except Exception as e:
            print(f"《{novel_name}》 第{chapter_number}章 编写失败，错误信息: {e}")
            print("-------------------------------------------------------------------")

        chapter_number += 1

def start_writing():
    global novel_name, total_chapters, output_folder, selected_model, temperature, max_tokens, tokens_per_chapter, temperature_var, max_tokens_var, api_keys

    novel_name = novel_name_entry.get()
    total_chapters = int(total_chapters_entry.get())
    output_folder = os.path.join(os.path.expanduser('~'), 'Desktop', novel_name)
    selected_model = model_var.get()
    temperature = float(temperature_entry.get())
    max_tokens = int(max_tokens_entry.get())
    tokens_per_chapter = int(tokens_per_chapter_entry.get())
    temperature_var = float(temperature_entry.get())
    max_tokens_var = int(max_tokens_entry.get())
    api_keys = [key.strip() for key in api_keys_entry.get().split(',')]  # 获取并更新 API 密钥列表

    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        threading.Thread(target=write_novel).start()

    except Exception as e:
        print("")

    # 更新配置文件
    config['Settings']['novel_name'] = novel_name
    config['Settings']['total_chapters'] = str(total_chapters)
    config['Settings']['selected_model'] = selected_model
    config['Settings']['temperature'] = str(temperature)
    config['Settings']['max_tokens'] = str(max_tokens)
    config['Settings']['tokens_per_chapter'] = str(tokens_per_chapter)
    config['Settings']['api_keys'] = ', '.join([key.strip() for key in api_keys_entry.get().split(',')])

    with open('settings.config', 'w') as configfile:
        config.write(configfile)
def toggle_visibility():
    current_state = api_keys_entry.cget("show")
    new_state = "" if current_state == "*" else "*"
    api_keys_entry.config(show=new_state)


# 创建 Tkinter 窗口
window = tk.Tk()
window.title("小说创作脚本-plus")
window.geometry("300x400")
# 设置窗口自适应内容大小
window.pack_propagate(True)

# 使用ttk.Style设置浅蓝色风格
style = ttk.Style()
style.configure('TButton', foreground='navy', background='blue')
style.configure('TEntry', foreground='black', fieldbackground='black')
style.configure('TLabel', foreground='black', background='lightblue')
style.configure('TMenubutton', foreground='navy', background='lightblue')
style.configure('TCombobox', foreground='navy', background='lightblue')

api_keys_label = ttk.Label(window, text="API密钥（用逗号分隔多个密钥）:", padding=(20, 5))
api_keys_label.pack()

api_keys_entry = ttk.Entry(window, width=40, show="*")
api_keys_entry.insert(0, ', '.join(api_keys))
api_keys_entry.pack()

# 在Entry组件上绑定Ctrl+V键
api_keys_entry.bind('<Control-v>', lambda e: api_keys_entry.event_generate('<<Paste>>'))
api_keys_entry.pack()
show_hide_button = ttk.Button(window, text="显示/隐藏", command=toggle_visibility)

# 布局Entry组件和按钮
api_keys_entry.pack(pady=5)
show_hide_button.pack(pady=5)
# 创建和放置窗口组件（包括每章字数的输入框）
novel_name_label = ttk.Label(window, text="小说名称:")
novel_name_label.pack()

novel_name_entry = ttk.Entry(window,width=20)
novel_name_entry.insert(0, novel_name)
novel_name_entry.pack()

total_chapters_label = ttk.Label(window, text="总章节数:")
total_chapters_label.pack()

total_chapters_entry = ttk.Entry(window)
total_chapters_entry.insert(0, total_chapters)  # 设置默认值
total_chapters_entry.pack()

model_options = [
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
    "gpt-4-1106-preview",
    "gpt-4-turbo-preview",
    "gpt-4-0125-preview",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-4-32k-0613",

]

model_var = tk.StringVar(window)
model_var.set(selected_model)

model_label = ttk.Label(window, text="选择模型:")
model_label.pack()

model_combobox = ttk.Combobox(window, textvariable=model_var, values=model_options, state="readonly")
model_combobox.pack()

temperature_label = ttk.Label(window, text="temperature:")
temperature_label.pack()

temperature_entry = ttk.Entry(window)
temperature_entry.insert(0, temperature)  # 设置默认值
temperature_entry.pack()

max_tokens_label = ttk.Label(window, text="max_tokens:")
max_tokens_label.pack()

max_tokens_entry = ttk.Entry(window)
max_tokens_entry.insert(0, max_tokens)  # 设置默认值
max_tokens_entry.pack()

tokens_per_chapter_label = ttk.Label(window, text="每章字数:")
tokens_per_chapter_label.pack()

tokens_per_chapter_entry = ttk.Entry(window)
tokens_per_chapter_entry.insert(0, tokens_per_chapter)  # 设置默认值
tokens_per_chapter_entry.pack()

start_button = ttk.Button(window, text="开始编写", command=lambda: start_writing())
start_button.pack()
def save_config():
    # 获取当前输入框中的配置信息
    novel_name_value = novel_name_entry.get()
    total_chapters_value = str(total_chapters_entry.get())
    selected_model_value = model_var.get()
    temperature_value = str(temperature_entry.get())
    max_tokens_value = str(max_tokens_entry.get())
    tokens_per_chapter_value = str(tokens_per_chapter_entry.get())
    api_keys_value = ', '.join(api_keys_entry.get().split(','))  # 更新 API 密钥列表

    # 确保Settings部分存在
    if 'Settings' not in config:
        config.add_section('Settings')

    # 更新或添加配置信息到Settings部分
    config.set('Settings', 'novel_name', novel_name_value)
    config.set('Settings', 'total_chapters', total_chapters_value)
    config.set('Settings', 'selected_model', selected_model_value)
    config.set('Settings', 'temperature', temperature_value)
    config.set('Settings', 'max_tokens', max_tokens_value)
    config.set('Settings', 'tokens_per_chapter', tokens_per_chapter_value)
    config.set('Settings', 'api_keys', api_keys_value)

    # 将配置信息保存到配置文件
    with open('settings.config', 'w') as configfile:
        config.write(configfile)
    window.destroy()  # 关闭窗口

# 在窗口关闭时触发保存配置事件
window.protocol("WM_DELETE_WINDOW", save_config)
# 进入 Tkinter 事件循环
window.mainloop()
