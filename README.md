# Wazzap Chat

A simple Python-based multi-client chat system with server and client code. Built as a learning project.

## Features
- Broadcast chat messages between clients
- Nickname support with `/nick NAME`
- Works locally and over the internet via Pinggy or ngrok
- Can be analyzed with Wireshark using the custom `wazzap.lua` dissector

## How to Run

### Server
```bash
python3 server.py
```

### Client
Update `HOST` and `PORT` in `client.py` to match the server or tunnel endpoint:
```bash
python3 client.py
```

When you start, you will see:
```
Type messages and press Enter. Use /nick NAME to change your name.
```

## Example Commands
- `/nick Jack` → change your nickname to Jack
- `Hello all` → broadcast to everyone

## Remote Access with Pinggy
1. Start the server on your machine.
2. Run a Pinggy tunnel for port 12345.
3. Copy the public host/port Pinggy provides.
4. Share it with teammates.
5. They set `HOST` and `PORT` in `client.py` and run the client to join the chat.

*Note*: Pinggy gives a new host/port each time you restart it.

## Advanced: Wireshark Protocol Analysis
We created a custom Lua dissector (`wazzap.lua`) to parse the chat protocol.

### Setup
1. Place `wazzap.lua` into your Wireshark plugins folder:
   - macOS: `~/.local/lib/wireshark/plugins/`
   - Confirm in **Wireshark → About → Plugins** that `wazzap.lua` is listed.
2. Restart Wireshark.

### Usage
- Capture on the correct interface (`lo0` for local, Wi-Fi if remote).
- If traffic is on port 12345, it auto-decodes as **WAZZAP**.
- If another port (Pinggy random), right-click → **Decode As…** → Wazzap Chat.

### Fields
- `wazzap.type` → SYS, MSG
- `wazzap.user` → nickname
- `wazzap.text` → message

### Filters
- All packets: `wazzap`
- From Jack: `wazzap.user == "Jack"`

---

This project demonstrates end-to-end chat implementation, remote tunneling, and protocol analysis.
