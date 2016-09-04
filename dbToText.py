# encoding: utf-8

from pymongo import MongoClient
import codecs
class dbToText():
    def __init__(self,dir = None):
        self.dir = dir
    def db_user_text(self,db,text,name):
        with codecs.open(text,'w','utf-8') as fp:
            for items in db.find({},{'user':1}):
                fp.write(items["user"][name]+'\n')

    def db_text(self,db,text,name):
        with codecs.open(text,'w','utf-8') as fp:
            for items in db.find():
                fp.write(items[name]+'\n')

    def run(self):
        MONGO_CONN=MongoClient(host='localhost',port=27017)
        db=MONGO_CONN['weibocomment']['shoujin']
        self.db_text(db,self.dir+'/webcomment.txt',"text")
        self.db_text(db,self.dir+'/created_at.txt','created_at')
        self.db_user_text(db,self.dir+'/province.txt',"province")

if __name__ == "__main__":
    t=dbToText('shoujin')
    t.run()