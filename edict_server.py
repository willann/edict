from socket import *
import sys
import time
import signal
import os
import pymongo


def edict_server(port):
    sockfd = socket(AF_INET, SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(("0.0.0.0", port))
    sockfd.listen(3)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        try:
            connfd, addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出")
        except Exception as e:
            print("服务器异常:", e)
            continue
        print("客户端连接")
        pid = os.fork()
        if pid == 0:
            sockfd.close()
            # 判断客户端请求
            while True:
                data = connfd.recv(1024).decode().split(" ")
                if data[0] == "D":
                    connfd.send(b"OK")
                    data = connfd.recv(1024).decode().split("#")
                    name = data[0]
                    password = data[1]
                    do_login(connfd, name, password)
                elif data[0] == "Z":
                    print(data)
                    connfd.send(b"OK")
                    data = connfd.recv(1024).decode().split("#")
                    name = data[0]
                    password = data[1]
                    do_sign(connfd, name, password)
                elif data[0] == "C":
                    word = connfd.recv(1024).decode()
                    if word=="##":
                        pass
                    else:
                        search(name, connfd, word)
                elif data[0] == "H":
                    # print(data)
                    history(name, connfd)
                elif data[0] == "Q":
                    # print(data)
                    connfd.close()
                    sys.exit()
                else:
                    connfd.close()
                    sys.exit()

        else:
            connfd.close()
            continue


def do_login(connfd, name, password):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn.user
    myset = db.user_info
    info = myset.find_one({"name": name}, {"password": 1})
    if info is None:
        connfd.send(b"false")
    elif info["password"] == password:
        connfd.send(b'successs')
    else:
        connfd.send(b"false")
    conn.close()


def do_sign(connfd, name, password):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn.user
    myset = db.user_info
    info = myset.find_one({"name": name}, {"password": 1})
    if not info:
        myset.insert({"name": name, "password": password})
        connfd.send(b'OK')
    else:
        connfd.send(b"false")
    conn.close()


def search(name, connfd, word):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn.edict
    myset = db.edict
    data = myset.find_one({"word": word}, {"_id": 0})
    if not data:
        msg = "!!!"
        connfd.send(msg.encode())
    else:
        msg = data["interpreter"]
        connfd.send(msg.encode())
    db2 = conn.user
    myset2 = db2.user_history
    myset2.insert({"name": name, "word": word,
                   "interpreter": msg, "time": 'time'})
    conn.close()


def history(name, connfd):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn.user
    myset = db.user_history
    cursor = myset.find({"name": name}, {"_id": 0})
    for i in cursor:
        word = i["word"]
        interpreter = i["interpreter"]
        time_serch = i["time"]
        # print(word,interpreter,time_serch)
        msg = word+"#"+interpreter+"#"+time_serch
        # print(msg)
        connfd.send(msg.encode())
        connfd.recv(1024)
    connfd.send(b'##')
    conn.close()


if __name__ == '__main__':
    edict_server(8888)
