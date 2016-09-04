# encoding: utf-8

from datetime import *
import codecs
from pylab import *
import numpy

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

class timeLocation():
    def __init__(self, dir = None):
        self.dir = dir
    def time_show(self):
        with open(self.dir+'/created_at.txt', 'r') as f:
            rt_time = []
            for line in f :
                time= line.strip().split(',')[-1]
                day = time[8:10]
                hms= time[11:17].replace(':', '')
                time = int(day + hms)
                rt_time.append(time)
        day=[]

        for i in rt_time:
            if len(str(i)) == 5:
                day.append(('2016-08-0'+str(i)[:1]+'-'+str(i)[1:3]))
            else:
                day.append(('2016-08-'+str(i)[:2]+'-'+str(i)[2:4]))
        day = [datetime.datetime.strptime(d, '%Y-%m-%d-%H') for d in day]
        day_weibo = datetime.datetime.strptime('2016-08-07-22', '%Y-%m-%d-%H')
        hours = [(i-day_weibo).total_seconds()/3600 for i in day]
        values, base = np.histogram(hours, bins = 40)
        cumulative = np.cumsum(values)
        plt.subplot(1, 2, 1)
        plt.plot(base[:-1], cumulative, c = 'red')
        plt.title('Cumulative Diffusion')
        plt.ylabel('Number of Retweets')
        plt.xlabel('Hours')
        plt.subplot(1, 2, 2 )
        plt.plot(base[:-1], values, c = 'orange')
        plt.title('Hourly Diffusion')
        plt.xlabel('Hours')
        plt.savefig(self.dir+'/hour.png')

    def my_cmp(self,E1,E2):
        return -cmp(E1[1],E2[1])

    def location_show(self):
        with codecs.open(self.dir+'/province.txt','r','utf-8') as fp:
            province={}
            for lines in fp:
                line=lines.strip()
                if line in province:
                    province[line]+=1
                else:
                    province[line]=1


        with codecs.open('weibo_province.txt','r','utf-8') as fp2:
            province_dict={}
            for line in fp2:
                num=line.split()[0]
                name=line.split()[1].strip()
                province_dict[num]=name

        province_info = [(province_dict[key],val) for key,val in province.items()]
        province_info.sort(self.my_cmp)
        keylist=[key for key,val in province_info]
        vallist=[val for key,val in province_info]
        barwidth=0.5
        xVal=numpy.arange(len(keylist))
        plt.xticks(xVal+barwidth/2.0,keylist,rotation=45)
        plt.bar(xVal,vallist,width=barwidth)
        plt.title(u'province')
        plt.savefig(self.dir+"/procince.png")

    def run(self):
        self.location_show()
        self.time_show()



if __name__ == "__main__":
    t = timeLocation('shoujin')
    t.run()



