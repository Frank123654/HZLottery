# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader

class Reporter:

    def __init__(self, name):
        self.name = name
        self.wscxkeys = ['regid', 'personname', 'personid', 'hashouse', 'wscx', 'othernames', 'otherids']
        self.luckyguyskeys = ['orderno', 'regid', 'personname', 'personid']
        self.name_idSamelistkeys = self.wscxkeys
        self.houseStatisticskeys = ['hashouse', 'count']

    def genHtml(self, url, wscxSame, nameSame, idSame, luckyguys, houseStatistics):
        url = 'http://down.hz-notary.com:10006/pdf/2019/1026/'
        wscxSamelist = list(map(lambda x: dict(zip(self.wscxkeys, x)), wscxSame))
        nameSamelist = list(map(lambda x: dict(zip(self.name_idSamelistkeys, x)), nameSame))
        idSamelist = list(map(lambda x: dict(zip(self.name_idSamelistkeys, x)), idSame))
        luckyguyslist = list(map(lambda x: dict(zip(self.luckyguyskeys, x)), luckyguys))
        houseStatisticslist = list(map(lambda x: dict(zip(self.houseStatisticskeys, x)), houseStatistics))
        env = Environment(loader=FileSystemLoader('./'))
        template = env.get_template('template.html')
        filename = """{0}_report.html""".format(self.name)
        with open(filename, 'w+') as fout:
            html_content = template.render(name=self.name,
                                           wscxSame=wscxSamelist,
                                           nameSame=nameSamelist,
                                           idSame=idSamelist,
                                           luckyguys=luckyguyslist,
                                           houseStatistics=houseStatisticslist,
                                           url = url)
            fout.write(html_content)
            fout.close()


if __name__ == "__main__":
    name = "weilaiyue"
    wscxSame = (('JHF00091', '杨*', '330105********2814', '是', '2019-WSCX-7321459', '杨*懿,杜*翡', '330105********282X,330683********7021'), ('JHF00001', '吴*涛', '330105********2814', '否', '2019-WSCX-7274948', '0', '0'))
    name_idSame = []
    luckyguys =((176, 'JHF00092', '李*', '331082********921X'), (178, 'JHF00092', '李*', '331082********921X'))
    houseStatistics = (('否', 126), ('是', 52))

    report = Reporter(name)
    report.genHtml(wscxSame, name_idSame, luckyguys, houseStatistics)



