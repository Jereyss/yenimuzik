
import os
import json
import sys
import string
import shutil
import asyncio
import threading
import yt_dlp
import os
import tempfile
import time
import base64
import subprocess
import asyncio
from asyncio import run as arun
from highrise import BaseBot, __main__
from highrise.models import User, SessionMetadata, Position
from highrise import *
from highrise.webapi import *
from highrise.models_webapi import *
from highrise.models import *
import socket
import aiohttp
import aiofiles
import yt_dlp
from mutagen.mp3 import MP3
from collections import deque
import random
from datetime import datetime, timedelta
from HRDB import ownerz, playlist, user_ticket, vip_users, msg, restrict, promo, bot_location, ids

invite = "675f21fcecbfd6b18c0474f3"

# Language system
BOT_LANGUAGE = "tr"  # Default language: Turkish

MESSAGES = {
    "tr": {
        # Play command messages
        "song_processing": "İsteğiniz işleniyor. Sabırlı olun.",
        "ticket_cost_note": "• Not: İstekler 1 bilet tutar. Biletlerinizi boşa harcamayın. İstediğiniz şarkı bulunamazsa biletiniz iade edilecektir.",
        "song_added": "🎵 {title}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• ({duration}) sıraya eklendi\n (@{user} tarafından istendi)",
        "song_failed": "Şarkınız eklenemedi. Zaten sırada olan şarkıyı tekrar istememek ve 8 dakikadan uzun şarkı istememek için dikkat edin.",
        "ticket_refunded": "Biletiniz cüzdanınıza iade edildi. Tekrar deneyin.",
        "song_already_queued": "Şarkı zaten sırada.",
        "no_tickets": "Yeterli biletiniz yok.",
        "check_prices": "Fiyat listesini görmek için /rlist yazın.",
        "vip_limit": "VIP kullanıcılar maksimum 2 şarkıyı aynı anda çalabilir. Mevcut şarkınız bitene kadar bekleyin.",
        "user_limit": "Aynı anda sadece 1 şarkı çalabilirsiniz. Mevcut şarkınız bitene kadar bekleyin.",
        "song_banned": "Bu şarkı yasaklandı. Biletiniz iade edildi.",
        "specify_song": "Lütfen /play komutundan sonra bir şarkı adı belirtin.",
        "links_not_supported": "Linkler şu anda desteklenmiyor, şarkı - sanatçı olarak ekleyin.",
        "no_playlists": "\n Playlist ekleyemezsiniz. Tek seferde bir şarkı isteyin",
        
        # Wallet and tickets
        "remaining_tickets": "Cüzdanınızda kalan bilet: {tickets}",
        "total_tickets": "Cüzdanınızdaki toplam bilet: {tickets}",
        "wallet_updated_5g": "{username}'ın cüzdanı 5g bahşiş için 2 bilet ile güncellendi.",
        "wallet_updated_10g": "{username}'ın cüzdanı 10g bahşiş için 3 bilet ile güncellendi.",
        "wallet_updated": "{username}'ın cüzdanı {amount}g bahşiş için {tickets} bilet ile güncellendi.",
        "bot_wallet": "Efendim, mevcut bakiyem {gold} altın!",
        "no_access": "Bu komuta erişiminiz yok",
        "min_tip_5g": "Bilet almak için en az 5g bahşiş verin.",
        "already_vip": "Zaten VIP'siniz, bilete ihtiyacınız yok.",
        "vip_extended": "VIP döneminiz uzatıldı. Altın bahşiş için teşekkürler. <3",
        "vip_added": "VIP kullanıcılara eklendiniz. Hata yaşarsanız @Atknz'ye mesaj atın. Keyfini çıkarın <3",
        "vip_note": "\n*NOT*: VIP'iniz {date} tarihinden başladı, gelecek ayın {day}'ından önce VIP'inizi yenilediğinizden emin olun.",
        
        # Bot status and info
        "now_playing": "🎵 Şu anda çalıyor: {title}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {duration}\n (@{user} tarafından istendi)",
        "now_playing_no_user": "🎵 Şu anda çalıyor: {title}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {duration}",
        "no_requests": "Şarkı isteği kalmadı. Şarkı istemek için /play yazın.",
        "bot_position_set": "Bot konumu şuna ayarlandı: {location}",
        "promo_cleared": "Promo listesi temizlendi.",
        "promo_empty": "Promo listesi zaten boş.",
        "operation_cancelled": "İşlem iptal edildi.",
        "bitrate_updated": "Ses bit hızı başarıyla {bitrate} olarak güncellendi.",
        "current_bitrate": "Şu anda {bitrate}bps'de ses akışı yapılıyor.",
        "bitrate_confirm": "{bitrate}'ye değiştirmek istediğinizden emin misiniz?",
        "bitrate_warning": "Bu ses akışını etkileyebilir.\n'yes' onaylamak, 'no' iptal etmek için yazın.",
        "invalid_bitrate": "Geçersiz komut, kullanım: /bitrate [sayı]k\nÖrnek: /bitrate 256k",
        "bot_restarting": "Bot yeniden başlatılıyor...",
        
        # Welcome messages
        "welcome_new": "Odaya hoş geldiniz <3.\nÜcretsiz bilet almak için bu bota /verify yazın. Her şarkı isteği 1 bilet tutar.",
        "welcome_commands": "/play 'şarkı' yazarak şarkı isteyebilirsiniz. Tüm komutlar için /help yazın.",
        "welcome_support": "Bot arızalanırsa @Atknz'ye mesaj atın",
        "welcome_back": "Odaya tekrar hoş geldiniz <3.\nBilet bilginizi kontrol etmek için /wallet yazın. Tüm komutlar için /help yazın.",
        "welcome_old_account": "Odaya hoş geldiniz <3.\nBu bir müzik botu. Fiyat listesi için /rlist, bilet bilginizi kontrol etmek için /wallet, şarkı istemek için /play yazın.",
        "account_verified": "Hesabınız doğrulandı.",
        "free_tickets": "3 ücretsiz bilet aldınız!",
        "account_too_new": "Hesabınız en az 30 günlük olmalı.",
        
        # Error and misc messages
        "error_occurred": "Hata oluştu: {error}. Lütfen @Atknz'yi bilgilendirin",
        "cannot_use_command": "Bu komutu kullanamazsınız.",
        "invalid_format": "Geçersiz format. Kullanım: {usage}",
        "language_changed": "Bot dili Türkçe olarak değiştirildi.",
        "only_owner_command": "Bu komut sadece bot sahibi tarafından kullanılabilir."
    },
    "eng": {
        # Play command messages
        "song_processing": "Your request is being processed. Please be patient.",
        "ticket_cost_note": "• Note: Requests cost 1 ticket. Don't waste your tickets. If your requested song is not found, your ticket will be refunded.",
        "song_added": "🎵 {title}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• ({duration}) added to queue\n (requested by @{user})",
        "song_failed": "Your song could not be added. Please avoid requesting songs already in queue and songs longer than 8 minutes.",
        "ticket_refunded": "Your ticket has been refunded to your wallet. Please try again.",
        "song_already_queued": "Song is already in queue.",
        "no_tickets": "You don't have enough tickets.",
        "check_prices": "Type /rlist to see price list.",
        "vip_limit": "VIP users can play maximum 2 songs simultaneously. Wait until your current song finishes.",
        "user_limit": "You can only play 1 song at a time. Wait until your current song finishes.",
        "song_banned": "This song is banned. Your ticket has been refunded.",
        "specify_song": "Please specify a song name after /play command.",
        "links_not_supported": "Links are not currently supported, add as song - artist.",
        "no_playlists": "\n You cannot add playlists. Request one song at a time",
        
        # Wallet and tickets
        "remaining_tickets": "Tickets remaining in your wallet: {tickets}",
        "total_tickets": "Total tickets in your wallet: {tickets}",
        "wallet_updated_5g": "{username}'s wallet updated with 2 tickets for 5g tip.",
        "wallet_updated_10g": "{username}'s wallet updated with 3 tickets for 10g tip.",
        "wallet_updated": "{username}'s wallet updated with {tickets} tickets for {amount}g tip.",
        "bot_wallet": "Sir, my current balance is {gold} gold!",
        "no_access": "You cannot access this command",
        "min_tip_5g": "Give at least 5g tip to buy tickets.",
        "already_vip": "You are already VIP, you don't need tickets.",
        "vip_extended": "Your VIP period has been extended. Thanks for the gold tip. <3",
        "vip_added": "You have been added to VIP users. If you experience any issues, message @Atknz. Enjoy <3",
        "vip_note": "\n*NOTE*: Your VIP started on {date}, make sure to renew your VIP before the {day} of next month.",
        
        # Bot status and info
        "now_playing": "🎵 Now playing: {title}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {duration}\n (requested by @{user})",
        "now_playing_no_user": "🎵 Now playing: {title}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {duration}",
        "no_requests": "No song requests left. Type /play to request a song.",
        "bot_position_set": "Bot position set to: {location}",
        "promo_cleared": "Promo list cleared.",
        "promo_empty": "Promo list is already empty.",
        "operation_cancelled": "Operation cancelled.",
        "bitrate_updated": "Audio bitrate successfully updated to {bitrate}.",
        "current_bitrate": "Currently streaming audio at {bitrate}bps.",
        "bitrate_confirm": "Are you sure you want to change audio bitrate to {bitrate}?",
        "bitrate_warning": "This may affect the audio stream.\nType 'yes' to confirm, 'no' to cancel.",
        "invalid_bitrate": "Invalid command, usage: /bitrate [number]k\nExample: /bitrate 256k",
        "bot_restarting": "Bot is restarting...",
        
        # Welcome messages
        "welcome_new": "Welcome to the room <3.\nType /verify to this bot to get free tickets. Each song request costs 1 ticket.",
        "welcome_commands": "Type /play 'song' to request a song. Type /help for all commands.",
        "welcome_support": "If the bot malfunctions, message @Atknz",
        "welcome_back": "Welcome back to the room <3.\nType /wallet to check your ticket info. Type /help for all commands.",
        "welcome_old_account": "Welcome to the room <3.\nThis is a music bot. Type /rlist for price list, each song request costs 1 ticket. Type /wallet to check your ticket info. Type /play to request a song.",
        "account_verified": "Your account has been verified.",
        "free_tickets": "You received 3 free tickets!",
        "account_too_new": "Your account must be at least 30 days old.",
        
        # Error and misc messages
        "error_occurred": "Error occurred: {error}. Please inform @Atknz",
        "cannot_use_command": "You cannot use this command.",
        "invalid_format": "Invalid format. Usage: {usage}",
        "language_changed": "Bot language changed to English.",
        "only_owner_command": "This command can only be used by the bot owner."
    }
}

def get_message(key, **kwargs):
    """Get localized message"""
    return MESSAGES[BOT_LANGUAGE][key].format(**kwargs)

# Icecast server configuration - Zeno.fm settings
SERVER_HOST = "link.zeno.fm" # dont change.
SERVER_PORT = 80 # dont change
MOUNT_POINT = "/wrmddxrooeyvv" # mount point from your settings
STREAM_USERNAME = "source" # dont change
STREAM_PASSWORD = "dIL0u18k" # your mount password from settings

AUDIO_FILES = [
    "Nothing.mp3"
]

# Check if audio files exist, if not create a simple fallback
import os
if not os.path.exists("Nothing.mp3"):
    # Create a simple text file as placeholder for now
    with open("Nothing.mp3", "w") as f:
        f.write("# Placeholder audio file - replace with actual MP3")

# BotDefinition imported from highrise

class SEA(BaseBot):
    def __init__(self):
        super().__init__()
        self.message_task = None
        self.notification_task = None
        self.promo_task = None
        self.username = None
        self.owner_id = None
        self.owner = None
        self.bot_id = None
        self.skip = False
        self.bitrate = '128k'
        self.choices = {}
        self.req_files = deque()
        self.now = deque()
        self.message = deque()
        self.wait = []
        self.state_file = "bot_state.json"
        self.req_files_dir = "./reqfiles"
        self.fav_dir = "./fav"
        self.room_id = None  # To store Room ID
        os.makedirs(self.fav_dir, exist_ok=True)
        os.makedirs(self.req_files_dir, exist_ok=True)
        self.load_state()

        self.dance_loop_running = False

    def count_user_songs_in_queue(self, username):
        """Calculate user's song count in queue"""
        count = 0
        for song in self.req_files:
            if song.get('user') == username:
                count += 1
        return count

    def save_state(self):
        """Save the current state of the req_files deque, with updated file paths."""
        try:
            data = {
                "req_files": [
                    {
                        "title": item["title"],
                        "url": item["url"],
                        "duration": item["duration"],
                        "user": item["user"]
                    }
                    for item in self.req_files
                ]
            }
            with open(self.state_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving state: {type(e).__name__} - {e}")

    def load_state(self):
        """Load the saved state of the req_files deque from a JSON file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    self.req_files = deque(data.get("req_files", []))
                    os.remove(self.state_file)
            except Exception as e:
                print(f"Error loading state: {type(e).__name__} - {e}")

    def move_files_and_update_urls(self):
        for item in self.req_files:
            if item["url"].startswith("/tmp/"):
                temp_file_path = item["url"]
                new_file_path = os.path.join(self.req_files_dir, os.path.basename(temp_file_path))

                try:
                    shutil.move(temp_file_path, new_file_path)
                    item["url"] = new_file_path
                except Exception as e:
                    print(f"Error moving file {temp_file_path} to {new_file_path}: {type(e).__name__} - {e}")

    async def restart_bot(self):
        self.move_files_and_update_urls()
        self.save_state()
        await asyncio.sleep(5)
        os.execv(sys.executable, [sys.executable, 'run.py'] + sys.argv[1:])


    async def _dance_loop(self):
        """ تشغيل حلقة الرقص مع إعادة المحاولة عند فشل الاتصال """
        while self.dance_loop_running:
            try:
                await self.highrise.send_emote("emote-hyped")
                await asyncio.sleep(7.3)
            except Exception as e:
                break  # إذا كان الخطأ غير متوقع، نوقف الحلقة

    async def on_start(self, session_metadata: SessionMetadata):
        try:
            self.username = await self.get_username(session_metadata.user_id)
            self.bot_id = session_metadata.user_id
            self.owner_id = session_metadata.room_info.owner_id
            self.owner = await self.get_username(self.owner_id)
        except Exception as e:
            print("Error in get username, and bot id on start:", e)

        if not (self.owner is None):
            if self.owner not in ownerz:
                ownerz.append(self.owner)
            else:
                pass
        else:
            pass

        if not (self.owner_id is None):
            if self.owner_id not in msg:
                msg.append(self.owner_id)
            else:
                pass
        else:
            pass

        if bot_location:
            await self.highrise.teleport(session_metadata.user_id, Position(**bot_location))
            # تشغيل حلقة الرقص
            self.dance_loop_running = True
            self.dance_loop_task = asyncio.create_task(self._dance_loop())
        else:
            await self.highrise.teleport(session_metadata.user_id, Position(15.5, 0.25, 2.5, 'FrontRight'))
            # تشغيل حلقة الرقص
            self.dance_loop_running = True
            self.dance_loop_task = asyncio.create_task(self._dance_loop())

        if self.notification_task is None or self.notification_task.done():
            self.notification_task = asyncio.create_task(self.notification())
        else:
            pass

        if self.message_task is None or self.message_task.done():
            self.message_task = asyncio.create_task(self.print_messages())

        if self.promo_task is None or self.promo_task.done():
            self.promo_task = asyncio.create_task(self.promo())
        print(f"{self.username} is alive.")

    async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
        try:
            response = await self.highrise.get_messages(conversation_id)
            if isinstance(response, GetMessagesRequest.GetMessagesResponse):
                message = response.messages[0].content
                if message != "/verify":
                    if user_id not in ids:
                        ids.append(user_id)
                    return
            username = await self.get_username(user_id)
            info = await self.webapi.get_user(user_id)
            joined_at = info.user.joined_at
            if isinstance(joined_at, datetime):
                one_month_ago = datetime.now(joined_at.tzinfo) - timedelta(days=30)
                if joined_at <= one_month_ago:
                    if not username in user_ticket:
                        user_ticket[username] = 3
                        await self.highrise.send_message(conversation_id, "Your account has been verified.")
                        await self.highrise.send_message(conversation_id, "You received 3 free tickets!")
                        if not user_id in ids:
                            ids.append(user_id)
                else:
                    await self.highrise.send_message(conversation_id, "Your account must be at least 30 days old.")
        except Exception as e:
            print(e)

    async def get_username(self, user_id):
        user_info = await self.webapi.get_user(user_id)
        return user_info.user.username

    async def invite_all(self, user):
        if not user.username in ownerz:
            await self.highrise.send_whisper(user.id, "You cannot use this command.")
            return
        try:
            # Automatically get Room ID
            invite_room = self.room_id if self.room_id else "675f21fcecbfd6b18c0474f3"
            for erm in ids:
                message_id = f"1_on_1:{erm}:{self.bot_id}"
                await self.highrise.send_message(
                    message_id,
                    message_type="invite",
                    content="Join this room!", 
                    room_id=invite_room)
                await asyncio.sleep(3)
        except Exception as e:
            await self.highrise.chat(f"Hata: {e}")

    async def color(self: BaseBot, category: str, color_palette: int):
        outfit = (await self.highrise.get_my_outfit()).outfit
        for outfit_item in outfit:
            item_category = outfit_item.id.split("-")[0]
            if item_category == category:
                try:
                    outfit_item.active_palette = color_palette
                except:
                    await self.highrise.chat(f"Bot is not wearing any items from '{category}' category.")
                    return
        await self.highrise.set_outfit(outfit)

    async def equip(self, item_name: str):
        items = (await self.webapi.get_items(item_name=item_name)).items
        if not items:
            await self.highrise.chat(f"Item '{item_name}' not found.")
            return

        item = items[0]
        item_id, category = item.item_id, item.category

        inventory = (await self.highrise.get_inventory()).items
        has_item = any(inv_item.id == item_id for inv_item in inventory)

        if not has_item:
            if item.rarity == Rarity.NONE:
                pass
            elif not item.is_purchasable:
                await self.highrise.chat(f"Item '{item_name}' cannot be purchased.")
                return
            else:
                try:
                    response = await self.highrise.buy_item(item_id)
                    if response != "success":
                        await self.highrise.chat(f"Failed to purchase item '{item_name}'.")
                        return
                    await self.highrise.chat(f"Item '{item_name}' purchased successfully.")
                except Exception as e:
                    await self.highrise.chat(f"Error purchasing '{item_name}': {e}")
                    return

        new_item = Item(
            type="clothing",
            amount=1,
            id=item_id,
            account_bound=False,
            active_palette=0,
        )

        outfit = (await self.highrise.get_my_outfit()).outfit
        outfit = [
            outfit_item
            for outfit_item in outfit
            if outfit_item.id.split("-")[0][0:4] != category[0:4]
        ]

        if category == "hair_front" and item.link_ids:
            hair_back_id = item.link_ids[0]
            hair_back = Item(
                type="clothing",
                amount=1,
                id=hair_back_id,
                account_bound=False,
                active_palette=0,
            )
            outfit.append(hair_back)
        outfit.append(new_item)
        await self.highrise.set_outfit(outfit)
    async def remove(self: BaseBot, category: str):
        outfit = (await self.highrise.get_my_outfit()).outfit

        for outfit_item in outfit:
            item_category = outfit_item.id.split("-")[0][0:3]
            if item_category == category[0:3]:
                try:
                    outfit.remove(outfit_item)
                except Exception as e:
                     pass
                     return
            await self.highrise.set_outfit(outfit)

    async def on_chat(self, user: User, message: str):
        if message.startswith("/remove"):
            if not user.username in ownerz:
                return
            try:
                parts = message.split()
                if len(parts) == 2:
                    _, category = parts
                    await self.remove(category)
                else:
                    await self.highrise.send_whisper(user.id, "Invalid format. Usage: /remove [item_name]")
            except:
                pass

        if message.startswith("/equip"):
            if not user.username in ownerz:
                return
            try:
                parts = message.split()
                if len(message.split()) >= 2:
                    item_name = message.split(maxsplit=1)[1].strip()  # Get everything after /equip
                    await self.equip(item_name)
                else:
                    await self.highrise.send_whisper(user.id, "Invalid format. Usage: /equip [item_name]")
            except:
                pass

        if message.startswith("/color"):
            if not user.username in ownerz:
                return
            parts = message.split()
            if len(parts) == 3:
                _, category, color_palette = parts
                try:
                    color_palette = int(color_palette)  # Convert to integer
                    await self.color(category, color_palette)
                except ValueError:
                    await self.highrise.send_whisper(user.id, "Color palette must be a number.")
            else:
                await self.highrise.send_whisper(user.id, "Invalid format. Usage: /color [category] [palette_number]")

        if message.startswith("/invite"):
            try:
                await self.invite_all(user)
            except Exception as e:
                await self.highrise.chat(f"Sorun: {e}")
        if not message.lower() == "no":
            if not message.lower() == "yes":
                if user.username in self.choices:
                    try:
                        if not user.username in self.wait:
                            self.wait.append(user.username)
                            await self.highrise.send_whisper(user.id, "Type 'yes' or 'no' to apply changes.")
                            await self.highrise.send_whisper(user.id, "If you don't respond with 'yes' or 'no' within 10 seconds, the operation will be canceled.")
                        await asyncio.sleep(10)
                        if user.username in self.choices:
                            del self.choices[user.username]
                            if user.username in self.wait:
                                self.wait.remove(user.username)
                            await self.highrise.send_whisper(user.id, "Operation canceled.")
                    except:
                        pass

        if message.lower() == "no":
            if user.username == "Atknz" or user.username in ownerz:
                if user.username in self.choices:
                    await self.highrise.send_whisper(user.id, "Operation cancelled.")
                    del self.choices[user.username]

        if message.lower() == "yes":
            if user.username == "Atknz" or user.username in ownerz:
                if user.username in self.choices:
                    new_bitrate = self.choices[user.username]
                    self.bitrate = new_bitrate
                    await self.highrise.chat(f"Audio bitrate successfully updated to {new_bitrate}.")
                    del self.choices[user.username]

        if message.startswith("/cbit") and (user.username == "Atknz" or user.username in ownerz):
            await self.highrise.send_whisper(user.id, f"Currently streaming audio at {self.bitrate}bps.")

        if message.startswith("/bitrate ") and (user.username == "Atknz" or user.username in ownerz):
            parts = message.split(" ")
            if len(parts) > 1:
                if parts[1].endswith("k") and parts[1][:-1].isdigit():
                    bitrate = parts[1]
                    await self.highrise.chat(f"Are you sure you want to change audio bitrate to {bitrate}?")
                    await self.highrise.send_whisper(user.id, "This may affect the audio stream.\n"
"Type 'yes' to confirm, 'no' to cancel.")
                    self.choices[user.username] = bitrate
                else:
                    await self.highrise.send_whisper(user.id, "Invalid command, usage: /bitrate [number]k\nExample: /bitrate 256k")
            else:
                await self.highrise.send_whisper(user.id, "Invalid command, usage: /bitrate [number]k\nExample: /bitrate 128k")

        if message.startswith("/setlang ") and (user.username == "Atknz" or user.username in ownerz):
            try:
                parts = message.split(" ", 1)
                if len(parts) == 2:
                    lang_code = parts[1].lower()
                    global BOT_LANGUAGE
                    if lang_code == "tr":
                        BOT_LANGUAGE = "tr"
                        await self.highrise.chat(get_message("language_changed"))
                    elif lang_code == "eng":
                        BOT_LANGUAGE = "eng"
                        await self.highrise.chat(get_message("language_changed"))
                    else:
                        await self.highrise.send_whisper(user.id, "Usage: /setlang tr or /setlang eng")
                else:
                    await self.highrise.send_whisper(user.id, "Usage: /setlang tr or /setlang eng")
            except Exception as e:
                print(f"Error in /setlang command: {e}")

        if message == "/restart" and (user.username == "Atknz" or user.username in ownerz):
            try:
                await self.highrise.send_whisper(user.id, get_message("bot_restarting"))
                await self.restart_bot()
            except Exception as e:
                print("Error in /restart command: ", e)

        if message.startswith("/help"):
            try:
                await self.highrise.send_whisper(user.id,"\nAVAILABLE COMMANDS:\n/play <song name> or /play <youtube url> - Play song.\n/next - Show next song.\n/skip - Skip current song.\n/skip [number] - Skip song in queue.")
                await asyncio.sleep(3)
                await self.highrise.send_whisper(user.id, "\n/now - Show currently playing song\n"
                                    "/dump [number] - Get song info from queue\n"
                                    "/wallet - View your ticket balance.\n"
                                    "/give @user [number] - Give tickets to user.")
                await asyncio.sleep(1)
                await self.highrise.send_whisper(user.id, "\n/rlist - View ticket price list.\n/info @user - Get user's ticket information.\n/fav - Add to favorite playlist.\n/rfav [number] - Remove from favorite playlist.\n/flist - Show favorite playlist.")
                await asyncio.sleep(1)
                await self.highrise.send_whisper(user.id, "\n/cfav - Clear favorite playlist.\n/transfer @user [number] - Transfer your tickets to user (min 6 tickets)") 
                return
            except:
                pass

        if message.startswith("/ahelp") and user.username in ownerz:
            try:
                await self.highrise.send_whisper(user.id,"\nADMIN COMMANDS:\n/add @user - Add user to owners\n/rem @user - Remove user from owners\n/addv @user - Add user to VIP\n/remv @user - Remove user from VIP")
                await asyncio.sleep(3)
                await self.highrise.send_whisper(user.id, "\n/give @user [number] - Give tickets to user\n/info @user - Check user's tickets\n/res [song] - Ban a song\n/unres [song] - Unban a song")
                await asyncio.sleep(1)
                await self.highrise.send_whisper(user.id, "\n/promo [message] - Add promo message\n/rpromo [message] - Remove promo message\n/cpromo - Clear all promo messages\n/msg @user - Add user to message list\n/rmsg @user - Remove user from message list")
                await asyncio.sleep(1)
                await self.highrise.send_whisper(user.id, "\n/cmsg - Clear message list\n/vipz - List all VIP users\n/accs - Account statistics\n/withdraw [amount] - Withdraw gold\n/bwallet - Check bot wallet")
                await asyncio.sleep(1)
                await self.highrise.send_whisper(user.id, "\n/setbot - Set bot position\n/base - Move bot to set position\n/bitrate [number]k - Change audio bitrate\n/cbit - Check current bitrate\n/restart - Restart bot")
                await asyncio.sleep(1)
                await self.highrise.send_whisper(user.id, "\n/equip [item] - Equip item\n/remove [category] - Remove item category\n/color [category] [palette] - Change item color\n/invite - Invite all users\n/fav - Add current song to favorites\n/rfav [number] - Remove from favorites\n/cfav - Clear favorites")
                return
            except:
                pass

        if message.startswith("/play"):
            if (user.username in vip_users) or (user.username in user_ticket and user_ticket[user.username] > 0) or (user.username in ownerz):
                try:
                    # Song limit check
                    user_songs_count = self.count_user_songs_in_queue(user.username)
                    
                    if user.username in ownerz:
                        # Unlimited for owners
                        pass
                    elif user.username in vip_users:
                        # Maximum 2 songs for VIPs
                        if user_songs_count >= 2:
                            await self.highrise.send_whisper(user.id, get_message("vip_limit"))
                            return
                    else:
                        # Maximum 1 song for normal users
                        if user_songs_count >= 1:
                            await self.highrise.send_whisper(user.id, get_message("user_limit"))
                            return
                    
                    query = message.split(" ", 1)[1]
                    lower_query = query.lower()
                    for item in restrict:
                        if item.lower() in lower_query:
                            await self.highrise.send_whisper(user.id, get_message("song_banned"))
                            return
                    if query.startswith("https://"):
                        if "playlist" not in query:
                            await self.highrise.send_whisper(user.id, get_message("links_not_supported"))
                            return
                            await self.highrise.send_whisper(user.id, get_message("song_processing"))
                            if user.username in user_ticket:
                                if user.username not in ownerz and user.username not in vip_users:
                                    await asyncio.sleep(1)
                                    await self.highrise.send_whisper(user.id, get_message("ticket_cost_note"))
                            await self.add_to_queue(query, user)
                        else:
                            await self.highrise.send_whisper(user.id, get_message("no_playlists"))
                    else:
                        await self.highrise.send_whisper(user.id, get_message("song_processing"))
                        if user.username in user_ticket and user.username not in ownerz and user.username not in vip_users:
                            await asyncio.sleep(1)
                            await self.highrise.send_whisper(user.id, get_message("ticket_cost_note"))
                        await self.add_to_queue(query, user)
                except IndexError:
                    await self.highrise.send_whisper(user.id, get_message("specify_song"))
                except Exception as e:
                    print(f"Error in chat command: {e}")
            else:
                await self.highrise.send_whisper(user.id, get_message("no_tickets"))
                await asyncio.sleep(3)
                await self.highrise.send_whisper(user.id, get_message("check_prices"))

        if message.startswith("/rlist"):
            try:
                await self.highrise.send_whisper(user.id, f"\n • Note: Tip @{self.username} in the room,\n • 1 ticket costs 5g\n • 3 tickets cost 10g\n • 30 tickets cost 100g, etc.")
                await asyncio.sleep(2)
                await self.highrise.send_whisper(user.id, f"\n*NOTE*: You can become VIP by tipping 1k to @{self.username} in the room.")
                await asyncio.sleep(2)
                await self.highrise.send_whisper(user.id, "VIP users can request songs without tickets. VIP users must renew their VIP membership every month.")
            except Exception as e:
                print("Error in rlist:", e)

        if message.startswith("/dump "):
            try:
                index_str = message.split("/dump ")[1]
                index = int(index_str)
                if self.now and self.now[0]['url'] in self.req_files:
                    index -= 1
                if 0 <= index < len(self.req_files):
                    file_info = self.req_files[index]
                    now = file_info['title']
                    audio_length = file_info['duration']
                    if file_info.get('user'):
                        await self.highrise.send_whisper(
                            user.id,
                            f"🎵 {index + 1}: {now}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {audio_length}\n (requested by @{file_info['user']})"
                        )
                    else:
                        await self.highrise.send_whisper(
                            user.id,
                            f"🎵 {now}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {audio_length}"
                        )
                else:
                    await self.highrise.send_whisper(user.id, f"Song number {index} not found in queue.")
            except ValueError:
                await self.highrise.send_whisper(user.id, "Invalid index format. Please provide a valid number after /dump command.")
            except Exception as e:
                print(f"Error in /dump command: {e}")
                await self.highrise.send_whisper(user.id, "Error occurred while processing request.")

        if message.startswith("/now"):
            try:
                if not self.now:
                    await self.highrise.send_whisper(user.id, "Nothing is currently playing.")
                    return
                    
                now_playing = self.now[0]
                now = self.now[0]['title']
                if self.now[0]['user']:
                    await self.highrise.send_whisper(user.id, f"🎵 Now playing: {now}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {self.now[0]['audio_length']}\n (@{now_playing['user']} requested)")
                else:
                    await self.highrise.send_whisper(user.id, f"🎵 Now playing: {now}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {self.now[0]['audio_length']}")
            except IndexError:
                await self.highrise.send_whisper(user.id, "Nothing is currently playing.")
            except Exception as e:
                print(f"Error in /now command: {e}")
                await self.highrise.send_whisper(user.id, "Error occurred while processing request.")

        if message.startswith("/wallet"):
            try:
                if user.username in user_ticket:
                    if user_ticket[user.username] == 0:
                        await self.highrise.send_whisper(user.id, f"No tickets left in your wallet. Tip @{self.username} to get tickets.")
                        return
                    if user_ticket[user.username] == 1:
                        await self.highrise.send_whisper(user.id, f"Only {user_ticket[user.username]} ticket left in your wallet.")
                        return
                    await self.highrise.send_whisper(user.id, f"Total tickets in your wallet: {user_ticket[user.username]}.")
                else:
                    await self.highrise.send_whisper(user.id, "Send a private message to this bot to get 3 free tickets.")
            except Exception as e:
                print("The error occurred in wallet:", e)

        if message.startswith("/next"):
            try: 
                if len(self.req_files) > 1:
                    next_file = self.req_files[1]
                    audio_length = (next_file['duration'])
                    next = next_file['title']
                    if next_file['user']:
                        await self.highrise.send_whisper(user.id, f"🎵 Next song: {next}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {audio_length}\n (@{next_file['user']} requested)")
                    else:
                        await self.highrise.send_whisper(user.id, f"🎵 Next song: {next}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {audio_length}")
                else: 
                    await self.highrise.send_whisper(user.id, "No more songs in queue")
            except Exception as e: 
                    print(f"Error in /next command: {e}") 
                    await self.highrise.send_whisper(user.id, "Error checking queue")

        

        if message.startswith("/skip"):
            try:    
                parts = message.split(" ")
                if len(parts) > 1 and parts[1].isdigit():
                    if int(parts[1]) == 0:
                        return
                    index = int(parts[1]) - 1

                    if self.now and self.now[0]['url'] in AUDIO_FILES:
                        adjusted_index = index
                    else:
                        adjusted_index = index + 1
                    if 0 <= adjusted_index < len(self.req_files):
                        removed_file = self.req_files[adjusted_index]
                        rem_length = self.req_files[adjusted_index]['duration']
                        req_user = self.req_files[adjusted_index]['user']
                        fix_rem = removed_file['title']
                        if not (user.username in ownerz or user.username == req_user):
                            await self.highrise.send_whisper(user.id, "NOTE: You can only skip songs you requested.")
                            return
                        if os.path.exists(self.req_files[adjusted_index]['url']):
                            os.remove(self.req_files[adjusted_index]['url'])
                        self.req_files.remove(removed_file)

                        await self.highrise.chat(f"🎵 Removed from queue: {fix_rem}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {rem_length}")
                    else: 
                        await self.highrise.send_whisper(user.id, f"Song number {get_ordinal(index + 1)} not found in queue.") 
                else:
                    if not self.now:
                        await self.highrise.send_whisper(user.id, "Nothing is currently playing.")
                        return
                    rem_length = self.now[0]['audio_length']
                    removed_file = self.now[0]
                    req_user = self.now[0]['user']
                    fix_rem = removed_file['title']
                    if not (user.username in ownerz or user.username == req_user):
                        await self.highrise.send_whisper(user.id, "NOTE: You can only skip your own requested song.")
                        return
                    await self.highrise.chat(f"🎵 Skipping {fix_rem}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {rem_length}")
                    await asyncio.sleep(3)
                    self.skip = True
            except Exception as e:
                print(f"Error in /skip command: {e}")
                await self.highrise.send_whisper(user.id, "Hiçbir şey çalmıyor.")

        if message.startswith("/queue"): 
            try:
                if len(self.req_files) > 0:
                    if self.now and self.now[0]['url'] not in AUDIO_FILES:
                        global_index = 1
                    else:
                        global_index = 0

                    if len(self.req_files) == 1 and global_index == 1:
                        await self.highrise.send_whisper(user.id, "Queue is empty.")
                        return

                    message_content = ""
                    queue_number = 1

                    for _, file in enumerate(list(self.req_files)[global_index:], start=global_index):
                        if file['user']:
                            item = f"{queue_number}. 🎵 {file['title']}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {file['duration']}\n (@{file['user']} requested)\n\n"
                        else:
                            item = f"{queue_number}. 🎵 {file['title']}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {file['duration']}\n\n"
                        
                        if len(message_content) + len(item) > 255:
                            await self.highrise.send_whisper(user.id, f"{message_content.strip()}")
                            message_content = item
                        else:
                            message_content += item
                        queue_number += 1

                    if message_content:
                        await self.highrise.send_whisper(user.id, f"{message_content.strip()}")
                else:
                    await self.highrise.send_whisper(user.id, "Queue is empty.")
            except Exception as e:
                print(f"Error in /queue command: {e}")
                await self.highrise.send_whisper(user.id, "Error checking queue.")

        if message.startswith("/info ") and (user.username in ownerz or user.username == "Atknz"):
            try:
                info = message.split(" ", 1)[1]
                infol = info.replace("@", "")
                if infol in user_ticket and user_ticket[infol] > 0:
                    if user_ticket[infol] == 1:
                        await self.highrise.chat(f"User {info} has only {user_ticket[infol]} ticket.")
                    if user_ticket[infol] > 1:
                        await self.highrise.chat(f"User {info} has only {user_ticket[infol]} ticket.")
                else:
                    await self.highrise.chat(f"User {info} has no tickets.")
            except Exception as e:
                print(e)

        if message.startswith("/rem ") and user.username in ownerz:
            try:
                remvip = message.split(" ", 1)[1]
                rem = remvip.replace("@", "")
                if rem in ownerz:
                    ownerz.remove(rem)
                    await self.highrise.chat(f"{remvip} removed from owners.")
                else:
                    await self.highrise.send_whisper(user.id, f"{rem} is not among owners.")
            except:
                pass

        if message.startswith("/add ") and user.username in ownerz:
            try:
                vip = message.split(" ", 1)[1]
                allowed = vip.replace("@", "")
                if allowed not in ownerz:
                    ownerz.append(allowed)
                    await self.highrise.chat(f"{vip} added to owners.")
                else:
                    await self.highrise.chat(f"{vip} is already an owner.")
            except:
                await self.highrise.send_whisper(user.id, "No")

        if message.startswith("/vipz") and (user.username in ownerz or user.username == "Atknz"):
            try:
                if vip_users:
                    message_content = ""
                    for idx, user_name in enumerate(vip_users, start=1):
                        item = f"{idx}. {user_name}\n"
                        if len(message_content) + len(item) > 255:
                            await self.highrise.send_whisper(user.id, f"\n{message_content.strip()}")
                            message_content = item
                        else:
                            message_content += item
                    if message_content:
                        await self.highrise.send_whisper(user.id, f"\n{message_content.strip()}")
                else:
                    await self.highrise.send_whisper(user.id, "VIP list is empty.")
            except Exception as e:
                print(f"Error in /vipz command: {e}")
                await self.highrise.send_whisper(user.id, "Error while checking queue.")

        if message.startswith("/remv ") and (user.username in ownerz or user.username == "Atknz"):
            try:
                current_date = datetime.now().strftime("%d/%m/%Y")
                remvip = message.split(" ", 1)[1]
                rem = remvip.replace("@", "")
                if rem in vip_users:
                    vip_users.remove(rem)
                    await self.highrise.chat(f"{remvip} removed from VIP.")
                    for user_id in msg:
                        message_id = f"1_on_1:{user_id}:{self.bot_id}"
                        try:
                            await self.highrise.send_message(message_id, f"User {remvip} removed from VIP on {current_date}, removed by @{user.username}")
                            await asyncio.sleep(1)
                        except Exception as e:
                            await self.highrise.chat(f"Could not send message to {user_id}: {e}")
                            print("Error in sending msg in /addv:", e)
                else:
                    await self.highrise.send_whisper(user.id, f"{rem} is not VIP.")
            except:
                pass

        if message.startswith("/addv ") and (user.username in ownerz or user.username == "Atknz"):
            try:
                current_date = datetime.now().strftime("%d/%m/%Y")
                vip = message.split(" ", 1)[1]
                allowed = vip.replace("@", "")
                if allowed not in vip_users:
                    vip_users.append(allowed)
                    await self.highrise.chat(f"{vip} added to VIP.")
                    for user_id in msg:
                        message_id = f"1_on_1:{user_id}:{self.bot_id}"
                        try:
                            await self.highrise.send_message(message_id, f"User {vip} became VIP on {current_date}, added by @{user.username}")
                            await asyncio.sleep(1)
                        except Exception as e:
                            await self.highrise.chat(f"Could not send message to {user_id}: {e}")
                            print("Error in sending msg in /addv:", e)
                else:
                    await self.highrise.chat(f"{vip} is already VIP.")
            except:
                await self.highrise.send_whisper(user.id, "No")

        if message.startswith("/transfer"):
            try:
                _, username, value = message.split(" ", 2)
                username = username.strip("@")
                value = int(value)
                if not value >= 6:
                    await self.highrise.send_whisper(user.id, "NOTE: You need to transfer at least 6 tickets.")
                else:
                    if user_ticket[user.username] >= value:
                        user_ticket[username] += value
                        user_ticket[user.username] -= value
                        await self.highrise.chat(f"{value} tickets sent to {username}.")
                    else:
                        await self.highrise.send_whisper(user.id, "You don't have enough tickets")
            except Exception as e:
                print(f"An error occurred: {e}")

        if message.startswith("/give") and (user.username in ownerz or user.username == "Atknz"):
            try:
                _, username, value = message.split(" ", 2)
                username = username.strip("@")
                value = int(value)
                user_ticket[username] += value
                if value == 1:
                    await self.highrise.chat(f"{username}'a {value} bilet gönderildi.")
                    return
                await self.highrise.chat(f"{username}'a {value} bilet gönderildi.")
            except Exception as e:
                print(f"An error occurred: {e}")

        if message.startswith("/rfav ") and (user.username in ownerz or user.username == "Atknz"):
            try:
                parts = message.split(" ")
                if len(parts) > 1 and parts[1].isdigit():
                    index = int(parts[1]) - 1
                    if 0 <= index <= len(playlist):
                        removed_file = playlist[index]
                        rem_length = removed_file.get('audio_length', 'Bilinmeyen süre')
                        fix_rem = removed_file.get('title', 'Bilinmeyen başlık')
                        file_path = removed_file.get('url', '')
                        if file_path and os.path.exists(file_path):
                            os.remove(file_path)
                            playlist.pop(index)

                            await self.highrise.chat(f"🎵 Removed from queue: {fix_rem}\n🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {rem_length}")
                    else:
                        await self.highrise.send_whisper(user.id, f"Song not found at position {get_ordinal(parts[1])} in queue.")
                else:
                    await self.highrise.send_whisper(user.id, "Please provide a valid song number to remove.")
            except Exception as e:
                print(f"Error in /rfav command: {e}")
                await self.highrise.send_whisper(user.id, f"Hata: {e}")

        if message.startswith("/flist"):
            try: 
                if playlist: 
                    message_content = ""
                    for idx, file in enumerate(list(playlist), start=1):
                        item = f"{idx}. {file['title']}\n"
                        if len(message_content) + len(item) > 255:
                            await self.highrise.send_whisper(user.id, f"\n{message_content.strip()}")
                            message_content = item
                        else:
                            message_content += item
                    if message_content:
                        await self.highrise.send_whisper(user.id, f"\n{message_content.strip()}")
                else:
                    await self.highrise.send_whisper(user.id, "Queue is empty.")
            except Exception as e:
                print(f"Error in /flist command: {e}")
                await self.highrise.send_whisper(user.id, "Error while checking queue.")

        if message.startswith("/fav") and (user.username in ownerz or user.username == "Atknz"):
            try:
                if self.now:
                    fav = self.now[0]
                    if any(item['url'] == fav['url'] for item in playlist):
                        await self.highrise.chat(f"{fav['title']} is already in favorite playlist.")
                        return
                    if fav['url'] in AUDIO_FILES:
                        await self.highrise.send_whisper(user.id, "• Note: You can only add requested songs to favorites.")
                    else:
                        permanent_file = f"./fav/{fav['title']}.mp3"
                        try:
                            shutil.copy(fav['url'], permanent_file)
                        except Exception as e:
                            print("Error in /fav copy:", e)
                            return
                        fav['url'] = permanent_file
                        playlist.append(fav)
                        await self.highrise.chat(f"{fav['title']} added to favorite playlist.")
                else:
                    await self.highrise.chat("Nothing is currently playing.")
            except Exception as e:
                print("Error in /fav command:", e)

        if message.startswith("/cfav"):
            if user.username in ownerz or user.username == "Atknz":
                if playlist:
                    for item in playlist:
                        if os.path.exists(item['url']):
                            try:
                                os.remove(item['url'])
                            except:
                                print("Error in /cfav for loop:", e)
                    playlist.clear()
                    await self.highrise.chat("Favorite playlist cleared.")
                else:
                    await self.highrise.chat("Favorite playlist is already empty.")
            else:
                await self.highrise.send_whisper(user.id, "You don't have access to this command.")

        if message.startswith("/cmsg") and (user.username in ownerz or user.username == "Atknz"):
            try:
                if msg:
                    msg.clear()
                    await self.highrise.chat("Message list cleared.")
                else:
                    await self.highrise.chat("Message list is already empty.")
            except:
                print("Error in /cmsg:", e)

        if message.startswith("/rmsg ") and (user.username in ownerz or user.username == "Atknz"):
            try:
                user = message.split(" ", 1)[1]
                username = user.replace("@", "")
                room_users = (await self.highrise.get_room_users()).content
                user_id = None
                for user in room_users:
                    if user[0].username.lower() == username.lower():
                        user_id = user[0].id
                        break
                if user_id is None:
                    await self.highrise.send_whisper(user.id,"User not found in room.")
                    return
                if user_id in msg:
                    msg.remove(user_id)
                    await self.highrise.chat(f"User @{username} removed from message list.")
                else:
                    await self.highrise.chat("User is not in the list.")
            except Exception as e:
                    print("Error in /rmsg:", e)

        if message.startswith("/msg ") and (user.username in ownerz or user.username == "Atknz"):
            try:
                user = message.split(" ", 1)[1]
                username = user.replace("@", "")
                room_users = (await self.highrise.get_room_users()).content
                user_id = None
                for user in room_users:
                    if user[0].username.lower() == username.lower():
                        user_id = user[0].id
                        break
                if user_id is None:
                    await self.highrise.send_whisper(user.id,"User not found in room.")
                    return
                if user_id not in msg:
                    msg.append(user_id)
                    await self.highrise.chat(f"User @{username} added to message list.")
                else:
                    await self.highrise.chat("User is already in the list.")
            except Exception as e:
                    print("Error in /msg:", e)

        if message.startswith("/res ") and user.username in ownerz:
            try:    
                res = message.split(" ", 1)[1]
                if not res in restrict:
                    restrict.append(res)
                    await self.highrise.chat("This song has been added to banned songs.")
                else:
                    await self.highrise.chat("This song is already banned.")
            except Exception as e:
                print(f"Error in /restrict command: {e}")

        if message.startswith("/unres ") and user.username in ownerz:
            try:    
                res = message.split(" ", 1)[1]
                if res in restrict:
                    restrict.remove(res)
                    await self.highrise.chat("This song has been removed from the banned songs list.")
                else:
                    await self.highrise.chat("This song is not banned.")
            except Exception as e:
                print(f"Error in /unrestrict command: {e}")

        if message.startswith("/promo ") and user.username in ownerz:
            try:    
                prom = message.lstrip("/promo ").strip()
                if prom:
                    if prom not in promo:
                        promo.append(prom)
                        await self.highrise.chat("This message has been added to promo list.")
                    else:
                        await self.highrise.chat("This message is already in promo list.")
                else:
                    await self.highrise.chat("/promo komutundan sonra bir promosyon mesajı verin.")
            except Exception as e:
                print(f"Error in /promo command: {e}")

        if message.startswith("/rpromo ") and user.username in ownerz:
            try:    
                prom = message.lstrip("/promo ").strip()
                if prom:
                    if prom in promo:
                        promo.remove(prom)
                        await self.highrise.chat("This message has been removed from the promo list.")
                    else:
                        await self.highrise.chat("This message is not in promo list.")
                else:
                    await self.highrise.chat("/promo komutundan sonra bir promosyon mesajı verin.")
            except Exception as e:
                print(f"Error in /rpromo command: {e}")

        if message.startswith("/cpromo"):
            try:
                if user.username == "Atknz" or user.username in ownerz:
                    if promo:
                        promo.clear()
                        await self.highrise.chat("Promo listesi temizlendi.")
                    else:
                        await self.highrise.chat("Promo list is already empty.")
                else:
                    pass
            except:
                pass

        if message.startswith("/accs") and user.username in ownerz:
            try:
                total = len(user_ticket)
                empty = {key: value for key, value in user_ticket.items() if value == 0}
                active = {key: value for key, value in user_ticket.items() if value > 0 and value != 3}
                total_empty = len(empty)
                total_active = len(active)
                await self.highrise.chat(f"\nTotal {total} users, {total_active} active accounts, only {total_empty} users have 0 balance.")
            except Exception as e:
                print("Error in /accs:", e)

        if message.startswith("/withdraw ") and (user.username in ownerz or user.username == "Atknz"):
            try:
                parts = message.split(" ")
                if len(parts) != 2:
                    await self.highrise.send_whisper(user.id, "\nKullanım: /withdraw [numara].")
                    return
                try:
                    amount = int(parts[1])
                except:
                    await self.highrise.send_whisper(user.id, "Ondalık sayılar ve kesirler kullanmayın, sadece tam sayılar [numara].")
                    return
                bot_wallet = await self.highrise.get_wallet()
                bot_amount = bot_wallet.content[0].amount
                if bot_amount <= amount:
                    await self.highrise.send_whisper(user.id, "Sir, I don't have enough balance.")
                    return
                """Possible values are: "gold_bar_1",
            "gold_bar_5", "gold_bar_10", "gold_bar_50", 
            "gold_bar_100", "gold_bar_500", 
            "gold_bar_1k", "gold_bar_5000", "gold_bar_10k" """
                bars_dictionary = {10000: "gold_bar_10k", 
                               5000: "gold_bar_5000",
                               1000: "gold_bar_1k",
                               500: "gold_bar_500",
                               100: "gold_bar_100",
                               50: "gold_bar_50",
                               10: "gold_bar_10",
                               5: "gold_bar_5",
                               1: "gold_bar_1"}
                fees_dictionary = {10000: 1000,
                               5000: 500,
                               1000: 100,
                               500: 50,
                               100: 10,
                               50: 5,
                               10: 1,
                               5: 1,
                               1: 1}
                tip = []
                total = 0
                for bar in bars_dictionary:
                    if amount >= bar:
                        bar_amount = amount // bar
                        amount = amount % bar
                        for i in range(bar_amount):
                            tip.append(bars_dictionary[bar])
                            total = bar+fees_dictionary[bar]
                if total > bot_amount:
                    await self.highrise.send_whisper(user.id, "Sir, I don't have enough funds.")
                    return
                tip_string = ",".join(tip)
                await self.highrise.tip_user(user.id, tip_string)
            except Exception as e:
                print("Error in /withdraw:", e)

        if message == "/setbot" and user.username in ownerz:
            try:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.username == user.username:
                        bot_location["x"] = pos.x
                        bot_location["y"] = pos.y
                        bot_location["z"] = pos.z
                        bot_location["facing"] = pos.facing
                        await self.highrise.send_whisper(user.id, f"Bot konumu şuna ayarlandı: {bot_location}")
                        break
            except Exception as e:
                print("Set bot:", e)

        if message == "/base" and user.username in ownerz:
            try:
                if bot_location:
                    await self.highrise.walk_to(Position(**bot_location))
            except Exception as e:
                print("Error in /base:", e)

        if message.startswith("/bwallet"):
            try:
                await self.bot_wallet(user, message)
            except:
                pass

    async def bot_wallet(self, user: User, message: str):
        if user.username in ownerz or user.username == "Atknz":
            wallet = await self.highrise.get_wallet()
            for item in wallet.content:
                if item.type == "gold":
                    gold = item.amount
                    await self.highrise.send_whisper(user.id, f"Efendim, mevcut bakiyem {gold} altın!")
                    return
            await self.highrise.send_whisper(f"Hello, {user.username}! I have no gold.")
        else:
            await self.highrise.send_whisper(user.id, "Bu komuta erişiminiz yok")

    async def on_user_join(self, user: User, pos: Position) -> None:
        try:
            response = await self.webapi.get_user(user.id)
            joined_at = response.user.joined_at

            if isinstance(joined_at, datetime):
                one_month_ago = datetime.now(joined_at.tzinfo) - timedelta(days=30)
                if joined_at <= one_month_ago:
                    if not user.username in user_ticket:
                        await self.highrise.send_whisper(user.id, "Welcome to the room <3.\nType /verify to this bot to get free tickets. Each song request costs 1 ticket.")
                        await asyncio.sleep(2)
                        await self.highrise.send_whisper(user.id, "Type /play 'song' to request a song. Type /help for all commands.")
                        await asyncio.sleep(1)
                        await self.highrise.send_whisper(user.id, "If the bot malfunctions, message @Atknz")
                    else:
                        await self.highrise.send_whisper(user.id, "Welcome back to the room <3.\nType /wallet to check your ticket info. Type /help for all commands.")
                        await asyncio.sleep(2)
                        await self.highrise.send_whisper(user.id, "If the bot malfunctions, message @Atknz")
                else:
                    await self.highrise.send_whisper(user.id, "Welcome to the room <3.\nThis is a music bot. Type /rlist for price list, each song request costs 1 ticket. Type /wallet to check your ticket info. Type /play to request a song.")
                    await asyncio.sleep(2)
                    await self.highrise.send_whisper(user.id, "If the bot malfunctions, message @Atknz")
            else:
                pass
        except:
            pass

    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
        try:
            if tip.amount == 1 and receiver.username == self.username:
                if sender.username in vip_users:
                    await self.highrise.send_whisper(sender.id, "You are already VIP, you don't need tickets.")
                else:
                    await self.highrise.send_whisper(sender.id, "Bilet almak için en az 5g bahşiş verin.")

            elif tip.amount == 5 and receiver.username == self.username:
                user_ticket[sender.username] = user_ticket.get(sender.username, 0) + 1
                if sender.username in vip_users:
                    await self.highrise.send_whisper(sender.id, "You are already VIP, you don't need tickets.")
                else:
                    await self.highrise.chat(f"{sender.username}'ın cüzdanı 5g bahşiş için 2 bilet ile güncellendi.")
                    await self.highrise.send_whisper(sender.id, f"Cüzdanınızdaki toplam bilet: {user_ticket[sender.username]}")

            elif tip.amount == 10 and receiver.username == self.username:
                user_ticket[sender.username] = user_ticket.get(sender.username, 0) + 3
                if sender.username in vip_users:
                    await self.highrise.send_whisper(sender.id, "You are already VIP, you don't need tickets.")
                else:
                    await self.highrise.chat(f"{sender.username}'ın cüzdanı 10g bahşiş için 3 bilet ile güncellendi.")
                    await self.highrise.send_whisper(sender.id, f"Cüzdanınızdaki toplam bilet: {user_ticket[sender.username]}")

            elif tip.amount == 1000 and receiver.username == self.username:
                current_date = datetime.now().strftime("%d/%m/%Y")
                day = datetime.now().strftime("%d")
                if sender.username in vip_users:
                    await self.highrise.send_whisper(user.id, "VIP döneminiz uzatıldı. Altın bahşiş için teşekkürler. <3")
                    for user_id in msg:
                        message_id = f"1_on_1:{user_id}:{self.bot_id}"
                        try:
                            await self.highrise.send_message(message_id, f"Kullanıcı @{sender.username} {current_date} tarihinde 1000g bahşiş verdi.")
                            await asyncio.sleep(1)
                        except Exception as e:
                            print("Error in sending msg abt tip:", e)

                else:
                    vip_users.append(sender.username)
                    await self.highrise.send_whisper(user.id, get_message("vip_added"))
                    await self.highrise.send_whisper(user.id, f"\n*NOT*: VIP'iniz {current_date} tarihinden başladı, gelecek ayın {get_ordinal(day)}'ından önce VIP'inizi yenilediğinizden emin olun.")
                    for user_id in msg:
                        message_id = f"1_on_1:{user_id}:{self.bot_id}"
                        try:
                            await self.highrise.send_message(message_id, f"Kullanıcı @{sender.username} {current_date} tarihinde VIP oldu.")
                            await asyncio.sleep(1)
                        except Exception as e:
                            print("Error in sending msg abt tip:", e)

            elif tip.amount % 10 == 0 and tip.amount >= 10 and receiver.username == self.username:
                tickets = (tip.amount // 10) * 3
                user_ticket[sender.username] = user_ticket.get(sender.username, 0) + tickets
                await self.highrise.chat(f"{sender.username}'ın cüzdanı {tip.amount}g bahşiş için {tickets} bilet ile güncellendi.")
                await self.highrise.send_whisper(sender.id, f"Cüzdanınızdaki toplam bilet: {user_ticket[sender.username]}")
            else:
                pass
        except Exception as e:
            print(e)
            await self.highrise.send_whisper(sender.id, f"Hata oluştu: {e}. Lütfen @Atknz'yi bilgilendirin")

    async def add_to_queue(self, query, user):
        """Search for a song and add it to the queue using yt-dlp."""
        buffered_file_path, track_duration, track = await self.search_track(query, user)
        if buffered_file_path:
            self.req_files.append({
                'url': buffered_file_path,
                'title': track['title'],
                'uploader': track['uploader'],
                'duration': track_duration,
                'user': user.username,
            })
            await self.highrise.chat(get_message("song_added", title=track["title"], duration=track_duration, user=user.username))
            if user.username in user_ticket:
                if user.username not in ownerz:
                    if user.username not in vip_users:
                        user_ticket[user.username] -= 1
                        await self.highrise.send_whisper(user.id, get_message("remaining_tickets", tickets=user_ticket[user.username]))
        else:
            await asyncio.sleep(2)
            await self.highrise.send_whisper(user.id, get_message("song_failed"))
            await asyncio.sleep(2)
            await self.highrise.send_whisper(user.id, get_message("ticket_refunded"))

    async def download_chunk(self, session, url, start, end, queue):
        headers = {'Range': f'bytes={start}-{end}'}
        async with session.get(url, headers=headers) as response:
            if response.status not in [206, 200]:
                print(f"Failed to download chunk: {response.status}")
                await queue.put(None)
                return

            chunk = await response.content.read()
            await queue.put((start, chunk))

    async def download_audio(self, session, audio_url, download_queue):
        retries = 3
        for attempt in range(retries):
            async with session.head(audio_url) as response:
                if response.status == 302:
                    audio_url = response.headers['Location']
                    continue
                if response.status != 200:
                    print(f"Failed to get audio info: {response.status}")
                    await download_queue.put(None)
                    return
                break
            asyncio.sleep(1)
        else:
            print("Failed to get audio info after retries")
            await download_queue.put(None)
            return

        total_size = int(response.headers.get('Content-Length'))
        chunk_size = total_size // 4  # Download in 4 chunks

        tasks = []
        for i in range(4):
            start = i * chunk_size
            end = (i + 1) * chunk_size - 1 if i != 3 else total_size - 1
            tasks.append(self.download_chunk(session, audio_url, start, end, download_queue))

        await asyncio.gather(*tasks)
        await download_queue.put(None)

    async def write_audio(self, temp_file_path, download_queue, buffer_queue):
        buffer_size = 10 * 1024 * 1024  # 10 MB buffer size

        async with aiofiles.open(temp_file_path, 'wb') as temp_file:
            while True:
                item = await download_queue.get()
                if item is None:
                    break
                start, chunk = item
                await temp_file.seek(start)
                await temp_file.write(chunk)
                await buffer_queue.put(chunk)
                download_queue.task_done()

            await buffer_queue.put(None)

    async def buffer_audio(self, audio_url):
        async with aiohttp.ClientSession() as session:
            try:
                temp_file_path = tempfile.mktemp(suffix='.mp3')
                download_queue = asyncio.Queue()
                buffer_queue = asyncio.Queue()

                download_task = asyncio.create_task(self.download_audio(session, audio_url, download_queue))
                write_task = asyncio.create_task(self.write_audio(temp_file_path, download_queue, buffer_queue))

                await asyncio.sleep(1)
                await asyncio.gather(download_task, write_task)
                return temp_file_path

            except Exception as e:
                print(f"Buffering error: {e}")
                return None

    async def search_track(self, query, user):
        """Search for a track using yt-dlp and buffer the audio."""
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1',
            'max_downloads': 1,
            'match_filter': yt_dlp.utils.match_filter_func('duration > 10 & duration < 480 & view_count > 1000'),  # 8 dakika = 480 saniye
            'extractor_args': {'youtube': {'skip': ['dash', 'hls']}},
        }



        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if query.startswith("http"):
                    info = ydl.extract_info(query, download=False)
                else:
                    info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]

                track_url = info['url']
                track_duration = f"{info['duration'] // 60}:{info['duration'] % 60:02d}"
                track = {
                    "title": info['title'],
                    "uploader": info['uploader']
                }
                for items in self.req_files:
                    if items["title"] == info['title']:
                        await self.highrise.send_whisper(user.id, get_message("song_already_queued"))
                        return None, None, None

                attempts = 0
                while attempts < 3:
                    buffered_file_path = await self.buffer_audio(track_url)
                    if buffered_file_path is None:
                        attempts += 1
                        await asyncio.sleep(1)
                        continue
                    
                    try:
                        file_size = os.path.getsize(buffered_file_path)
                        if file_size >= 4 * 1024:
                            break
                    except FileNotFoundError:
                        attempts += 1
                        await asyncio.sleep(1)
                        continue
                    attempts += 1
                    await asyncio.sleep(1)
                else: # If loop finishes without break
                    if buffered_file_path and os.path.exists(buffered_file_path):
                        os.remove(buffered_file_path) # Clean up if it exists but is too small
                    return None, None, None

                if os.path.getsize(buffered_file_path) >= 4 * 1024:
                    return buffered_file_path, track_duration, track
                else:
                    if buffered_file_path and os.path.exists(buffered_file_path):
                        os.remove(buffered_file_path)
                    return None, None, None
        except Exception as e:
            print(f"Error searching track: {e}")
            return None, None, None

    async def promo(self):
        while True:
            try:
                for items in promo:
                    await self.highrise.chat(items)
                    await asyncio.sleep(100)
                else:
                    await asyncio.sleep(100)
            except:
                pass
            await asyncio.sleep(300)

    async def notification(self):
        while True:
            try:
                if not self.req_files:
                    await self.highrise.chat("Şarkı isteği kalmadı. Şarkı istemek için /play yazın.")
            except:
                pass
            await asyncio.sleep(277)

    async def print_messages(self):
        while True:
            try:
                if self.message:
                    nowplaying = self.message[0]
                    # Nothing.mp3 çalarken mesaj gösterme
                    if nowplaying.get('title') == 'Nothing' or nowplaying.get('url') in AUDIO_FILES:
                        self.message.clear()
                        await asyncio.sleep(5)
                        continue
                        
                    fix_nowplaying = nowplaying['title']
                    if nowplaying['user']:
                        await self.highrise.chat(f"🎵 Şu anda çalıyor: {fix_nowplaying}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {nowplaying['audio_length']}\n (@{nowplaying['user']} tarafından istendi)")
                    else:
                        await self.highrise.chat(f"🎵 Şu anda çalıyor: {fix_nowplaying}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {nowplaying['audio_length']}")
                    self.message.clear()
            except:
                pass
            await asyncio.sleep(5)

    async def run(self, room_id: str, token: str):
        definitions = [BotDefinition(self, room_id, token)]
        await __main__.main(definitions)

    def get_audio_length(self, audio_path):
        try:
            audio = MP3(audio_path)
            length = audio.info.length
            length = max(length, 0)
            minutes = int(length // 60)
            seconds = int(length % 60)
            return f"{minutes}:{seconds:02d}"
        except Exception:
            # Return default length for invalid MP3 files without logging
            return "0:30"

def get_ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

def connect_to_icecast():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
        sock.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to Icecast server.")

        auth = f"source:{STREAM_PASSWORD}"
        headers = (
            f"PUT {MOUNT_POINT} HTTP/1.1\r\n"
            f"Host: {SERVER_HOST}\r\n"
            f"Authorization: Basic {base64.b64encode(auth.encode()).decode()}\r\n"
            f"Content-Type: audio/mpeg\r\n"
            f"User-Agent: Icecast/2.4.0\r\n"
            f"ice-name: ROBINS MUSIC\r\n"
            f"ice-genre: Various\r\n"
            f"ice-url: https://stream.zeno.fm{MOUNT_POINT}\r\n"
            f"ice-public: 1\r\n"
            f"ice-audio-info: bitrate=128000;samplerate=44100;channels=2\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
        sock.sendall(headers.encode('utf-8'))

        response = sock.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

        if "HTTP/1.0 200 OK" in response:
            print("Authentication successful.")
        else:
            print("Unexpected server response. Closing connection.")
            sock.close()
            return None
        return sock
    except Exception as e:
        print(f"Connection error: {e}")
        return None


def start_streaming(bot_instance):
    try:
        while True:
            sock = connect_to_icecast()
            if sock:
                try:
                    while True:
                        audio_file = None
                        
                        # Check for requested songs first
                        if bot_instance.req_files:
                            # Verify file still exists
                            if os.path.exists(bot_instance.req_files[0]['url']):
                                audio_file = bot_instance.req_files[0]['url']
                                print(f"Streaming from queue: {bot_instance.req_files[0]['title']}")
                            else:
                                print(f"Requested file missing: {bot_instance.req_files[0]['url']}")
                                bot_instance.req_files.popleft()
                                continue
                        
                        # Check playlist if no requests
                        elif playlist:
                            available_playlist = [item for item in playlist if os.path.exists(item['url'])]
                            if available_playlist:
                                erm = random.choice(available_playlist)
                                audio_file = erm['url']
                                print(f"Streaming from playlist: {erm['title']}")
                        
                        # Default to Nothing.mp3 when queue is empty
                        if audio_file is None:
                            audio_file = random.choice(AUDIO_FILES)
                            # Don't spam console when playing default audio
                            # print(f"Streaming default audio: {audio_file}")

                        success = stream_audio(sock, audio_file, bot_instance)
                        
                        if bot_instance.skip:
                            bot_instance.skip = False
                            continue
                        
                        if not success:
                            sock.close()
                            break
                        
                        # Longer delay when playing default audio to reduce spam
                        if audio_file in AUDIO_FILES:
                            time.sleep(2)
                        else:
                            time.sleep(0.5)

                except Exception as e:
                    print(f"Error during streaming: {e}")
                    if sock:
                        sock.close()
            else:
                print("Failed to connect to Icecast server.")

            time.sleep(5)
    except Exception as e:
        print(f"Error in start_streaming: {e}")

def stream_audio(sock, audio_file, bot_instance):
    try:
        # Only print for non-default audio files to reduce spam
        if audio_file not in AUDIO_FILES:
            print(f"Streaming audio file: {audio_file}")
        
        # Clear current song info before setting a new one
        bot_instance.now.clear()
        bot_instance.message.clear()

        # Check if file exists first
        if not os.path.exists(audio_file):
            print(f"Audio file not found: {audio_file}")
            return False

        if audio_file in AUDIO_FILES:
            song_title = audio_file.replace(".mp3", "")
            audio_length = bot_instance.get_audio_length(audio_file)
            if audio_length is None:
                audio_length = "0:00"
            bot_instance.now.append({'url': audio_file, 'title': song_title, 'user': None, 'audio_length': audio_length})
            # Nothing.mp3 için mesaj ekleme
            if song_title != "Nothing":
                bot_instance.message.append({'url': audio_file, 'title': song_title, 'user': None, 'audio_length': audio_length})

        elif any(item['url'] == audio_file for item in playlist):
            matching_item = next((item for item in playlist if item['url'] == audio_file), None)
            if matching_item:
                details = {
                    'url': matching_item['url'],
                    'title': matching_item['title'],
                    'user': None,
                    'audio_length': matching_item.get('audio_length', matching_item.get('duration', '0:00'))
                }
                bot_instance.now.append(details)
                bot_instance.message.append(details)

        elif bot_instance.req_files and audio_file == bot_instance.req_files[0]['url']:
            details = {
                'url': bot_instance.req_files[0]['url'],
                'title': bot_instance.req_files[0]['title'],
                'user': bot_instance.req_files[0]['user'],
                'audio_length': bot_instance.req_files[0]['duration']
            }
            bot_instance.now.append(details)
            bot_instance.message.append(details)

        command = [
            './bin/ffmpeg',
            '-re',
            '-i', audio_file,
            '-map', '0:a',
            '-c:a', 'libmp3lame',
            '-ar', '44100',
            '-b:a', bot_instance.bitrate,
            '-f', 'mp3',
            '-content_type', 'audio/mpeg',
            '-buffer_size', '500k',
            '-'
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        
        while True:
            data = process.stdout.read(4096)
            
            if bot_instance.skip:
                if audio_file not in AUDIO_FILES:
                    print(f"Skipping: {audio_file}")
                process.terminate()
                
                # Remove from req_files if it was a requested song
                if bot_instance.req_files and bot_instance.req_files[0]['url'] == audio_file:
                    bot_instance.req_files.popleft()
                
                # Clean up temporary file if it's not a default AUDIO_FILE and not in playlist
                if audio_file not in AUDIO_FILES and not any(item['url'] == audio_file for item in playlist):
                    cleanup_temp_file(bot_instance, audio_file)
                
                return True # Indicate successful skip
                
            if not data:
                process.terminate()
                # Only print for non-default audio files to reduce spam
                if audio_file not in AUDIO_FILES:
                    print(f"Finished streaming: {audio_file}")
                
                # Clean up req_files when song finishes naturally
                if bot_instance.req_files and bot_instance.req_files[0]['url'] == audio_file:
                    bot_instance.req_files.popleft()

                # Clean up temporary file if it's not a default AUDIO_FILE and not in playlist
                if audio_file not in AUDIO_FILES and not any(item['url'] == audio_file for item in playlist):
                    cleanup_temp_file(bot_instance, audio_file)
                
                # Clear now playing info when song ends
                bot_instance.now.clear()
                
                return True # Indicate successful stream completion
            
            try:
                sock.sendall(data)
            except (BrokenPipeError, ConnectionResetError) as e:
                print(f"Connection lost while sending chunk: {e}")
                process.terminate()
                return False # Indicate connection error
            time.sleep(0.05)
            
    except Exception as e:
        print(f"Streaming error: {e}")
        return False # Indicate streaming error

def cleanup_temp_file(bot_instance, temp_file_path):
    """Remove the temporary file from memory."""
    try:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Temporary file removed: {temp_file_path}")
    except Exception as e:
        print(f"Error cleaning up temporary file {temp_file_path}: {e}")
