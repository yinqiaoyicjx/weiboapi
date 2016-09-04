__author__ = 'cjx'
from weibo import APIClient
import urllib2
import urllib
import json
import sys
from pymongo import MongoClient
import codecs
import time
from dbToText import dbToText
from text_filter import textFilter
from ciping import ciPing
from time_location import timeLocation

class weiboApi():
    def __init__(self,colleage = None,dir = None):
        self.colleage = colleage
        self.dir = dir
        self.total = 0

    def weiboClient(self):
        APP_KEY='1257616669'
        APP_SECRET='b8d924e1b6aa10f0bbd4e7af6ed1bf19'
        CALLBACK_URL='https://api.weibo.com/oauth2/default.html'
        AUTH_URL='https://api.weibo.com/oauth2/authorize'
        USERID=''
        PASSWD=''
        client=APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
        referer_url=client.get_authorize_url()
        print "referer url is: %s" % referer_url
        cookies=urllib2.HTTPCookieProcessor()
        opener=urllib2.build_opener(cookies)
        urllib2.install_opener(opener)
        postdata={
            "client_id":APP_KEY,
            "redirect_uri":CALLBACK_URL,
            "userId":USERID,
            "passwd":PASSWD,
            "isLoginSina":"0",
            "action":"submit",
            "response_type":"code",
        }
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
                   "Host": "api.weibo.com",
                   "Referer": referer_url
                   }
        req=urllib2.Request(url=AUTH_URL,data=urllib.urlencode(postdata),headers=headers)
        try:
            resp=urllib2.urlopen(req)
            print "callback url is : %s" % resp.geturl()
            code=resp.geturl()[-32:]
            print "code is %s" % code
        except Exception, e:
            print e

        code = raw_input()
        r = client.request_access_token(code)
        access_token1 = r.access_token
        expires_in = r.expires_in

        print "access_token=" ,access_token1
        print "expires_in=" ,expires_in
        client.set_access_token(access_token1,expires_in)
        return client

    def showcomments(self,mid,client,page = 1):
        result=client.comments.show.get(id = mid,page = page,count = 200)
        return result

    def savetex(self,result):
        re=[]
        for i in range(99):
            time=result["comments"][i]["created_at"]
            id=result["comments"][i]["id"]
            text=result["comments"][i]["text"]
            mid=result["comments"][i]["mid"]
            user_id=result["comments"][i]["user"]["id"]
            user_province=result["comments"][i]["user"]["province"]
            user_city=result["comments"][i]["user"]["city"]
            user_location=result["comments"][i]["user"]["location"]
            #print "%s,%s,%s,%s,%s,%s" % (time,id,text,mid,user_id,user_province)
            text=text+" "+str(id)
            re.append(text)
            if i == 48:
                sin_id=id

        with codecs.open('webcomment', 'ab', encoding='utf-8') as fp:
            movies=re
            fp.write(u'{movies}\n\n'.format(movies='\n'.join(movies)))

    def savemongo(self,result,MONGO_CONN):
        for com in result["comments"]:
            MONGO_CONN['weibocomment'][self.colleage].update_one(
                filter={'_id':com["id"]},
                update={'$set':com},
                upsert=True
            )


    def run(self):
        client=self.weiboClient()
        mid = client.get.statuses__queryid(mid = 'E2va4bnb9', isBase62 = 1, type = 1)['id']
        MONGO_CONN=MongoClient(host='localhost',port=27017)
        r=self.showcomments(mid,client)
        self.total = r["total_number"]
        self.savemongo(r,MONGO_CONN)
        #self.total*0.3/200-1
        for i in range(4):
            time.sleep(240)
            r=self.showcomments(mid,client,i+2)
            self.savemongo(r,MONGO_CONN)


if __name__ == "__main__":
    #a=weiboApi('shoujin','shoujin')
    #a.run()
    #b=dbToText('shoujin')
    #b.run()
    #c=textFilter('shoujin')
    #c.run()
    #d=ciPing('shoujin')
    #d.run()
    e=timeLocation('shoujin')
    e.run()


