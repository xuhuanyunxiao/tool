

#%% -----------------     安装与导入  ----------------------
# 通过如下命令设定镜像
options(repos = 'http://mirrors.ustc.edu.cn/CRAN/')
# 查看镜像是否修改
getOption('repos')

# 安装与导入package
install.packages("pastecs")
remove.packages (c("pkg1" ,"pkg2") ,   # 卸载
			lib = file.path("path" , "to" , "library"))

if(!require(pastecs)){install.packages("pastecs")}
library('arules')

.libPaths()  # 能够显示库所在的位置， 
library()    # 可以显示库中有哪些包。

# 导入数据集
# R在datasets包中共提供了100个可以使用的数据集，这些数据集都可以通过 data() 函数加载入内存。
dim(data ()$ results )
data ()$ results [ ,4]
# arules 包自带数据集 Groceries
data(Groceries)
Groceries
class(Groceries)


#%% -----------------     设置与帮助  ----------------------
# R语言设置显示常用的命令是options 、format、signif等
# options主要是用来设置可以改变R的计算和显示结果全局选项。
# 如果用该命令后还是显示不全，则可以把变量转换成字符型然后再转换成数值型，再进行显示。
options(digits = 7)           # 控制要打印数值的位数（最大只能到22）
options(scipen = 100)     # 平时常用的数值或科学计数法输出，此处用于设置显示的位数


# 各种帮助
help.start()  # 查看帮助文档
 help.search("pattern")  # 搜索帮助文档
??pattern
 help(package="name") # 查看R软件包帮助信息
# 获取函数的帮助文档
help(functionname)  # 在网页中显示
?functionname # 在控制台显示
args(functionname) # 快速获取函数的参数
example(functionname) # 查看函数的实例























