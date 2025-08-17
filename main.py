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

    def __init__(self) -> None:
        self.bot_instance = SEA()  # SEA sınıfını kullan
        self.definitions = [
            BotDefinition(
                self.bot_instance,
                self.room_id, self.bot_token)
        ] 

    def run_loop(self) -> None:
        # Streaming thread'i başlat
        streaming_thread = Thread(target=start_streaming, args=(self.bot_instance,))
        streaming_thread.daemon = True
        streaming_thread.start()

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