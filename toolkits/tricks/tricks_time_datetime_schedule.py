
#%% -----------------     时间符号  ------------------
# %y # 两位数的年份表示（00-99）
# %Y # 四位数的年份表示（000-9999）
# %m # 月份（01-12）
# %d # 月内中的一天（0-31）
# %H # 24小时制小时数（0-23）
# %I # 12小时制小时数（01-12） 
# %M # 分钟数（00=59）
# %S # 秒（00-59）
 
# %a # 本地简化星期名称
# %A # 本地完整星期名称
# %b # 本地简化的月份名称
# %B # 本地完整的月份名称
# %c # 本地相应的日期表示和时间表示
# %j # 年内的一天（001-366）
# %p # 本地A.M.或P.M.的等价符
# %U # 一年中的星期数（00-53）星期天为星期的开始
# %w # 星期（0-6），星期天为星期的开始
# %W # 一年中的星期数（00-53）星期一为星期的开始
# %x # 本地相应的日期表示
# %X # 本地相应的时间表示
# %Z # 当前时区的名称
# %% # %号本身

#%% ----------------- 
# 表示时间的两种方式：
# 1. 时间戳(相对于1970.1.1 00:00:00以秒计算的偏移量),时间戳是惟一的
# 2. 时间元组 即(struct_time),共有九个元素，分别表示，同一个时间戳的struct_time会因为时区不同而不同

#%% ----------------- 
# 生成日期列表
import datetime
start='2018-07-01'
end='2018-07-21'
 
datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
dateend=datetime.datetime.strptime(end,'%Y-%m-%d')
 
day_list = []
while datestart<dateend:
    datestart+=datetime.timedelta(days=1)
    day_list.append(datestart.strftime('%Y-%m-%d'))


#%% ----------------- 
# 格式化输出时间
time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# '2014-08-15 09:43:04'

# 接上文，不加参数时，默认就是输出当前的时间
time.strftime('%Y-%m-%d %H:%M:%S')
# '2014-08-15 09:46:53’

# 当然也可以透过datetime模块来实现，如下：
t = time.time()
datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
# '2014-08-15 10:04:51’

# 同时，也可以只使用datetime模块
datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# '2014-08-15 09:45:27’
datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
# '2014-08-15 09:46:10'

#%% ----------------- 
# 获取时间差，计算程序执行时间
start = time.time()
time.sleep(10)
end = time.time()
print end - start

starttime = datetime.datetime.now()
endtime = datetime.datetime.now()
print (endtime - starttime).seconds

# time.time()和time.clock()在不同的操作系统下，有不同的结果
# 在ubuntu下，time()获取的是时钟过去的时间，clock()获取的是CPU在当前进程上的执行时间
print(time.time(), time.clock())

#%% ----------------- 
# 获取n天前的时间
cur_time = dt.now()
# previous n days
pre_time = dt.timedelta(days=n)

import datetime
now = datetime.datetime.now()

# 前一小时
d1 = now - datetime.timedelta(hours=1)
print d1.strftime("%Y-%m-%d %H:%S:%M")

# 前一天
d2 = now - datetime.timedelta(days=1)
print d2.strftime("%Y-%m-%d %H:%S:%M")

# 上周日
d3 = now - datetime.timedelta(days=now.isoweekday())
print d3.strftime("%Y-%m-%d %H:%S:%M"), " ", d3.isoweekday()

# 上周一
d31 = d3 - datetime.timedelta(days=6)
print d31.strftime("%Y-%m-%d %H:%S:%M"), " ", d31.isoweekday()

# 上个月最后一天
d4 = now - datetime.timedelta(days=now.day)
print d3.strftime("%Y-%m-%d %H:%S:%M")

# 上个月第一天
print datetime.datetime(d4.year, d4.month, 1) 

#%% ----------------- 
# 时间格式转换
# 字符串时间转时间搓
datestr1 = '2015-06-06 10:10:10'
print 'datestr to time :', time.mktime(time.strptime(datestr1, "%Y-%m-%d %H:%M:%S"))

# 时间搓转格式化时间字符串
time1 = time.time()
print 'time to datestr :', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time1))

# datetime对象转时间搓
datetime1 = datetime.datetime.now()
print 'datetime to time :', time.mktime(datetime1.timetuple())

# 时间戳转datetime对象
t1 = time.time()
t2 = t1 + 20
d1 = datetime.datetime.fromtimestamp(t1)
d2 = datetime.datetime.fromtimestamp(t2)
print 'time1 to datetime1 :', datetime.datetime.fromtimestamp(t1)
print 'time2 to datetime2 :', datetime.datetime.fromtimestamp(t2)
print 'seconds diff :', (d2 - d1).seconds


#%% -----------------     datetime  ------------------
import datetime as dt
#%% ----------------- 
# 1. datetime.date: 是指年月日构成的日期(相当于日历)
today = datetime.date.today()
# datetime.date(2014, 8, 15)
t = datetime.date(2014,8,15)
# datetime.date(2014, 8, 15)

today.strftime('%Y-%m-%d %H:%M:%S')
# '2014-08-15 00:00:00’
# date对象中小时、分钟、秒默认都是0，纪元年的那个时间

# 转成struct_time格式，这样传递给time.mktime(t)  后，直接转成时间戳格式
today.timetuple()

today.replace(year=2013)
# datetime.date(2013, 8, 15)

# 将时间戳转化为date对象
datetime.date.fromtimestamp(1408058729)
# datetime.date(2014, 8, 15)

#%% ----------------- 
# 2. datetime.time: 是指时分秒微秒构成的一天24小时中的具体时间(相当于手表)

#%% ----------------- 
# 3. datetime.datetime: 上面两个合在一起，既包含时间又包含日期
datetime.datetime.today()
# 当不指定时区时，和datetime.datetime.today()是一样的结果，如下
datetime.datetime.now()
datetime.datetime.timple()
datetime.datetime.replace(year, month, day)
# 将时间戳转化为datetime对象
datetime.datetime.fromtimestamp(1408061894)

#%% ----------------- 
# 4. datetime.timedelta: 时间间隔对象(timedelta)。
# 一个时间点(datetime)加上一个时间间隔(timedelta)可以得到一个新的时间点(datetime)。
# 比如今天的上午3点加上5个小时得到今天的上午8点。
# 同理，两个时间点相减会得到一个时间间隔。
today = datetime.datetime.today()
yesterday = today - datetime.timedelta(days=1)
# datetime.datetime(2014, 8, 14, 15, 8, 25, 783471)


#%% -----------------     time  ------------------
import time

time.clock()
time.sleep(3)
time.strftime('%Y-%m-%d %H:%M:%S')
time.time() # 得到当前时间
time.localtime(time.time())  # 将时间戳转换为时间元组 struct_time
time.mktime(time.localtime(1407945600.0))  # 将一个struct_time转换为时间戳

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt
 
def datetime_timestamp(dt):
     #dt为字符串
     #中间过程，一般都需要将字符串转化为时间数组
     time.strptime(dt, '%Y-%m-%d %H:%M:%S')
     ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
     #将"2012-03-28 06:53:40"转化为时间戳
     s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
     return int(s)

timestamp_datetime(1508994902)   # '2017-10-26 13:15:02'
datetime_timestamp('2018-06-04 23:59:59')  # 1528127999


#%% -----------------     schedule  ------------------
import schedule
import time
 
def job():
    print("I'm working...")
 
schedule.every(10).seconds.do(job)#每隔10秒执行函数job
schedule.every(10).minutes.do(job)#每隔10分钟执行函数job
schedule.every().hour.do(job)#每隔1小时执行函数job
schedule.every().day.at("10:30").do(job) #每天的10点半执行函数job 
schedule.every().monday.do(job)#每周一执行函数job
schedule.every().wednesday.at("13:15").do(job)  #每周三下午1点14分执行函数job
 
while True:
    schedule.run_pending()
    time.sleep(1)