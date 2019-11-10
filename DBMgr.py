#!usr/bin/env python
import pymysql as sqldb
import pandas as pd
import DataSource
import re
import ReportHTML as repHtml

class SQLMgr(object):
    # init
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    # connect to db
    def connect(self):
        self.conn = sqldb.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'root',
            db = 'mysql',
            charset='utf8')
        self.cursor = self.conn.cursor()

    # query single
    def get_one(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    # query many
    def get_list(self, sql, args=None):
        print(sql)
        self.cursor.execute(sql, args)
        self.conn.commit()
        result = self.cursor.fetchall()
        return result

    # modify one
    def moddify_single(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.conn.commit()

    # modify many
    def modify_list(self, sql, args=None):
        self.cursor.executemany(sql, args)
        self.conn.commit()

    # create
    def create(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.conn.commit()
        #last_id = self.cursor.lastrowid()
        #return last_id

    # close database
    def close(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self__

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()



class LotterySQLMgr(SQLMgr):

    # 初始化时，创建相应reg_tbl, lottery_tbl表格
    def __init__(self, reg_tbl, lottery_tbl):
        self.reg_tbl = reg_tbl
        self.lottery_tbl = lottery_tbl
        SQLMgr.__init__(self)
        # create table if not exists
        if self.isTableExist(reg_tbl) == False:
            sql = r'''create table if not exists {0} (regid varchar(64) not null primary key,personname varchar(64) not null,personid varchar(64) not null,hashouse varchar(64) not null,wscx varchar(64) not null,othernames varchar(128),otherids varchar(128))'''.format(self.reg_tbl)
            self.create(sql)

        if self.isTableExist(lottery_tbl) == False:
            sql = r'''create table if not exists {0} ( orderno int primary key, regid varchar(64) not null, regidnum int )'''.format(self.lottery_tbl)
            self.create(sql)

    # query data
    def isTableExist(self, tbl_name):
        sql = "show tables;"
        tables = self.get_list(sql)
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if tbl_name not in table_list:
            return False
        else:
            return True

    # insert reg data
    def insertReg(self, df):
        sql = r"""insert ignore into {0} values(%s, %s, %s, %s, %s, %s, %s)""".format(self.reg_tbl)
        df = df.fillna('0')
        record_tuple_list = []
        rows = df.shape[0]  # 获取行数
        columns = df.shape[1]  # 获取列数
        for r in range(rows):
            if df.iloc[r].iloc[0] == '购房登记号':
                continue
            list = df.iloc[r].tolist()
            record_tuple = tuple(map(lambda x: x.replace('\r', '').replace('\n', ''), list))  # 获取一行数据组成的tuple
            record_tuple_list.append(record_tuple)
        self.modify_list(sql, record_tuple_list)

    # insert lottery data
    def insertLottery(self, list):
        sql = r"""insert ignore into {0} values(%s, %s, %s)""".format(self.lottery_tbl)
        self.modify_list(sql, list)

    ### 1.登记信息校验
    # 1.1.无房证明重复
    def wscxSame(self):
        sql = r"""select * from {0} where wscx in (select wscx from {0} group by wscx having count(wscx) > 1)""".format(self.reg_tbl)
        return self.get_list(sql)


    # 1.2.名字一致（仅参考）
    def nameSame(self):
        #sql = r"""select distinct t1.regid,t1.personname,t1.personid,t1.hashouse,t1.wscx,t1.othernames,t1.otherids from {0} t1, {0} t2 where t1.regid != t2.regid and (t1.personname = t2.personname or t1.personid = t2.personid)""".format(self.reg_tbl)
        sql = r"""select * from {0} t1 where t1.personname in (select t2.personname from {0} t2 group by t2.personname having count(t2.personname) > 1)""".format(self.reg_tbl)
        return self.get_list(sql)

    # 1.3.身份证一致（仅参考）
    def idSame(self):
        #sql = r"""select distinct t1.regid,t1.personname,t1.personid,t1.hashouse,t1.wscx,t1.othernames,t1.otherids from {0} t1, {0} t2 where t1.regid != t2.regid and (t1.personname = t2.personname or t1.personid = t2.personid)""".format(self.reg_tbl)
        sql = r"""select * from {0} t1 where t1.personid in (select t2.personid from {0} t2 group by t2.personid having count(t2.personid) > 1)""".format(self.reg_tbl)
        return self.get_list(sql)

    ### 2.摇号结果校验
    # 2.1.两连号
    def consecutiveNo(self):
        #sql = r"""""".format(self.lottery_tbl)
        pass

    # 2.2.重复中签
    def luckyguys(self):
        sql = r"""select t1.orderno, r.regid, r.personname, r.personid from {1} t1, {0} r where t1.regid in (select t2.regid from {1} t2 group by t2.regid having count(t2.regid) > 1) and t1.regid = r.regid""".format(self.reg_tbl, self.lottery_tbl)
        return self.get_list(sql)


    ### 3.统计中签的无房家庭和有房家庭
    def houseStatistics(self):
        sql = r"""select t.hashouse as '是否无房家庭', count(t.hashouse) as '数量' from (select r.hashouse from {0} r, {1} l where r.regid = l.regid) t group by t.hashouse;""".format(self.reg_tbl, self.lottery_tbl)
        return self.get_list(sql)

if __name__ == '__main__':
    df = DataSource.DataSrc.getRegInfo()
    list = DataSource.DataSrc.getLotteryRet()
    try:
        reg_tbl = "test3_register"
        lottery_tbl = "test3_lottery"

        # 初始化
        ltySQLMgr = LotterySQLMgr(reg_tbl, lottery_tbl)

        # 插入登记表数据
        if ltySQLMgr.isTableExist(reg_tbl)==True:
            ltySQLMgr.insertReg(df)

        # 插入摇号结果数据
        if ltySQLMgr.isTableExist(lottery_tbl) == True:
            ltySQLMgr.insertLottery(list)

        ##### 开始数据分析
        report = repHtml.Reporter("杨柳郡")
        url = 'https://www.hz-notary.com/lottery/detail?lottery.id=3076c1ce6b034c2c81797af26a5c0aac'
        report.genHtml(url, ltySQLMgr.wscxSame(), ltySQLMgr.nameSame(), ltySQLMgr.idSame(), ltySQLMgr.luckyguys(), ltySQLMgr.houseStatistics())

    except BaseException as e:
        print("exception in+++++")
        print(e)

    finally:
        pass
        #DataSource.getLotteryRet()
