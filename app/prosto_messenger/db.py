import psycopg2
import dotenv
import os

dotenv.load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)


def get_by_chat_id(chat_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages WHERE chat_id = %s;", (chat_id,))
    messages_data = cur.fetchall()
    cur.execute("SELECT ai_answer FROM chats WHERE id = %s;", (chat_id,))
    ai = cur.fetchone()[0]
    cur.close()
    return messages_data, ai




def get_chats():
    cur = conn.cursor()
    cur.execute("SELECT * FROM chats;")
    chats_data = cur.fetchall()
    cur.close()
    return chats_data


def save_message(chat_id, sender, message):
    cur = conn.cursor()
    cur.execute('INSERT INTO messages (chat_id, sender, message) VALUES (%s, %s, %s)', (chat_id, sender, message))
    conn.commit()
    cur.close()


def save_status(status, chat_id):
    cur = conn.cursor()
    cur.execute("UPDATE chats SET ai_answer=%s WHERE id=%s", (status, chat_id))
    conn.commit()
    cur.close()