from flask import Flask, render_template, request
from markupsafe import Markup
import openai
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite

openai.api_key = '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'
app = Flask(__name__)
messages = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    ip = request.remote_addr
    user_input = request.form['user_input']
    messages_ip = messages.get(ip, []) + [{'role': 'user', 'content': user_input}]
    # print(messages_ip)
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_ip,
            timeout=5
        )
        ai_response = completion.choices[0].message['content']
        messages_ip.append({'role': 'assistant', 'content': ai_response})
        messages[ip] = messages_ip
    except Exception as err:
        ai_response = "调用失败，原因为：" + str(err)
        print(ai_response)
    print("{} - - Message: {}".format(ip, messages_ip))
    with open("logs/debug.txt", 'a+', encoding="utf8") as file:
        file.write(str(messages)+'\n')
    return  Markup(markdown.markdown(ai_response, extensions=['fenced_code', 'codehilite']))

@app.route('/reset')
def reset():
    ip = request.remote_addr
    global messages
    messages[ip] = []
    return "Conversation history has been reset."
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
