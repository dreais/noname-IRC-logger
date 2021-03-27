import socket, threading, logging
import time
import codecs
from config import botnick, passwd, channels


"""
    INITIAL SETUP
    connection, authentification, channels
"""
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect(('irc.ppy.sh', 6667))
irc.send(bytes("PASS " + passwd + "\r\n", 'UTF-8'))
irc.send(bytes("NICK " + botnick + "\r\n", 'UTF-8'))

for channel in channels:
    send_data("JOIN #" + channel)

"""
    VARIABLES
"""
thread_on = True
PROCESS_ALIVE = 'PROCESS_ALIVE'


"""
    N/A
"""
def handle_privmsg(line):
    try:
        channel = line[11:].split('#')[1].split(' ')[0]
    except IndexError:
        channel = 'limbo'
    try:
        content = line[12:].split('!')[1].split(':')[1]
    except IndexError:
        content = '# EMPTY CONTENT'
    try:
        nickname = line[12:].split('!')[0]
    except IndexError:
        nickname = 'NO_USER'
    time = line[:11]
    for x in channels:
        if channel == x:
            f = codecs.open(channel + '.txt', 'a', 'utf-8-sig')
            f.write(time + nickname + ':' + content + '\n')
            f.close()
        elif '#' not in line:
            f = codecs.open('private_msg.txt', 'a', 'utf-8-sig')
            f.write(time + nickname + ':' + content + '\n')
            f.close()


def send_data(command):
    res = irc.send(bytes(command + "\r\n", 'UTF-8'))
    print("[" + command + "] returned " + str(res))


"""
    Listener(): FUNCTION USED BY THREAD 1 TO RECEIVE FROM SERVER
"""
def Listener():
    global thread_on
    while thread_on:
        try:
            msg = irc.recv(2040)
            msg = msg.decode('UTF-8').split('\n')
        except UnicodeDecodeError:
            print(msg)
            msg = ""
            continue
        if msg:
            for line in msg:
                t = time.localtime()
                strtime = '[' + time.strftime("%H:%M:%S", t) + '] '
                if 'PING' in line:
                    irc.send(bytes('PONG cho.ppy.sh\r\n', 'UTF-8'))
                    print(strtime + 'PONG!')
                if 'PRIVMSG' in line:
                    print(strtime + line)
                    handle_privmsg(strtime + line)


"""
    InputReader(): FUNCTION USED BY THREAD 2 TO RECEIVE FROM CLIENT
"""
def InputReader():
    global thread_on
    while thread_on:
        cmd = input()
        if 'QUIT' in cmd:
            thread_on = False
        else:
            print('> ' + cmd)


"""
    THREADING
"""
listening = threading.Thread(target=Listener)
listening.start()
inputreader = threading.Thread(target=InputReader)
inputreader.start()


"""
    USED FROM LOCAL TO CHECK IF BOT CRASHED
    check every 5 minutes (can be adjusted)
"""
f = open(PROCESS_ALIVE, 'w')
while thread_on:
    t = time.localtime()
    f.write(time.strftime("%H:%M:%S", t))
    sleep(60 * 5)

f.close()

"""
    IF CRASH/MANUAL QUIT, JOIN THREADS
"""
listening.join()
inputreader.join()
print('Threads joined, closing noname.py')
