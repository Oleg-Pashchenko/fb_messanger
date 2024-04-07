from flask import Flask, render_template, jsonify, request

import db

app = Flask(__name__)


@app.route('/')
def index():
    chats = db.get_chats()
    chats_data = {}
    for chat in chats:
        chats_data[chat[0]] = {'name': chat[1]}
    return render_template('index.html', chats=chats_data)


@app.route('/messages/<int:chat_id>')
def get_messages(chat_id):
    messages, ai = db.get_by_chat_id(chat_id)
    messages_data = []
    for message in messages:
        messages_data.append({'text': message[1], 'sender': message[2]})
    if len(messages_data) != 0:
        return jsonify({'messages': messages_data, 'ai_status': ai})
    else:
        return jsonify([])


@app.route('/send_message/<int:chat_id>', methods=['POST'])
def send_message(chat_id):
    message_text = request.form['message']
    db.save_message(chat_id, 'мы', message_text)
    return jsonify(success=True)


@app.route('/set-ai-status/', methods=['POST'])
def set_ai_status():
    status = request.form.get('status')
    chat_id = request.form.get('chat_id')
    db.save_status(status, chat_id)
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
