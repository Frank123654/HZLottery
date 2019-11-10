import re
import urllib.request as http
import tabula
from pandas import Series, DataFrame
import pdfplumber as pdfer
class DataSrc():
    urls = ['http://down.hz-notary.com:10006/pdf/2019/1026/191026125013819_26449989149514513.pdf',
            'http://down.hz-notary.com:10006/pdf/2019/1027/191027155324102_26547378576490021.pdf']

    @classmethod
    def getRegInfo(cls):
        file_url = cls.urls[0]
        pattern = re.compile(r'\d+')  # 编译过滤数字正则的pattern
        response = http.urlopen(file_url)
        pdf = response.read()
        file_name = file_url.split('/')[-1]
        df = DataFrame({})
        with open(file_name, 'wb+') as f:
            f.write(pdf)
            df = tabula.read_pdf(file_name, encoding='gbk', pages='all', pandas_options={'error_bad_lines': False})
            #print(df)
            f.close()
        return df

    @classmethod
    def getLotteryRet(cls):
        file_url = cls.urls[1]
        pattern = re.compile(r'\d+')  # 编译过滤数字正则的pattern
        response = http.urlopen(file_url)
        pdf = response.read()
        file_name = file_url.split('/')[-1]
        df = DataFrame({})
        with open(file_name, 'wb+') as f:
            f.write(pdf)
            f.close()
        lists = []
        with pdfer.open(file_name) as f:
            for page in f.pages:
                s = page.extract_text()
                lists.extend(list(map(lambda x: tuple(x.split(" ")), s.splitlines())))
                f.close()
                #print(lists)
        if len(lists) > 1:
            del lists[0]
        lists = list(map(lambda x: tuple([int(x[0]), x[1], int(pattern.findall(x[1])[0])]), lists))
        return lists

if __name__ == '__main__':
    print(DataSrc.getLotteryRet())
    #DataSource.getLotteryRet()
