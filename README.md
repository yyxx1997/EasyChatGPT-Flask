# EasyChatGPT-Flask

用python和flask简单实现调用chatGPT的API，支持上下文回复、latex公式渲染、和代码高亮。

EasyChatGPT-Flask 是一个使用 [OpenAI GPT-3.5 API](https://openai.com/)（也就是ChatGPT） 实现的简单聊天机器人 。使用 Python 的 Flask 框架编写。

## 使用

1.  克隆仓库到本地


2.  进入项目目录


3.  安装依赖

`pip install flask markupsafe openai markdown` 

4. 在 'app.py' 中设置你自己的 OpenAI APE key

`openai.api_key = 'YOUR_API_KEY'` 

5.  运行项目

`python app.py` 

6.  访问网页

默认访问 127.0.0.1:5000 即可

## API 使用说明

-   `/get_response`：用于获取聊天机器人的回复。需要以 POST 请求发送用户输入，并返回聊天机器人的回复。
-   `/reset`：用于重置聊天历史记录以及上下文。

## 代码说明

-   `app.py`：Flask 项目主文件，包含了 API 接口的定义和聊天机器人的实现。

## 许可证

EasyChatGPT-Flask 使用 MIT 许可证。请参阅 [LICENSE](https://chat.openai.com/chat/LICENSE) 文件了解详情。
