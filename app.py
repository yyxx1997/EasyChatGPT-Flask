from flask import Flask, render_template, request
from markupsafe import Markup
import openai
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite
import tiktoken
from MessageQueue import MessageQueue

model_name = "gpt-3.5-turbo"
encoding = tiktoken.encoding_for_model(model_name)
openai.api_key = 'xxx'
app = Flask(__name__)
messages = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_bot_response():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    user_input = request.form['user_input']
    log_info = "{} - - Message: {}".format(ip, user_input)
    with open("logs/debug.log", 'a+', encoding="utf8") as file:
        file.write(str(log_info) + '\n')
    if ip in messages.keys():
        messages_queue = messages[ip]
    else:
        messages_queue = MessageQueue(encoding)
        messages[ip] = messages_queue
    final_response = ""
    ret = messages_queue.add_message(user_input, role=MessageQueue.USER)
    if not ret:
        final_response = "Maximum context length is 4096 tokens. \nPlease reducing your tokens in one request per time!"
    else:
        try:
            message_request = messages_queue.get_recent_messages()
            print(message_request)
            completion = openai.ChatCompletion.create(model=model_name,
                                                    messages=message_request,
                                                    timeout=5)
            api_response = completion.choices[0].message['content']
            messages_queue.add_message(api_response, role=MessageQueue.ASSISTANT)
            final_response = api_response
        except Exception as err:
            final_response = "调用失败，原因为：" + str(err) + "\n 如果为网络原因请稍后再试，梯子可能不稳定；如果是token超过上限，请点击清空按钮即可。"
    print("{} - - Message: {}".format(ip, final_response))
    return Markup(markdown.markdown(final_response,extensions=['fenced_code', 'codehilite']))


@app.route('/reset')
def reset():
    # ip = getattr(request.headers, 'X-Real-Ip', request.remote_addr)
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    global messages
    if ip in messages.keys():
        del messages[ip]
    return "Conversation history has been reset."


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
