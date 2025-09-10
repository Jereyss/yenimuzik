# Highrise Music Bot with Live Streaming

## Overview

This is a Highrise chatroom bot that integrates music streaming capabilities using Zeno.fm/Icecast servers. The bot can play music in virtual rooms, manage user permissions through a ticket system, handle VIP users, and maintain playlists. It combines the Highrise Bot SDK for virtual world interactions with audio streaming technology to create an interactive music experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Bot Framework
- **Highrise Bot SDK**: Primary framework for interacting with Highrise virtual rooms
- **Async/Await Pattern**: Handles concurrent operations for bot responses and streaming
- **Event-Driven Architecture**: Responds to user commands and room events in real-time

### Data Storage System
- **JSON-Based Persistence**: Uses local JSON files for data storage with automatic save/load mechanisms
- **File-Based Database**: Stores user tickets, VIP lists, playlists, bot location, and permissions
- **Automatic Backup**: Implements periodic saving every 100 seconds with disk space checking

### Audio Streaming Integration
- **Zeno.fm/Icecast Server**: Streams audio content to external radio platforms
- **FFmpeg Integration**: Handles audio processing and streaming protocol conversion
- **YouTube-dl Integration**: Downloads and processes audio from various sources
- **Fallback Audio System**: Maintains default audio files when no content is available

### User Management System
- **Ticket-Based Permissions**: Users earn/spend tickets for bot interactions
- **VIP User System**: Special privileges for designated users
- **Owner/Admin Hierarchy**: Multi-level permission system for bot management
- **Restriction Management**: Ability to temporarily limit user access

### Threading Architecture
- **Main Bot Thread**: Handles Highrise room interactions and commands
- **Streaming Thread**: Manages continuous audio streaming in background
- **Timer-Based Tasks**: Periodic data saving and maintenance operations
- **Error Recovery**: Automatic restart mechanisms for bot resilience

### Command Processing
- **Real-time Response**: Immediate feedback to user commands in chat
- **Queue Management**: Handles playlist and music request queuing
- **State Management**: Tracks bot location, current playing status, and user interactions

## External Dependencies

### Highrise Platform
- **Highrise Bot SDK**: Official SDK for room interactions and user management
- **Room API**: Real-time communication with virtual rooms and users

### Streaming Services
- **Zeno.fm**: Primary streaming platform for audio broadcast
- **Icecast Protocol**: Industry-standard streaming protocol for audio distribution

### Audio Processing
- **FFmpeg**: Professional audio/video processing and streaming
- **yt-dlp**: YouTube and multi-platform media downloading
- **Mutagen**: Audio metadata extraction and manipulation

### Python Libraries
- **aiohttp/aiofiles**: Asynchronous HTTP operations and file handling
- **Flask**: Web framework for potential API endpoints
- **pendulum**: Advanced date/time handling for scheduling features

### Development Tools
- **Threading**: Built-in Python threading for concurrent operations
- **asyncio**: Asynchronous programming support for real-time interactions
- **JSON**: Data serialization for persistent storage