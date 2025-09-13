
# Wazzap Chat

Simple Python-based multi-client chat server and client.

## Features
- Broadcast chat messages
- Nickname support with `/nick NAME`
- System messages for join/leave
- Works locally and over the internet with Pinggy or ngrok

## How to Run

### Server
```bash
python3 server.py
```

### Client
Edit `client.py` and set HOST/PORT to match server (or Pinggy/ngrok endpoint).
```bash
python3 client.py
```

## Example Commands
- `/nick Alice` → change your nickname
- Just type any text to broadcast

## Remote Access with Pinggy
1. Start the server.
2. Run Pinggy tunnel for port 12345.
3. Share the public host/port with your teammates.
4. They update HOST/PORT in `client.py` and connect.

## Notes
- Every time you restart Pinggy, you get a new host/port.
- Use multiple terminals or PCs to test broadcast.
