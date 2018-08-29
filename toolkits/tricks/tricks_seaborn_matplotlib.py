# -*- coding: utf-8 -*-

#%% -----------------     seaborn  ----------------------
import seaborn as sns

sns.distplot(data, bins = 500)        # kde 密度曲线  rug 边际毛毯

g = sns.PairGrid(distance_data_1)
g.map_upper(plt.scatter)
g.map_lower(sns.regplot)
g.map_diag(sns.kdeplot)

sns.jointplot(x="company_regis_capital", y="exist_days", 
              data=pd.concat([distance_data_4, distance_data_5], axis = 1), 
              kind="reg")

def plot_stat_fig(data_1,data_2,data_3,data_4,data_5,kind = 'boxplot'):
    fig = plt.subplots(figsize = (16,12))
    gs = gridspec.GridSpec(2,16)
    fontsize = 30
    label_fontsize = 25
    ticklabel_fontsize = 15

    def get_plot(data, title = None, kind = 'barplot'):
        if kind == 'barplot':
            sns.barplot(data = data, ax=ax)   
        elif kind == 'boxplot':
            sns.boxplot(data = data, ax=ax) 
        elif kind == 'violinplot':
            sns.violinplot(data = data, ax=ax)         
        elif kind == 'stripplot':
            sns.stripplot(data = data, ax=ax, jitter=True) 
        ax.set_title(title, fontsize = fontsize)

    for i in range(5):
        i = i + 1
        if i == 1 :
            ax = plt.subplot(gs[0,:])
            # sns.barplot(data = distance_data_1, ax=ax)
            get_plot(data_1, title = 'd_1', kind = kind)            
        elif i == 2:
            ax = plt.subplot(gs[1,:6])
            get_plot(data_2, title = 'd_2', kind = kind)
            ax.set_ylabel('Mean', fontsize = label_fontsize)
        elif i == 3:
            ax = plt.subplot(gs[1,6:12])
            get_plot(data_3, title = 'd_3', kind = kind)
            ax.set_title('d_3', fontsize = fontsize) 
        elif i == 4:
            ax = plt.subplot(gs[1,12:14])
            get_plot(data_4, title = 'd_4', kind = kind)
        elif i == 5:
            ax = plt.subplot(gs[1,14:])
            get_plot(data_5, title = 'd_5', kind = kind)

        setp(ax.get_yticklabels(), fontsize = ticklabel_fontsize)
        ax.set_xticks(ax.get_xticks() - [0.5])
        setp(ax.get_xticklabels(), fontsize = ticklabel_fontsize, rotation = 45)
        ax.tick_params(width = 0,length = 0)    

    plt.subplots_adjust(left=None, bottom=None, right=None, 
                        top=None, wspace = 6, hspace = 0.6) 
    plt.show()    

# 相关
fig, ax = plt.subplots(figsize=(22, 15))
cmap = sns.diverging_palette(220, 20, n=20)
sns.heatmap(distance_data.corr(), cmap = cmap,
            annot = True, annot_kws={'size':8, 'weight':'bold', 'color':'blue'}, 
            cbar = True, cbar_kws ={'orientation':'vertical',
                                    'pad':0.005, 'fraction':0.45}, 
            vmax = 1, vmin = -1, linewidths=.5, fmt="0.2f")
plt.yticks(fontsize = 15)
plt.xticks(fontsize = 15)

# colorbar
cax = plt.gcf().axes[-1]
cax.tick_params(labelsize = 10, direction = 'out', 
                length = 6, width = 2, color = 'r') # tick & ticklabel



#%% -----------------     matplotlib  ----------------------
%matplotlib inline  # jupyter notebook 中显示图片
import matplotlib.pyplot as plt  
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
from matplotlib.artist import setp

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 可旋转三维散点图
%matplotlib notebook  #  notebook  与 inline
def plot3(features):    
    % matplotlib notebook
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import seaborn as sns

    colors = sns.color_palette("Set2", 8)
    f = plt.figure(figsize=(15, 9))
    ax = f.add_subplot(111, projection='3d')  # 创建一个三维的绘图工程

    for i in range(1,9):
        ax.scatter(features[features['label']==i]['f1'],
                   features[features['label']==i]['f2'],
                   features[features['label']==i]['f3'],
                   color=colors[i-1], label=class_name_dict[i], alpha=.8)

    ax.set_zlabel('f3')  # 坐标轴
    ax.set_ylabel('f2')
    ax.set_xlabel('f1')
    plt.legend(loc='best', shadow=False, scatterpoints=1)

    plt.show()

    

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = np.random.randint(0, 255, size=[40, 40, 40])

x, y, z = data[0], data[1], data[2]
ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
#  将数据点分成三部分画，在颜色上有区分度
ax.scatter(x[:10], y[:10], z[:10], c='y')  # 绘制数据点
ax.scatter(x[10:20], y[10:20], z[10:20], c='r')
ax.scatter(x[30:40], y[30:40], z[30:40], c='g')

ax.set_zlabel('Z')  # 坐标轴
ax.set_ylabel('Y')
ax.set_xlabel('X')
plt.show()


#%% 中文相关
def set_ch():
    '''
    功能：设定绘图时显示中文
    ''' 
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题
set_ch()

# 图片保存


# 在柱状图上添加值标签
    values = d['importance'].tolist()
    ylocs = np.arange(len(values))
    for x, y in zip(values, ylocs):
        ax.text(x + 0.01, y, x, va='center')

ax.text(x, y, s, fontdict=None, withdash=False, **kwargs)
rects1 = plt.bar(index, scores[0], bar_width, color='#0072BC', label=names[0])  
def add_labels(rects):  
    for rect in rects:  
        height = rect.get_height()  
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')  
        # horizontalalignment='center' plt.text(x坐标，y坐标，text,位置)  
        # 柱形图边缘用白色填充，为了更加清晰可分辨  
        rect.set_edgecolor('white')  
  
add_labels(rects1)  


def cluster_plot(d, k): 
    '''
    自定义作图函数来显示聚类结果  
    '''
    plt.figure(figsize = (8, 3))  
    for j in range(0, k):  
        plt.plot(data[d==j], [j for i in d[d==j]], 'o')  
    
    plt.ylim(-0.5, k-0.5)  
    return plt  
  
cluster_plot(d1, k).show()  

def plot_color_table(data, fontsize = 10):
    '''
    显示带颜色的表格
    data： DataFrame
    '''
    vals = np.around(data.values,3)
    normal = colors.Normalize(vals.min()-1, vals.max()+1)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, frameon=True, xticks=[], yticks=[])
    ax.spines['top'].set_visible(False) #去掉上边框
    ax.spines['bottom'].set_visible(False) #去掉下边框
    ax.spines['left'].set_visible(False) #去掉左边框
    ax.spines['right'].set_visible(False) #去掉右边框
    
    the_table=plt.table(cellText=vals, cellLoc='center', 
                        cellColours=plt.cm.Blues(normal(vals)), 
                        rowLabels=data.index,  rowColours=None, rowLoc='left', 
                        colLabels=data.columns,colColours=None, colLoc='center', 
                        colWidths = None, 
                        loc='center', bbox=[0, 0, int(data.shape[1]/5) + 1, 
                                            int(data.shape[0]/5) + 1] )  
                                        # [left, bottom, width, height]\
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(fontsize)

def plot_bar_table(rows, cols, col_list, rawdata):
    #rows = 2
    #cols = 3
    num = 0

    fig,axs = plt.subplots(rows,cols, figsize = (15,12))

    for i in range(rows):
        for j in range(cols):
            if num < len(col_list):
                col = col_list[num]
                data = rawdata[col].value_counts().sort_index()

                col_labels = ['Freq']
                row_labels = [[x] for x in data.index.tolist()]
                table_vals = [[x] for x in data.values.tolist()]
                row_colors = sns.diverging_palette(220, 20, n = data.shape[0]) 

                my_table = axs[i,j].table(cellText=table_vals, colWidths=[0.2],
                                     rowLabels=row_labels, colLabels=col_labels,
                                     rowColours=row_colors, loc='best',
                                         )#bbox = [0.5,0.6,0.3,0.3]

                axs[i,j].bar(data.index.tolist(), 
                             data.values.tolist(), 
                             color = row_colors, width = 0.3)
                axs[i,j].set_title(col, fontsize = 20)
                # setp(ax.get_yticklabels(), fontsize = ticklabel_fontsize)
                # axs[i,j].set_xticks(axs[i,j].get_xticks() - [0.5])
                setp(axs[i,j].get_xticklabels(), fontsize = 10, rotation = 45)
                axs[i,j].tick_params(width = 0,length = 0)             

                num += 1

    plt.subplots_adjust(left=None, bottom=None, right=None, 
                        top=None, wspace = None, hspace = 0.4) 
    plt.show()


def get_plot_data(data,gender,value_name):    
    useful_data = data[data['性别'] == gender].drop(['性别'],axis = 1)        
    tuples = useful_data.columns.tolist()
    tupless = [i for i in tuples if (i[1] == value_name) |(i[0] =='年级')|(i[0] =='年龄')|(i[0] =='学段')]
    useful_data = useful_data.reindex(columns=pd.MultiIndex.from_tuples(tupless))
    
    plot_data = np.array(useful_data)
    plot_data = plot_data[:,1:]

    return plot_data

def get_color_names(xlabel):
#    color_sequence1 = ['#800000', '#FF0000', '#D87093',# 栗色/大红/浅紫红
#              '#FFC0CB', '#CCCC99','#FF8C00',# 粉红/重褐色/深橙色
#              '#BA55D3', '#228B22', '#228B22',# 中紫色/绿色/森林绿
#              '#99CC33', '#008B8B','#000000'] # 间海蓝色/深青色/黑
                       
#2010: 重褐色 #8B4513   2011:秘鲁色 #CD853F  2012：原木色 #DEB887   
#2013:蓟色 #D8BFD8  2014：紫罗兰 #EE82EE  
#2015:石蓝色 #6A5ACD  2016:深洋红色 #8B008B                       
                       
    color_sequence1 = ['#8B4513', '#CD853F', '#DEB887',# 栗色/大红/浅紫红
              '#D8BFD8', '#EE82EE','#6A5ACD',# 粉红/重褐色/深橙色
              '#8B008B', '#228B22', '#228B22',# 中紫色/绿色/森林绿
              '#99CC33', '#008B8B','#000000'] # 间海蓝色/深青色/黑
                       
                       
    color_sequence2 = color_sequence1[:9]   
    legend_names1 = ['一年级','二年级','三年级','四年级','五年级','六年级',
         '初一','初二','初三','高一','高二','高三']
    legend_names2 = ['2010', '2011', '2012', '2013', '2014', '2015', '2016']
    # legend_names3 = ['小学', '中学']
    legend_names3 = ['小学低年级', '小学中年级', '小学高年级', '初中', '高中']

    if xlabel == '年份':
        return color_sequence1,legend_names1
    elif xlabel == '学段':
        return color_sequence1,legend_names3
    else :
        return color_sequence2,legend_names2
    
def get_x_axis(fig, ax,xlabel,data):    
    color_sequence, legend_names = get_color_names(xlabel)    
    if xlabel == '年级':
        ax.set_xlim(1, 13)    
        plt.xticks(range(0, 14, 1), fontsize=14)
        ax.set_xticklabels(['','一年级','二年级','三年级','四年级','五年级','六年级',
                '初一','初二','初三','高一','高二','高三',''])
        plt.xlabel('年级', fontsize=16, ha='center')
        for index,item in enumerate(legend_names):
            plt.plot(np.arange(1,13,1),data[:,index],lw = 1.5,
                     color=color_sequence[index],label = legend_names[index])
    elif xlabel == '年龄':
        ax.set_xlim(1, 15)    
        plt.xticks(range(0, 15, 1), fontsize=14)
        ax.set_xticklabels(['','6','7','8','9','10','11',
                '12','13','14','15','16','17','18','19',''])        
        plt.xlabel('年龄', fontsize=16, ha='center')
        for index,item in enumerate(legend_names):
            plt.plot(np.arange(1,15,1),data[:,index],lw = 1.5,
                     color=color_sequence[index],label = legend_names[index])
    elif xlabel == '年份':
        ax.set_xlim(2010, 2017)    
        plt.xticks(range(2010, 2017, 1), fontsize=14)
        plt.xlabel('年份', fontsize=16, ha='center')    
        for index,item in enumerate(legend_names):
            plt.plot(np.arange(2010,2017,1),data[index,:],lw = 1.5,
                     color=color_sequence[index],label = legend_names[index])
    elif xlabel == '学段':
        ax.set_xlim(2010, 2017)    
        plt.xticks(range(2010, 2017, 1), fontsize=14)
        plt.xlabel('年份', fontsize=16, ha='center')    
        for index,item in enumerate(legend_names):
            plt.plot(np.arange(2010,2017,1),data[index,:],lw = 1.5,
                     color=color_sequence[index],label = legend_names[index])
            
    ax.legend(loc='best', shadow=True,fontsize=14) 
    return fig,ax    

def get_y_axis(fig, ax,fea_name,value_name,plot_data):
    if fea_name == '身高':
        threshold = [190,180]       
        ax.set_ylim(100, threshold[g-1])
        plt.yticks(np.arange(100, threshold[g-1], 10), fontsize=14)    
        ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))  
        plt.ylabel(fea_name, fontsize=16, ha='center')
    elif fea_name == '体重':
        threshold = [85,75]       
        ax.set_ylim(10, threshold[g-1])
        plt.yticks(np.arange(10, threshold[g-1], 5), fontsize=14)    
        ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))  
        plt.ylabel(fea_name, fontsize=16, ha='center')
    elif fea_name == 'BMI':
        threshold = [25,25]       
        if value_name == '均值':
            ax.set_ylim(12, threshold[g-1])
            plt.yticks(np.arange(12, threshold[g-1], 1), fontsize=14)    
            ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))  
            plt.ylabel('BMI 值', fontsize=16, ha='center')
        elif value_name == '肥胖率':
            ax.set_ylim(0, 55)
            plt.yticks(np.arange(0, 55, 5), fontsize=14)    
            ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))  
            plt.ylabel('肥胖比例', fontsize=16, ha='center')
            plot_data = plot_data * 100
    elif fea_name == '肺活量': 
        threshold = [4500,3500]            
        if value_name == '均值':
            ax.set_ylim(0, threshold[g-1])
            plt.yticks(np.arange(0, threshold[g-1], 500), fontsize=14)    
            ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))  
            plt.ylabel('肺活量', fontsize=16, ha='center')
        elif value_name == '不及格率':
            ax.set_ylim(0, 35)
            plt.yticks(np.arange(0, 35, 5), fontsize=14)    
            ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))  
            plt.ylabel('不合格比例', fontsize=16, ha='center')
            plot_data = plot_data * 100         
    elif fea_name == '视力':                        
        threshold = [4500,3500]       
        if value_name == '均值':
            ax.set_ylim(0, threshold[g-1])
            plt.yticks(np.arange(0, threshold[g-1], 500), fontsize=14)    
            ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))  
            plt.ylabel('视力', fontsize=16, ha='center')
        elif value_name == '检出率':
            ax.set_ylim(0, 105)
            plt.yticks(np.arange(0, 110, 10), fontsize=14)    
            ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}%'.format))  
            plt.ylabel('检出率', fontsize=16, ha='center')
            plot_data = plot_data * 100            
            
    return fig, ax,plot_data

def sta_plot(data,xlabel,g,fea_name,value_name,title,filename):
    plot_data = get_plot_data(data,g,value_name)
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 9))    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    plt.grid(True, 'major', 'x', ls='--', lw=.5, c='k', alpha=.3)

    fig, ax,plot_data = get_y_axis(fig, ax,fea_name,value_name,plot_data)
    fig, ax = get_x_axis(fig, ax,xlabel,plot_data)
           
    fig.suptitle(title, fontsize=18, ha='center')        
    plt.savefig(filename, bbox_inches='tight')
    plt.show()    
