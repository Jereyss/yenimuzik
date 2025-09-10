

import threading
import asyncio
from youtubezeno import SEA, start_streaming
from highrise import __main__

class BotDefinition:
    def __init__(self, bot, room_id: str, api_token: str):
        self.bot = bot
        room_id = "685fe9208ab075915779c70e"
        self.room_id = room_id
        self.api_token = api_token

async def verify_reminder_task(bot_instance):
    """Disabled verify reminder task"""
    while True:
        await asyncio.sleep(3600)  # Sleep for 1 hour (task disabled)
        # Verify reminder is disabled to prevent spam messages
        pass

async def main():
    room_id = "685fe9208ab075915779c70e"
    token = "de29bb353e3d2be63f50157cb3d6c857bfc6ab46bb21b53451d903e015f76831"    
    bot_instance = SEA()  
    bot_instance.room_id = room_id  # Bot instance'a room_id'yi aktar
    
    # Start the streaming thread
    streaming_thread = threading.Thread(target=start_streaming, args=(bot_instance,))
    streaming_thread.daemon = True
    streaming_thread.start()
    
    # Start verify reminder task
    verify_task = asyncio.create_task(verify_reminder_task(bot_instance))
    
    definitions = [BotDefinition(bot_instance, room_id, token)]
    
    while True:
        try:
            await __main__.main(definitions)
        except Exception as e:
            print(f"Bot error: {e}. Restarting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())

