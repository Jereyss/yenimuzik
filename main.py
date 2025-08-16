from highrise import *
from highrise.models import *
from asyncio import run as arun
from flask import Flask
from threading import Thread
from highrise.__main__ import *
import random
import asyncio
import time

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.compliments = [
            "Çok tatlı görünüyorsun! 💖",
            "Stilin harika! ✨",
            "Bugün çok güzel görünüyorsun! 🌟",
            "Enerjin çok pozitif! 😊",
            "Çok şık duruyorsun! 👑",
            "Gülüşün çok güzel! 😍",
            "Harika bir vibe'ın var! 🌈",
            "Çok karizmatiksin! ⭐",
            "Outfitin mükemmel! 👗",
            "Çok yakışıklısın/güzelsin! 💫"
        ]

        self.responses = {
            "merhaba": ["Merhaba tatlım! 🌸", "Selam canım! 💕", "Merhaba güzelim! ✨"],
            "nasılsın": ["Çok iyiyim, sen nasılsın? 😊", "Harikayım! Sen nasılsın canım? 💖", "Müthişim! Ya sen? 🌟"],
            "günaydın": ["Günaydın tatlım! ☀️", "Günaydın canım, güzel bir gün! 🌅", "Günaydın güzelim! 🌻"],
            "iyi geceler": ["İyi geceler canım! 🌙", "Tatlı rüyalar! 💤", "İyi geceler güzelim! ⭐"],
            "teşekkürler": ["Rica ederim tatlım! 💕", "Ne demek canım! 😊", "Her zaman! 💖"],
            "tatlı": ["Teşekkür ederim canım, sen de çok tatlısın! 💖", "Aww, çok tatlısın! 🥰", "Sen daha tatlısın! 💕"],
            "güzel": ["Sen daha güzelsin! ✨", "Teşekkürler canım! 💖", "Çok tatlısın! 🌟"],
            "seviyorum": ["Ben de seni seviyorum! 💕", "Aww, çok tatlısın! 🥰", "Sen çok özelsin! 💖"],
        }

        self.random_compliment_timer = 0

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("AI Chat Bot aktif! 🤖💕")
        await self.highrise.chat("Merhaba herkese! Ben yeni AI sohbet botunuzum! Benimle konuşmak için @bot ile etiketleyin! 💖")

        # Random compliment timer
        asyncio.create_task(self.random_compliment_loop())

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        welcome_messages = [
            f"Hoş geldin {user.username}! Çok güzel görünüyorsun! 💖",
            f"Merhaba {user.username}! Odaya güzellik getirdin! ✨",
            f"Hoş geldin {user.username}! Çok tatlısın! 🌟"
        ]
        message = random.choice(welcome_messages)
        await self.highrise.chat(message)

    async def on_chat(self, user: User, message: str) -> None:
        message_lower = message.lower().strip()

        # Bot etiketlendiğinde cevap ver
        if "@bot" in message_lower:
            await self.handle_bot_mention(user, message_lower)
            return

        # Moderatör whisper özelliği
        if message.startswith('/') and await self.is_user_allowed(user):
            command = message[1:]
            await self.highrise.chat(command)

    async def handle_bot_mention(self, user: User, message: str):
        # Bot etiketini temizle
        clean_message = message.replace("@bot", "").strip()

        # Özel yanıtlar
        if any(word in clean_message for word in ["tatlı", "cute", "güzel", "beautiful"]):
            responses = [
                f"Aww teşekkürler {user.username}! Sen daha tatlısın! 🥰💖",
                f"Çok tatlısın {user.username}! Sen çok özelsin! ✨💕",
                f"Sen de çok güzelsin {user.username}! 😍💫"
            ]

        elif any(word in clean_message for word in ["merhaba", "selam", "hi", "hello"]):
            responses = [
                f"Merhaba {user.username}! Nasılsın canım? 😊💖",
                f"Selam tatlım! Çok güzel görünüyorsun! ✨",
                f"Merhaba güzelim! Bugün nasıl geçiyor? 🌟"
            ]

        elif any(word in clean_message for word in ["nasılsın", "how are you", "naber"]):
            responses = [
                f"Çok iyiyim {user.username}! Sen nasılsın canım? 💕",
                f"Harikayım! Sen nasılsın tatlım? 😊",
                f"Müthişim! Ya sen {user.username}? 🌟"
            ]

        elif any(word in clean_message for word in ["sıkıldım", "bored", "ne yapıyorsun"]):
            responses = [
                f"Gel biraz sohbet edelim {user.username}! ✨",
                f"Buradayım seninle sohbet etmek için! 💖",
                f"Sıkılma canım, birlikte vakit geçirelim! 😊"
            ]

        elif any(word in clean_message for word in ["üzgün", "sad", "mutsuz"]):
            responses = [
                f"Üzülme {user.username}, her şey düzelecek! 💖🌈",
                f"Buradayım canım, konuşmak istersen! 🤗💕",
                f"Sen çok güçlüsün {user.username}! ✨💪"
            ]

        elif any(word in clean_message for word in ["teşekkür", "thanks", "sağol"]):
            responses = [
                f"Rica ederim {user.username}! 💕",
                f"Ne demek canım! Her zaman! 😊💖",
                f"Sevgiyle {user.username}! ✨"
            ]

        elif any(word in clean_message for word in ["dans", "dance", "müzik"]):
            responses = [
                f"Dans etmeyi seviyorum! Sen de sever misin {user.username}? 💃✨",
                f"Müzik harika! Hangi müziği seviyorsun {user.username}? 🎵💖",
                f"Hadi birlikte dans edelim {user.username}! 🕺💫"
            ]

        elif any(word in clean_message for word in ["aşk", "love", "sevgi"]):
            responses = [
                f"Aşk harika bir şey {user.username}! 💕💫",
                f"Sevgi her yerde {user.username}! Sen de çok seviliyorsun! 💖",
                f"Sen çok sevgi dolusun {user.username}! ✨💕"
            ]

        else:
            # Genel sohbet yanıtları
            responses = [
                f"Çok ilginç {user.username}! Daha fazla anlat! 😊💖",
                f"Harika bir sohbet {user.username}! ✨",
                f"Sen çok zekisin {user.username}! 🌟💕",
                f"Seninle konuşmak çok güzel {user.username}! 💫",
                f"Çok tatlı düşünüyorsun {user.username}! 🥰"
            ]

        response = random.choice(responses)
        await self.highrise.chat(response)

    async def random_compliment_loop(self):
        """Random olarak odadaki birisini etiketleyip iltifat et"""
        while True:
            try:
                await asyncio.sleep(random.randint(180, 300))  # 3-5 dakika arası

                room_users = await self.highrise.get_room_users()
                if room_users.content:
                    # Rastgele bir kullanıcı seç
                    random_user = random.choice([user for user, _ in room_users.content])
                    compliment = random.choice(self.compliments)

                    await self.highrise.chat(f"@{random_user.username} {compliment}")

            except Exception as e:
                print(f"Random compliment error: {e}")

    async def is_user_allowed(self, user: User) -> bool:
        try:
            user_privileges = await self.highrise.get_room_privilege(user.id)
            return user_privileges.moderator or user.username in ["Atekinz", ""]
        except:
            return False

    async def on_whisper(self, user: User, message: str) -> None:
        if await self.is_user_allowed(user):
            try:
                await self.highrise.chat(message)
            except Exception as e:
                print(f"Whisper error: {e}")

    async def on_user_move(self, user: User, pos: Position) -> None:
        pass

    async def run(self, room_id, token) -> None:
        await __main__.main(self, room_id, token)

class WebServer():
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index() -> str:
            return "AI Chat Bot Alive! 🤖💖"

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