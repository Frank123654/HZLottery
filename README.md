# HZLottery
===
A script to verify lottery information

...to be continued

HZ摇号信息分析脚本
===
概要
---
该脚本针对HZ楼市摇号的登记信息和摇号结果，分析是否有异常情况。目前实现的分析维度有：

    1.登记信息校验
    1.1.查档编号重复
    1.2.购房人名称重复
    1.3.购房人证件号码重复
    2.摇号结果校验
    2.1.两连号
    2.2.重复中签
    3.统计中签的无房家庭和有房家庭
最终结果以'_report.html'报告文件形式呈现


上手指南
---
脚本主要目前主要实现了三个模块，它们分别是：<br/>
`DataSource`:主要作用是从目标url里（分别是登记信息url和摇号结果url）提取出登记信息和摇号信息，作为下一步分析的数据源。<br/>
`DBMgr`:实现了对MySQL的操作类，将从DataSource取得的数据存入数据库，并实现了前述各类校验信息的查找函数。<br/>
`ReportHTML`:将DBMgr各类校验性查找的结果报表化，以'_report.html'报告文件形式输出<br/>


安装
---
1.MySQL，本人采用8.0.17版<br/>
2.<br/>
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple tabula-py<br/>
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas<br/>
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy<br/>
还需要安装java7/8<br/>
3.pip install pdfplumber<br/>
4.pip install pymysql<br/>
5.pip install jinja2<br/>


部署
---
1.确保mysql服务打开。<br/>
安装好mysql后，在“服务”里查看"MYSQL"是否已经启动，如果没有就启动。建议设为自动启动。<br/>
2.SQL登录信息修改<br/>
目前SQL的登录信息是写死在代码里的，在DBMgr.py的SQLMgr的connect里填上正确的登录信息。<br/>
3.填写数据源URL<br/>
目前摇号数据源也是写死的，在DataSource.py的DataSrc的urls变量填写想分析的URL。可以在https://www.hz-notary.com/lottery/index随意点击感兴趣的楼盘摇号信息，
然后分别填下登记汇总表和摇号结果的url。这块后面再用爬虫爬取来优化。<br/>
4.执行DBMgr.py脚本<br/>
执行后在当前目录下生成_report.html文件<br/>


框架
---
* pymysql - python的mysql管理模块
* tabula - python的pdf模块之一，适合读取pdf表格数据
* pandas - python数据处理三剑客之一，适合数据分析，基于numpy
* numpy - python数据处理三剑客之一，适合大量维度数组和矩阵计算
* pdfplumber - python的pdf模块之一，适合读取pdf文本数据
* jinja2 - python生成html文件的模块


作者
---
Frank123654(https://github.com/Frank123654)
