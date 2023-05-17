import requests
from pyrogram import Client, filters
import base64
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
webhook_url = os.getenv("WEBHOOK_URL")

app = Client("my_account",api_id=api_id, api_hash=api_hash)
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
    with open("./downloads/temp.mp4", "rb") as file:
        file_data = file.read()

    post_data = {
        "jid": "919072215994@s.whatsapp.net",
        "buffer": base64.b64encode(file_data).decode("utf-8"),
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


app.run()
