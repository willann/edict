import pymongo
import sys
import re


def edict():
    pattern = r".+\n"
    regex = re.compile(pattern)
    f = open("dict.txt")
    id = 1
    conn = pymongo.MongoClient("localhost", 27017)
    db = conn.edict
    myset = db.edict
    for line in f:
        l = regex.findall(line)
        word = l[0][0:17].strip(" ")
        interpreter = l[0][17:-2]
        myset.insert({"_id": id, "word":word,"interpreter": interpreter})
        id += 1
    conn.close()


if __name__ == '__main__':
    edict()
