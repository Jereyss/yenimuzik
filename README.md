# Highrise Music Bot

This is a Highrise chatroom bot with live music streaming capabilities using Zeno.fm/Icecast servers.

## Features

- Stream music to Zeno.fm/Icecast servers
- Queue management with numbered display
- VIP user system with special privileges
- Ticket-based song requests
- YouTube music integration
- Admin commands for bot management
- Real-time queue display and management

## Installation

1. Install Python 3.10 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Edit `run.py`:
   - Set your `room_id` 
   - Set your `api_token` from Highrise dashboard

2. Edit `youtubezeno.py`:
   - Configure Icecast server settings (lines 36-40)
   - Set your stream credentials

## Running the Bot

```bash
python run.py
```

## Commands

### User Commands
- `/play <song name>` - Request a song
- `/next` - Show next song in queue
- `/queue` - Show full queue with details
- `/now` - Show currently playing song
- `/skip` - Skip current song (only your own)
- `/wallet` - Check your ticket balance
- `/help` - Show all commands

### Admin Commands
- `/ahelp` - Show admin commands
- `/add @user` - Add user to owners
- `/rem @user` - Remove user from owners
- `/addv @user` - Add user to VIP
- `/give @user [number]` - Give tickets to user
- `/restart` - Restart bot

## Requirements

- Python 3.10+
- Highrise bot API key
- Icecast/Zeno.fm streaming setup
- FFmpeg installed on system

## License

This project is open source.