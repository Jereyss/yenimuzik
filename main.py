from highrise import *
from highrise.models import *
from asyncio import run as arun
from flask import Flask
from threading import Thread
from highrise.__main__ import *
import random
import asyncio
import time
import os
from youtubezeno import SEA, start_streaming
from HRDB import ownerz, playlist, user_ticket, vip_users, msg, restrict, promo, bot_location, ids

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.bot_username = None

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Müzik Bot aktif! 🎵🤖")

        # Bot'un kendi kullanıcı adını al
        try:
            self.bot_username = session_metadata.user.username
            print(f"Bot kullanıcı adı: {self.bot_username}")
        except:
            self.bot_username = "bot"  # Fallback

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        await self.highrise.send_whisper(user.id, "🎵 Müzik botuna hoş geldin! Şarkı istemek için /play [şarkı adı] kullan!")

    async def on_chat(self, user: User, message: str) -> None:
        print(f"Chat mesajı alındı: {user.username}: {message}")

        # Temel komutları burada işleyebiliriz, ana müzik komutları youtubezeno.py'de
        if message.startswith('/help'):
            await self.highrise.send_whisper(user.id, "🎵 Müzik Bot Komutları:\n/play [şarkı] - Şarkı çal\n/queue - Sırayı göster\n/skip - Şarkıyı geç\n/now - Şu an çalan\n/wallet - Bilet durumu")

    async def on_whisper(self, user: User, message: str) -> None:
        # Whisper komutlarını işle
        pass

    async def run(self, room_id, token) -> None:
        await __main__.main(self, room_id, token)

class WebServer():
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index() -> str:
            return "Müzik Bot Çalışıyor! 🎵🤖"

    def run(self) -> None:
        self.app.run(host='0.0.0.0', port=8080)

    def keep_alive(self):
        t = Thread(target=self.run)
        t.start()

class RunBot():
    room_id = "675f21fcecbfd6b18c0474f3"
    bot_token = "de29bb353e3d2be63f50157cb3d6c857bfc6ab46bb21b53451d903e015f76831"
    bot_file = "main"
    bot_class = "Bot"

    def __init__(self) -> None:
        self.definitions = [
            BotDefinition(
                getattr(import_module(self.bot_file), self.bot_class)(),
                self.room_id, self.bot_token)
        ] 

    def run_loop(self) -> None:
        while True:
            try:
                arun(main(self.definitions)) 
            except Exception as e:
                import traceback
                print("Caught an exception:")
                traceback.print_exc()
                time.sleep(1)
                continue

if __name__ == "__main__":
    WebServer().keep_alive()
    RunBot().run_loop()