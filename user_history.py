import pymongo


def user_history(name,word):
    conn=pymongo.MongoClient("localhost",27017)
    db=conn.user
    myset=db.user_history
    myset.insert({"name":name,"word":word})
    conn,close()