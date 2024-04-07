from flask import Flask, render_template, jsonify, request

from app.prosto_messenger import db

app = Flask(__name__)

chats = {
    1: {'name': 'Чат 1',
        'messages': [
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},
            {'text': 'Сообщение 1', 'sender': 'мы'}, {'text': 'Сообщение 2', 'sender': 'собеседник'},

        ]},
    2: {'name': 'Чат 2',
        'messages': [{'text': 'Сообщение 3', 'sender': 'мы'}, {'text': 'Сообщение 4', 'sender': 'собеседник'}]},
    3: {'name': 'Чат 3',
        'messages': [{'text': 'Сообщение 5', 'sender': 'мы'}, {'text': 'Сообщение 6', 'sender': 'собеседник'}]},
}


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
    if chat_id in chats:
        message_text = request.form['message']
        db.save_message(chat_id, 'мы', message_text)
        #  chats[chat_id]['messages'].append(message)
        return jsonify(success=True)
    else:
        return jsonify(success=False)


@app.route('/set-ai-status/', methods=['POST'])
def set_ai_status():
    status = request.form.get('status')
    chat_id = request.form.get('chat_id')
    db.save_status(status, chat_id)
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
