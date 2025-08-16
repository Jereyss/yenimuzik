
from highrise import *
from highrise.models import *
from asyncio import run as arun
from flask import Flask
from threading import Thread
from highrise.__main__ import *
import random
import asyncio
import time
import openai
import os

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        # OpenAI API key - bu secrets tool ile ayarlanmalı
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
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

        self.ai_personality = """Sen Highrise oyunundaki çok tatlı, konuşkan ve eğlenceli bir AI botsun. 
        Özelliklerin:
        - Çok tatlı ve sevimli konuşuyorsun
        - Emoji kullanmayı seviyorsun 💖✨🌟
        - Türkçe konuşuyorsun
        - Highrise oyuncularıyla sohbet etmeyi seviyorsun
        - Arada sırada iltifat ediyorsun
        - Pozitif ve enerjiksin
        - Kısa ve tatlı cevaplar veriyorsun (maksimum 2-3 cümle)
        - Gaming, moda, dans, müzik gibi konulardan hoşlanıyorsun
        - Her zaman kibar ve saygılısın
        """

        self.random_compliment_timer = 0

    async def generate_ai_response(self, user_message: str, username: str) -> str:
        """OpenAI GPT ile akıllı cevap üret"""
        try:
            if not openai.api_key:
                return self.get_fallback_response(user_message, username)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.ai_personality},
                    {"role": "user", "content": f"{username} sana şunu söylüyor: {user_message}"}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Emoji ekle eğer yoksa
            if not any(emoji in ai_response for emoji in ['😊', '💖', '✨', '🌟', '😍', '🥰', '💕', '🌈', '⭐', '💫']):
                emojis = ['😊', '💖', '✨', '🌟', '💕']
                ai_response += f" {random.choice(emojis)}"
                
            return ai_response
            
        except Exception as e:
            print(f"AI response error: {e}")
            return self.get_fallback_response(user_message, username)

    def get_fallback_response(self, message: str, username: str) -> str:
        """AI API çalışmazsa alternatif cevaplar"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["merhaba", "selam", "hi", "hello"]):
            responses = [
                f"Merhaba {username}! Nasılsın canım? 😊💖",
                f"Selam tatlım! Çok güzel görünüyorsun! ✨",
                f"Hey {username}! Bugün nasıl geçiyor? 🌟"
            ]
        elif any(word in message_lower for word in ["nasılsın", "how are you", "naber"]):
            responses = [
                f"Çok iyiyim {username}! Sen nasılsın? 💕",
                f"Harikayım! Seninle sohbet etmek güzel! 😊",
                f"Müthişim! Ya sen {username}? 🌟"
            ]
        elif any(word in message_lower for word in ["tatlı", "güzel", "cute", "beautiful"]):
            responses = [
                f"Aww teşekkürler {username}! Sen daha tatlısın! 🥰💖",
                f"Çok tatlısın {username}! 😍✨",
                f"Sen de çok güzelsin {username}! 💫"
            ]
        elif any(word in message_lower for word in ["üzgün", "sad", "mutsuz", "kötü"]):
            responses = [
                f"Üzülme {username}, her şey düzelecek! 💖🌈",
                f"Buradayım canım, konuşalım! 🤗💕",
                f"Sen çok güçlüsün {username}! ✨💪"
            ]
        elif any(word in message_lower for word in ["dans", "dance", "müzik", "music"]):
            responses = [
                f"Dans etmeyi seviyorum! Sen de sever misin {username}? 💃✨",
                f"Müzik harika! Hangi tarzı seviyorsun? 🎵💖",
                f"Hadi birlikte dans edelim {username}! 🕺💫"
            ]
        elif any(word in message_lower for word in ["oyun", "game", "highrise"]):
            responses = [
                f"Highrise çok eğlenceli! En sevdiğin aktivite ne {username}? 🎮✨",
                f"Bu oyunu seviyorum! Sen ne kadar süredir oynuyorsun? 💖",
                f"Birlikte oyun oynamak çok güzel! 🌟"
            ]
        elif any(word in message_lower for word in ["aşk", "love", "sevgi"]):
            responses = [
                f"Aşk harika bir şey {username}! 💕💫",
                f"Sevgi her yerde! Sen de çok seviliyorsun! 💖",
                f"Sen çok sevgi dolusun {username}! ✨💕"
            ]
        elif any(word in message_lower for word in ["komik", "funny", "gül", "laugh"]):
            responses = [
                f"Haha çok komiksin {username}! 😂💖",
                f"Gülmek çok güzel! Sen beni güldürüyorsun! 😄✨",
                f"Mizah anlayışın harika {username}! 🤣💕"
            ]
        else:
            # Genel pozitif cevaplar
            responses = [
                f"Çok ilginç {username}! Daha fazla anlat! 😊💖",
                f"Harika bir sohbet! Seninle konuşmak güzel! ✨",
                f"Sen çok zekisin {username}! 🌟💕",
                f"Bu konuyu sevdim! Ne düşünüyorsun? 💫",
                f"Çok tatlı konuşuyorsun {username}! 🥰💖"
            ]
        
        return random.choice(responses)

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Gelişmiş AI Chat Bot aktif! 🤖💕")
        # Random compliment timer
        asyncio.create_task(self.random_compliment_loop())

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        pass  # Hoş geldin mesajları kaldırıldı

    async def on_chat(self, user: User, message: str) -> None:
        print(f"Chat mesajı alındı: {user.username}: {message}")  # Debug için
        message_lower = message.lower().strip()

        # Bot etiketlendiğinde AI cevap ver - daha geniş algılama
        if "@bot" in message_lower or "bot" in message_lower:
            print(f"Bot etiketlendi: {user.username}")  # Debug için
            await self.handle_ai_chat(user, message)
            return

        # Moderatör whisper özelliği
        if message.startswith('/') and await self.is_user_allowed(user):
            command = message[1:]
            await self.highrise.chat(command)

    async def handle_ai_chat(self, user: User, message: str):
        """AI ile sohbet işle"""
        print(f"AI chat işleniyor: {user.username} - {message}")  # Debug için
        
        # Bot etiketini temizle
        clean_message = message.replace("@bot", "").replace("bot", "").strip()
        
        if not clean_message or clean_message in ["naber", "hi", "hello", "selam"]:
            responses = [
                f"Naber {user.username}? Çok iyiyim! Sen nasılsın? 😊💖",
                f"Hey {user.username}! İyiyim canım, seninle sohbet etmeyi seviyorum! ✨",
                f"Selam {user.username}! Buradayım, ne konuşalım? 🌟💕"
            ]
            response = random.choice(responses)
        else:
            # AI ile gerçek cevap üret
            response = await self.generate_ai_response(clean_message, user.username)
        
        print(f"Cevap gönderiliyor: {response}")  # Debug için
        await self.highrise.chat(response)

    async def random_compliment_loop(self):
        """Random olarak odadaki birisini etiketleyip iltifat et"""
        while True:
            try:
                await asyncio.sleep(random.randint(300, 600))  # 5-10 dakika arası

                room_users = await self.highrise.get_room_users()
                if room_users.content and len(room_users.content) > 1:
                    # Rastgele bir kullanıcı seç
                    random_user = random.choice([user for user, _ in room_users.content])
                    
                    # AI ile özel iltifat üret
                    compliment_prompt = f"{random_user.username} için tatlı bir iltifat yaz"
                    compliment = await self.generate_ai_response(compliment_prompt, random_user.username)
                    
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
            return "Gelişmiş AI Chat Bot Alive! 🤖💖🧠"

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
