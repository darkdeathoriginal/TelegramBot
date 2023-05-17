import requests
import multiprocessing
from pyrogram import Client, filters
from dotenv import load_dotenv
import os
from flask import Flask, send_from_directory
from gevent.pywsgi import WSGIServer

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
webhook_url = os.getenv("WEBHOOK_URL")

app = Client("my_account",api_id=api_id, api_hash=api_hash)


flask_app = Flask(__name__)

@flask_app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory('./downloads', filename, as_attachment=True)



@app.on_message(~filters.me)
async def start(client, message):
    return 0


@app.on_message(filters.command("start"))
async def start(client, message):
    await app.send_message(message.chat.id, "Bot started")


@app.on_message(filters.command("send"))
async def send(client, message):
    fileName = message.reply_to_message.document.file_name
    Mime = message.reply_to_message.document.mime_type
    await app.download_media(message.reply_to_message, file_name="temp.mp4")
    print("download finnished")

    post_data = {
        "jid": "919072215994@s.whatsapp.net",
        "buffer": "temp",
        "filename": fileName,
        "mime": Mime,
    }

    response = requests.post(
        webhook_url, json=post_data
    )

    if response.status_code == 200:
        print(response)
    else:
        print(f"Request failed with status code {response.status_code}")


@app.on_message(filters.command("exec"))
async def exec(client, message):
    await eval(message.command[1])


@app.on_message(filters.command("edit"))
async def edit(client, message):
    await app.edit_message_text(
        message.chat.id, message.reply_to_message_id, message.command[1]
    )


def run_telegram():
    app.run()

def run_flask():
    http_server = WSGIServer(('0.0.0.0', 5555), flask_app)
    http_server.serve_forever()

if __name__ == '__main__':
    telegram_process = multiprocessing.Process(target=run_telegram)
    flask_process = multiprocessing.Process(target=run_flask)

    telegram_process.start()
    flask_process.start()

    telegram_process.join()
    flask_process.join()
