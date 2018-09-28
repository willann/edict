import pymongo


def do_sign(conndf,name, password):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn.user
    myset = db.user_info
    myset.insert({"name": name, "password": password})
    conn.close()


def do_login(connfd,name,password):
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn.user
    myset = db.user_info
    info=myset.find_one({"name":name},{"password":1})
    if info{password}==password:
        connfd.send(b'OK')
    else:
        connfd.send(b"false")
    conn.close()
