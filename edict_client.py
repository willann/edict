from socket import *
import sys
import getpass


def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)

    sockfd = socket(AF_INET, SOCK_STREAM)

    try:
        sockfd.connect(ADDR)
    except:
        print("连接服务器失败")
        return
    while True:
        print("     ========== 命令选项 ===========")
        print("     ***1. 登录   2.注册   3.退出***")
        print("     ===============================")

        cmd = input("请输入命令>>")
        if cmd.strip() == '1':
            sockfd.send(b'D')
            data = sockfd.recv(1024).decode()
            if data == "OK":
                name = input("请输入用户名：")
                password = getpass.getpass("请输入密码：")
                msg = name + "#" + password
                sockfd.send(msg.encode())
                data = sockfd.recv(1024).decode()
                if data == "successs":
                    print("登录成功")
                    while True:
                        print("     ========== 命令选项 ===============")
                        print("     ***1.查单词   2.历史记录  3.退出***")
                        print("     ===================================")
                        cmd = input("请输入命令>>")
                        if cmd.strip() == '1':
                            search(sockfd)
                        elif cmd.strip() == '2':
                            history(sockfd)
                        elif cmd.strip() == '3':
                            break
                        else:
                            print("请输入正确命令!!!")
                            continue

                elif data == "false":
                    print("登录失败，请检查用户名和密码")
                    pass

        elif cmd.strip() == '2':
            sockfd.send(b'Z')
            data = sockfd.recv(1024).decode()
            if data == "OK":
                while True:
                    name = input("请输入用户名：")
                    password = getpass.getpass("请输入密码：")
                    password2 = getpass.getpass("请输入密码：")
                    if password != password2:
                        print("两次密码不一致")
                        continue
                    else:
                        msg = name + "#" + password
                        sockfd.send(msg.encode())
                        data = sockfd.recv(1024).decode()
                        if data == "OK":
                            print("注册成功")
                            break
                        elif data == "false":
                            print("用户名已存在")

        elif cmd.strip() == '3':
            sockfd.send(b'Q')
            sockfd.close()
            sys.exit("谢谢使用")

        else:
            print("请输入正确命令!!!")
            continue


def search(sockfd):
    while True:
        sockfd.send(b'C')
        word = input("请输入单词").strip(" ")
        # print(word)
        if word:
            sockfd.send(word.encode())
            data = sockfd.recv(1024).decode()
            if data == "!!!":
                print("没有查询到单词")
            else:
                print("%s:%s" % (word[0], data))
        else:
            sockfd.send("##".encode())
            break


def history(sockfd):
    sockfd.send(b"H")
    while True:
        data = sockfd.recv(1024).decode()
        if data == "##":
            break
        else:
            msg = data.split("#")
            # print(data)
            print("%s:%s:%s" %
                  (msg[0], msg[1], msg[2]))
            sockfd.send(b'ok')


def user_interface():
    while True:
        print("     ========== 命令选项 ===============")
        print("     ***1.查单词   2.历史记录  3.退出***")
        print("     ===================================")
        cmd = input("请输入命令>>")
        if cmd.strip() == '1':
            search(sockfd)
        elif cmd.strip() == '2':
            history(sockfd)
        elif cmd.strip() == '3':
            break
        else:
            print("请输入正确命令!!!")
            continue


if __name__ == '__main__':
    main()
