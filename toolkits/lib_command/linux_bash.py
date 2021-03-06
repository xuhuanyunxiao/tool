
----------------------------------------- linux ----------------------------------------
#%% -----------------  挂载共享文件夹
sudo mount -t vboxsf win_to_centos7 /mnt/centos7_to_win
sudo mount -t vboxsf win_to_centos7 /root/centos7_to_win
sudo mount -t vboxsf win_to_centos7 /mnt/centos7_to_win
sudo mount -t vboxsf win_to_centos7 /mnt/ubuntu_to_win

#%% -----------------  网卡
systemctl restart network   重启网卡
systemctl status network  查看网卡状态

#%% -----------------  防火墙
启动： systemctl start firewalld
查看状态： systemctl status firewalld 
停止： systemctl disable firewalld
禁用： systemctl stop firewalld


#%% -----------------  路径与文件 
# 复制、删除、移动
cp -r git_prog/proj_circ circ  # -r 递归复制，保留原文件目录结构  # 注意复制时命令所在文件夹
rm -rf 目录名字 # 删除文件
	-r 向下递归，不管有多少级目录，
	-f 直接强行删除，不作提示意思。

# 查看
du -sh * # 查看当前目录下各个文件及目录占用空间大小
df -h  # 查看系统中文件的使用情况
du -h --max-depth=1 /home   仅列出home目录下面所有的一级目录文件大小
du -h --max-depth=1 /home/* 列出home下面所有一级目录的一级目录文件大小。

ll -h
Linux是先有目录，再有磁盘分区。
//没有挂载磁盘的目录，显示在系统盘
//挂载了磁盘的目录，显示在数据盘分区vdb1
df -h /home/

# 查看文件的权限
ls -l 
# 一共有十位数，其中：最前面那个 - 代表的是类型
# 中间那三个 rw- 代表的是所有者（user）拥有的权限
# 然后那三个 r-- 代表的是组群（group）拥有的权限
# 最后那三个 r-- 代表的是其他人（other）拥有的权限
#  然后
# r 表示文件可以被读（read）
# w 表示文件可以被写（write）
# x 表示文件可以被执行（如果它是程序的话）
# - 表示相应的权限还没有被授予
需要注意的是：查看文件权限的目录问题: 如果有文件夹  /a/b/c

那么执行 ls -l /a/b 查看权限的文件并不是b，而是查看的c的权限。

ls -l /a 查看的是b文件的权限
ls -l /a/b 查看的是c文件的权限
ls -l /a/b/c 查看的是c文件的权限

# 显示隐藏文件
l.（这是个命令别名，实际命令为ls -d .* --color=auto）
# 显示当前目录下的所有隐藏文件，只显示名称，不显示详情

# 查找
(1)find命令是根据文件的属性进行查找，如文件名，文件大小，所有者，所属组，是否为空，访问时间，修改时间等。 
(2)grep是根据文件的内容进行查找，会对文件的每一行按照给定的模式(patter)进行匹配查找。

基本格式：find  path expression
1.按照文件名查找
　　　　(1)find / -name httpd.conf　　#在根目录下查找文件httpd.conf，表示在整个硬盘查找
　　　　(2)find /etc -name httpd.conf　　#在/etc目录下文件httpd.conf
　　　　(3)find /etc -name '*srm*'　　#使用通配符*(0或者任意多个)。表示在/etc目录下查找文件名中含有字符串‘srm’的文件
　　　　(4)find . -name 'srm*' 　　#表示当前目录下查找文件名开头是字符串‘srm’的文件
2.按照文件特征查找 　　　　
　　　　(1)find / -amin -10 　　# 查找在系统中最后10分钟访问的文件(access time)
　　　　(2)find / -atime -2　　 # 查找在系统中最后48小时访问的文件
　　　　(3)find / -empty 　　# 查找在系统中为空的文件或者文件夹
　　　　(4)find / -group cat 　　# 查找在系统中属于 group为cat的文件
　　　　(5)find / -mmin -5 　　# 查找在系统中最后5分钟里修改过的文件(modify time)
　　　　(6)find / -mtime -1 　　#查找在系统中最后24小时里修改过的文件
　　　　(7)find / -user fred 　　#查找在系统中属于fred这个用户的文件
　　　　(8)find / -size +10000c　　#查找出大于10000000字节的文件(c:字节，w:双字，k:KB，M:MB，G:GB)
　　　　(9)find / -size -1000k 　　#查找出小于1000KB的文件
3.使用混合查找方式查找文件
　　　　参数有： ！，-and(-a)，-or(-o)。
　　　　(1)find /tmp -size +10000c -and -mtime +2 　　#在/tmp目录下查找大于10000字节并在最后2分钟内修改的文件
　　  (2)find / -user fred -or -user george 　　#在/目录下查找用户是fred或者george的文件文件
　　  (3)find /tmp ! -user panda　　#在/tmp目录中查找所有不属于panda用户的文件


#%% -----------------  系统信息
cat /proc/version  
uname：显示操作系统信息
uname -a 显示全部信息

#%% ----- Ubuntu
lsb_release：显示发行版信息
lsb_release -a 显示全部

uname -m && cat /etc/*release
gcc --version


#%% -----------------  CUP
/proc/cupinfo：查看CUP特性信息
cat /proc/cpuinfo
cat /proc/cpuinfo | grep process | wc -l   统计CPU的物理核心数量
# 总核数 = 物理CPU个数 X 每颗物理CPU的核数 
# 总逻辑CPU数 = 物理CPU个数 X 每颗物理CPU的核数 X 超线程数

# 查看物理CPU个数
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l

# 查看每个物理CPU中core的个数(即核数)
cat /proc/cpuinfo| grep "cpu cores"| uniq

# 查看逻辑CPU的个数
cat /proc/cpuinfo| grep "processor"| wc -l
 查看CPU信息（型号）
cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c

# 查使用CPU最多的K个进程
ps -aux | sort -k3nr | head -K


#%% -----------------  GPU
# 显卡型号
ubuntu-drivers devices
model    : GM107 [GeForce GTX 750 Ti]#这个就是图形卡类型

# 图形显卡驱动安装成功与否
nvidia-smi   # 查看显存的使用情况

lspci | grep -i vga
使用nvidia GPU可以：
lspci | grep -i nvidia

查看指定显卡的详细信息用以下指令：
lspci -v -s 00:0f.0


查看服务器cuda版本
cat /usr/local/cuda/version.txt

cudnn 版本 
cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2


#%% -----------------  硬盘与内存
free total -h

# Linux下查看硬盘及分区信息
fdisk -l 
# 文件系统的磁盘空间占用情况
df -h
# 查看某目录的大小:
linuxidc@ubuntu:~$ du -sh 
# 查看某目录下占用空间最多的文件或目录。取前10个。需要先进入该目录下。
du -cks * | sort -rn | head -n 10

#%% -----------------  内存
free 
free -m

# 查使用内存最多的K个进程
ps -aux | sort -k4nr | head -K
# 如果是10个进程，K=10，如果是最高的三个，K=3
# 说明：ps -aux中（a指代all——所有的进程，u指代userid——执行该进程的用户id，x指代显示所有程序，不以终端机来区分）
#         ps -aux的输出格式如下：
# USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
# root         1  0.0  0.0  19352  1308 ?        Ss   Jul29   0:00 /sbin/init
# root         2  0.0  0.0      0     0 ?        S    Jul29   0:00 [kthreadd]
# root         3  0.0  0.0      0     0 ?        S    Jul29   0:11 [migration/0]
# sort -k4nr中（k代表从第几个位置开始，后面的数字4即是其开始位置，结束位置如果没有，则默认到最后；
# n指代numberic sort，根据其数值排序；
# r指代reverse，这里是指反向比较结果，输出时默认从小到大，反向后从大到小。）。
# 本例中，可以看到%MEM在第4个位置，根据%MEM的数值进行由大到小的排序。
# head -K（K指代行数，即输出前几位的结果）

#%% -----------------  进程与端口
iostat：查看系统CUP、磁盘性能指标
-C 显示CPU使用情况
-d 显示磁盘使用情况 -k以KB为单位 -m以MB为单位 -g以GB为单位
-N 显示LVM信息
-x 显示详细信息
-p 显示分区情况
另外命令后面可以加2个数字，就是时间和次数比如：
iostat -d -m 2 5     以MB为单位显示磁盘使用情况，每2秒刷新一次，显示5次。

ps -ef 
ps -aux|grep chat.js
a:显示所有程序 
u:以用户为主的格式来显示 
x:显示所有程序，不以终端机来区分
用ps -def | grep查找进程很方便，最后一行总是会grep自己
用grep -v参数可以将grep命令排除掉
ps -aux|grep chat.js| grep -v grep


查看使用某端口的进程
查看进程:	ps -ef | grep 11000
lsof -i:8090
netstat -ap|grep 8090

netstat -ntlp  所有端口
lsof -i tcp:22  端口22

查看到进程id之后，使用netstat命令查看其占用的端口
netstat -nap|grep 5137

kill -9 2234    强制（-9）杀死进程2234

查看一下占用情况：  netstat -tulpn

#%% -----------------  nohup和&后台运行，进程查看及终止
nohup
用途：不挂断地运行命令
&
用途：在后台运行
一般两个一起用
nohup command &



----------------------------------------- bash shell ----------------------------------------
#%% -----------------  linux之if [ $? -ne 0 ]
[ $? -ne 0 ]
$?是shell变量,表示"最后一次执行命令"的退出状态.0为成功,非0为失败.
-ne 是不等于
这个语句的意思是“如果shell的启动参数不等于0个”

$# 表示提供到shell脚本或者函数的参数总数；
$1 表示第一个参数.


另外：
整数比较
-eq     等于,如:if ["$a" -eq "$b" ]
-ne     不等于,如:if ["$a" -ne "$b" ]
-gt     大于,如:if ["$a" -gt "$b" ]
-ge    大于等于,如:if ["$a" -ge "$b" ]
-lt      小于,如:if ["$a" -lt "$b" ]
-le      小于等于,如:if ["$a" -le "$b" ]
<  小于(需要双括号),如:(("$a" < "$b"))
<=  小于等于(需要双括号),如:(("$a" <= "$b"))
>  大于(需要双括号),如:(("$a" > "$b"))
>=  大于等于(需要双括号),如:(("$a" >= "$b"))

