2024.3.2修复无法生成完整章节内容bug，添加apibase设置，更新模型列表，添加小说大纲，增加更多可玩性！
# 小说创作脚本-plus

这是一个使用OpenAI API生成小说章节的脚本。


## 如何使用

1. 将 API 密钥和其他配置信息填入 `settings.config` 文件。

2. 运行脚本，它将自动生成小说的章节。

## 安装依赖

确保已安装必要的依赖，使用Python版本为3.8以上。

```bash
pip install -r requirements.txt

```
## 效果如图：
![屏幕截图 2024-03-02 001810](https://github.com/buwanyuanshen/ChatGPT-NovelWrite/assets/144007759/68fcb66c-751d-44c7-91d1-897b6a8f3e27)
![屏幕截图 2024-03-02 001927](https://github.com/buwanyuanshen/ChatGPT-NovelWrite/assets/144007759/76601cf6-5c4e-4663-8a9d-22ce0dd80469)


## 配置文件

在 `settings.config` 中配置了小说名称、大纲，总章节数、API密钥等信息。

```ini
[Settings]
novel_name = Your_Novel_Name
novel_outline = 小说大纲
total_chapters = 3
api_keys = Your_API_Key_1,Your_API_Key_2
selected_model = gpt-3.5-turbo-0125
temperature = 0.5
max_tokens = 2000
tokens_per_chapter = 400
```

## 模型选择

你可以在 `settings.config` 中选择不同的OpenAI模型，如 `gpt-3.5-turbo-1106`、`gpt-3.5-turbo`等。

## 开始编写

运行脚本，并在窗口中填入小说名称、大纲、总章节数等参数，点击“开始编写”按钮即可。

## 注意事项

- 请确保 API 密钥的安全性，不要分享到公共场合。
- 请根据实际需要修改章节内容的生成方式。


请替换“Your_Novel_Name”和“Your_API_Key_1, Your_API_Key_2”等内容为你实际的小说名称和API密钥。同时，你也可以根据实际需要添加或修改其他信息。
