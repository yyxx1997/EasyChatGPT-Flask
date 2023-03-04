from flask import Flask, render_template, request
from markupsafe import Markup
import openai
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite

openai.api_key = 'sk-xxxxxx'
app = Flask(__name__)
messages = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    ip = request.remote_addr
    user_input = request.form['user_input']
    print(messages)
    messages_ip = messages.get(ip, []) + [{'role': 'user', 'content': user_input}]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_ip
    )
    ai_response = completion.choices[0].message['content']
    messages_ip.append({'role': 'assistant', 'content': ai_response})
    messages[ip] = messages_ip
    print("{} - - Message: {}".format(ip, messages_ip))
    return  Markup(markdown.markdown(ai_response, extensions=['fenced_code', 'codehilite']))

@app.route('/reset')
def reset():
    ip = request.remote_addr
    global messages
    messages[ip] = []
    return "Conversation history has been reset."
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
