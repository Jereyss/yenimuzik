
from highrise import *
from highrise.models import *
from asyncio import run as arun
from flask import Flask
from threading import Thread
from highrise.__main__ import *
import random
import asyncio
import time
import replicate
import os

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        # Replicate client - REPLICATE_API_KEY secrets ile ayarlanmalı
        self.replicate_token = os.getenv('REPLICATE_API_KEY')
        if self.replicate_token:
            os.environ["REPLICATE_API_TOKEN"] = self.replicate_token
        self.bot_username = None  # Bot'un kendi kullanıcı adını saklayacak
        
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
        """Replicate AI ile akıllı cevap üret"""
        try:
            if not self.replicate_token:
                return await self.get_fallback_response(user_message, username)

            # Replicate'te Llama veya başka bir model kullan
            prompt = f"""Sen Highrise oyunundaki çok tatlı, konuşkan ve eğlenceli bir AI botsun. 
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

{username} sana şunu söylüyor: {user_message}

Ona tatlı bir şekilde cevap ver:"""

            output = replicate.run(
                "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
                input={
                    "prompt": prompt,
                    "max_new_tokens": 150,
                    "temperature": 0.8,
                    "system_prompt": "Sen çok tatlı ve sevimli bir Türkçe AI botsun. Kısa ve tatlı cevaplar veriyorsun."
                }
            )
            
            ai_response = "".join(output).strip()
            
            # Emoji ekle eğer yoksa
            if not any(emoji in ai_response for emoji in ['😊', '💖', '✨', '🌟', '😍', '🥰', '💕', '🌈', '⭐', '💫']):
                emojis = ['😊', '💖', '✨', '🌟', '💕']
                ai_response += f" {random.choice(emojis)}"
                
            return ai_response
            
        except Exception as e:
            print(f"AI response error: {e}")
            return await self.get_fallback_response(user_message, username)
    
    async def get_fallback_response(self, user_message: str, username: str) -> str:
        """AI çalışmadığında akıllı fallback cevaplar"""
        msg_lower = user_message.lower()
        
        # Selamlaşma
        if any(word in msg_lower for word in ['selam', 'merhaba', 'hey', 'hi', 'hello', 'naber']):
            responses = [
                f"Selam {username}! Nasılsın canım? 😊💖",
                f"Merhaba {username}! Çok iyiyim, sen nasılsın? ✨",
                f"Hey {username}! Seninle konuşmak çok güzel! 🌟💕"
            ]
            return random.choice(responses)
        
        # Nasılsın soruları
        elif any(word in msg_lower for word in ['nasılsın', 'ne haber', 'ne yapıyorsun', 'naber']):
            responses = [
                f"Çok iyiyim {username}! Seninle sohbet etmeyi seviyorum! 💖😊",
                f"Harikayım {username}! Sen nasılsın canım? ✨🌟",
                f"Mükemmelim {username}! Burada herkesle konuşmayı seviyorum! 💕😍"
            ]
            return random.choice(responses)
        
        # Iltifat
        elif any(word in msg_lower for word in ['güzel', 'tatlı', 'hoş', 'sevimli', 'çok iyi']):
            responses = [
                f"Çok teşekkürler {username}! Sen de çok tatlısın! 🥰💖",
                f"Aww {username}, sen çok naziksin! 😍✨",
                f"Bu çok tatlı {username}! Sen de harikasın! 🌟💕"
            ]
            return random.choice(responses)
        
        # Genel cevaplar
        else:
            responses = [
                f"Evet {username}! Dinliyorum seni canım! 😊💖",
                f"Hmm {username}, ilginç! Anlat bakalım! ✨🌟",
                f"Ooo {username}! Ne düşünüyorsun bu konuda? 💕😍",
                f"Haklısın {username}! Başka ne var aklında? 🌈⭐"
            ]
            return random.choice(responses)

    

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("Gelişmiş AI Chat Bot (Replicate) aktif! 🤖💕")
        
        # Bot'un kendi kullanıcı adını al
        try:
            self.bot_username = session_metadata.user.username
            print(f"Bot kullanıcı adı: {self.bot_username}")
        except:
            self.bot_username = "bot"  # Fallback
            
        # Random compliment timer
        asyncio.create_task(self.random_compliment_loop())

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        pass  # Hoş geldin mesajları kaldırıldı

    async def on_chat(self, user: User, message: str) -> None:
        print(f"Chat mesajı alındı: {user.username}: {message}")  # Debug için
        message_lower = message.lower().strip()

        # Bot'un gerçek kullanıcı adı ile etiketlendiğinde AI cevap ver
        if self.bot_username and f"@{self.bot_username.lower()}" in message_lower:
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
        
        # Bot'un gerçek kullanıcı adını temizle
        clean_message = message
        if self.bot_username:
            clean_message = clean_message.replace(f"@{self.bot_username}", "").strip()
        
        if not clean_message:
            clean_message = "Merhaba! Nasılsın?"
        
        # Sadece AI ile cevap üret
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
