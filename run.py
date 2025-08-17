import threading
import asyncio
from youtubezeno import SEA, start_streaming

async def main():
    room_id = "6823567c93ff9fd00c8c2b54"
    token = "c58928d2c7f8de6b35cc78f87690814b3dc8707e084a379e139edf7ae4ba66de"    
    bot_instance = SEA()  
    # Start the streaming thread
    streaming_thread = threading.Thread(target=start_streaming, args=(bot_instance,))
    streaming_thread.daemon = True
    streaming_thread.start()
    while True:
        try:
            await asyncio.sleep(5)
            await bot_instance.run(room_id, token)
        except Exception as e:
            print(f"Bot error: {e}. Restarting in 5 seconds...")
            await asyncio.sleep(5)
if __name__ == '__main__':
    asyncio.run(main())