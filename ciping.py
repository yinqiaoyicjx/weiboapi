# encoding: utf-8
from pylab import *
import string
import numpy
import codecs
from wordcloud import WordCloud
mpl.rcParams['font.sans-serif'] = ['SimHei']

mpl.rcParams['axes.unicode_minus'] = False

class ciPing():

    def __init__(self, dir = None):
        self.dir = dir

    def getstr(self,word, count):
        countstr = word + ',' + str(count)
        return countstr

    def get_wordlist(self,infile):
        c = codecs.open(infile,'rb+','utf-8').readlines()
        wordlist = []
        for line in c:
            if len(line)>1:
                words = line.split(' ')
                for word in words:
                    if len(word)>1:
                        wordlist.append(word)
        return wordlist

    def get_wordcount(self,wordlist, outfile):
        out = codecs.open(outfile, 'w','utf-8')
        wordcnt ={}
        for i in wordlist:
            if i in wordcnt:
                wordcnt[i] += 1
            else:
                wordcnt[i] = 1
        worddict = wordcnt.items()
        worddict.sort(key=lambda a: -a[1])
        for word,cnt in worddict:
            out.write(self.getstr(word, cnt)+'\n')
        out.close()
        return wordcnt

    def barGraph(self,wcDict):
        wordlist=[]
        for key,val in wcDict.items():
            if val>20 and len(key)>1:
                wordlist.append((key,val))
        wordlist.sort()
        keylist=[key for key,val in wordlist]
        vallist=[val for key,val in wordlist]
        barwidth=0.5
        xVal=numpy.arange(len(keylist))
        plt.xticks(xVal+barwidth/2.0,keylist,rotation=45)
        plt.bar(xVal,vallist,width=barwidth,color='y')
        plt.title(u'微博词频分析图')
        plt.savefig(self.dir+'/ciping.png')

    def wordcloudshow(self,Dict):
        wordlist=[]
        for key,val in Dict.items():
            if val>10 and len(key)>1:
                wordlist.append((key,val))
        wc=WordCloud(font_path='simhei.ttf',background_color="black",   margin=5, width=1800, height=800)
        wc.generate_from_frequencies(wordlist)
        plt.figure()
        plt.imshow(wc)
        plt.axis("off")
        wc.to_file(self.dir+'/ciyun.png')

    def run(self):
        myfile = self.dir+'/webcom_filter.txt'
        outfile = self.dir+'/result.dat'
        wordlist = self.get_wordlist(myfile)
        wordcnt = self.get_wordcount(wordlist,outfile)
        self.barGraph(wordcnt)
        self.wordcloudshow(wordcnt)

if __name__ == "__main__":
    t=ciPing('shoujin')
    t.run()