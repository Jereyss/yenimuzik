
import threading
import asyncio
from youtubezeno import SEA, start_streaming

async def main():
    room_id = "675f21fcecbfd6b18c0474f3"
    token = "de29bb353e3d2be63f50157cb3d6c857bfc6ab46bb21b53451d903e015f76831"    
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
