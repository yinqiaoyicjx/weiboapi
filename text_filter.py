__author__ = 'cjx'
#coding:utf-8
import string
import jieba
import codecs

class textFilter():
    def __init__(self,dir = None):
        self.dir = dir
        extra='filter_dict'
        jieba.load_userdict(extra)


    def filter_str(self,instr):
        deEstr = string.punctuation + ' ' + string.digits + string.letters
        deCstr = ',.()?!"":'
        destr = deEstr + deCstr
        outstr = ''
        for char in instr.decode('utf-8'):
          if char not in destr:
            outstr += char
        return outstr

    def run(self):

        fp_in=open(self.dir+'/webcomment.txt','rb+')
        fp_out=codecs.open(self.dir+'/webcom_filter.txt','ab','utf-8')


        for line in fp_in:
            str_delete=self.filter_str(line)
            str_list=jieba.cut(str_delete,cut_all=True)
            str_join=' '.join(str_list)
            fp_out.write(str_join)

        fp_in.close()
        fp_out.close()

if __name__ == "__main__":
    t=textFilter('shoujin')
    t.run()

