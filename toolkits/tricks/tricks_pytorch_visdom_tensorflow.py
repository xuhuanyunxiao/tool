
#%% -----------------     pytorch  ----------------------
import torch
from torch.nn import Linear
from torch import nn
import torch as t
t.__version__

#%% ----------------- tensor
b = t.Tensor([[1,2,3],[4,5,6]])
b.tolist() # 把tensor转为list
b_size = b.size()
t.ones(2, 3)
t.zeros(2, 3)
t.arange(1, 6, 2)
t.linspace(1, 10, 3)
t.randn(2, 3, device=t.device('cpu'))
t.randperm(5) # 长度为5的随机排列
t.eye(2, 3, dtype=t.int) # 对角线为1, 不要求行列数一致

a = t.arange(0, 6)
a.view(2, 3)
b = a.view(-1, 3) # 当某一维为-1的时候，会自动计算它的大小
b.unsqueeze(1) # 注意形状，在第1维（下标从0开始）上增加“１”
 #等价于 b[:,None] 
b[:, None].shape
b.unsqueeze(-2) # -2表示倒数第二个维度
c = b.view(1, 1, 1, 2, 3)
c.squeeze(0) # 压缩第0维的“１”
c.squeeze() # 把所有维度为“1”的压缩
a[1] = 100
b # a修改，b作为view之后的，也会跟着修改
b.resize_(3, 3) # 旧的数据依旧保存着，多出的大小会分配新空间

#%% ----------------- tensor and numpy
# 将numpy变量转化为tensor
x_train = torch.from_numpy(x_train)
x_train = x_train.float()

predict = predict.data.numpy()

#%% ----------------- 损失函数和优化函数
# 定义损失函数和优化函数
criterion = nn.CrossEntropyLoss() # 交叉熵损失函数
# criterion = nn.MSELoss() # 均方损失函数
optimizer = torch.optim.SGD(model.parameters(), lr = 1e-3)

####  损失函数
# torch.nn.L1Loss(reduce=False, size_average=False) #  L1 损失
# torch.nn.SmoothL1Loss(reduce=False, size_average=False) # Huber Loss
# torch.nn.MSELoss(reduce=False, size_average=False) # 均方损失函数
# torch.nn.BCELoss(reduce=False, size_average=False) # 二分类用的交叉熵，用的时候需要在该层前面加上 Sigmoid 函数
# # loss = loss_fn(F.sigmoid(input), target)
# # nn.BCEWithLogitsLoss # nn.BCELoss 加一个 Sigmoid 层
# torch.nn.CrossEntropyLoss(reduce=False,   # 多分类用的交叉熵损失函数
#                           size_average=False, 
#                           weight=weight)
# nn.NLLLoss # 用于多分类的负对数似然损失函数
# nn.KLDivLoss # 相对熵，算的是两个分布之间的距离，越相似则越接近零
# nn.MarginRankingLoss # 评价相似度的损失

# nn.MultiMarginLoss # 多分类（multi-class）的 Hinge 损失
# nn.MultiLabelMarginLoss
# # 多类别（multi-class）多分类（multi-classification）的 Hinge 损失，是上面 MultiMarginLoss 在多类别上的拓展。
# nn.SoftMarginLoss # 多标签二分类问题
# nn.MultiLabelSoftMarginLoss # 多标签多分类版本

# nn.CosineEmbeddingLoss # 余弦相似度的损失，目的是让两个向量尽量相近
# nn.HingeEmbeddingLoss
# nn.TripleMarginLoss

# nn.PoissonNLLLoss  # 适合多目标分类

#%% ----------------- 激活函数
# Torch的激励函数都在torch.nn.functional中，relu,sigmoid, tanh, softplus都是常用的激励函数。
y_relu = F.relu(x_variable).data.numpy() 
y_sigmoid = F.sigmoid(x_variable).data.numpy() 
y_tanh = F.tanh(x_variable).data.numpy() 
y_softplus = F.softplus(x_variable).data.numpy() 

#%% ----------------- 优化器


# 将模型变成测试模式
model.eval() 



#%% ----------------- GPU
if torch.cuda.is_available():
    model = LinearRegression().cuda()
else :
    model = LinearRegression()

# Tensor可通过.cuda 方法转为GPU的Tensor，从而享受GPU带来的加速运算。
# 在不支持CUDA的机器下，下一步还是在CPU上运行
device = t.device("cuda:0" if t.cuda.is_available() else "cpu")
x = x.to(device)

#%% ----------------- 持久化
# Tensor的保存和加载十分的简单，使用t.save和t.load即可完成相应的功能。
# 在save/load时可指定使用的pickle模块，在load时还可将GPU tensor映射到CPU或其它GPU上。

# 通过t.save(obj, file_name)等方法保存任意可序列化的对象，然后通过obj = t.load(file_name)方法加载保存的数据。
# 对于Module和Optimizer对象，这里建议保存对应的state_dict，而不是直接保存整个Module/Optimizer对象。
# Optimizer对象保存的主要是参数，以及动量信息，通过加载之前的动量信息，能够有效地减少模型震荡，下面举例说明。

# ----- 保存整个模型的结构信息和参数信息
if t.cuda.is_available():
    a = a.cuda(1) # 把a转为GPU1上的tensor,
    t.save(a,'a.pth')

    # 加载为b, 存储于GPU1上(因为保存时tensor就在GPU1上)
    b = t.load('a.pth')
    # 加载为c, 存储于CPU
    c = t.load('a.pth', map_location=lambda storage, loc: storage)
    # 加载为d, 存储于GPU0上
    d = t.load('a.pth', map_location={'cuda:1':'cuda:0'})

# ----- 保存模型参数
# Module对象的保存与加载
t.save(model.state_dict(), 'squeezenet.pth')
model.load_state_dict(t.load('squeezenet.pth'))


#%% -----------------     visdom  ----------------------
import visdom
vis = visdom.Visdom()
assert vis.check_connection()

#%% ----------------- 安装与启动
# 安装：pip install visdom
# 启动：python -m visdom.server (-port 9100)
#     nohup python3 -m visdom.server -port 9100 &
#     http://192.168.30.220:9100
# 浏览器：localhost:8097
#     http://192.168.0.104:8097

#     可用参数：
#         -port：运行服务器的端口。
#         -env_path：重新加载序列化会话的路径。
#         -logging_level：记录级别（默认=INFO）。接受标准文本和数字记录值。

#%% ----------------- 可视化接口
# vis.scatter : 2D 或 3D 散点图
# vis.line : 线图
# vis.stem : 茎叶图
# vis.heatmap : 热力图
# vis.bar : 条形图
# vis.histogram: 直方图
# vis.boxplot : 箱型图
# vis.surf : 表面图
# vis.contour : 轮廓图
# vis.quiver : 绘出二维矢量场
# vis.mesh : 网格图

# vis.image : 图片
# vis.images : list of images
# vis.text : 文本
# vis.save : 序列化状态
# vis.properties : properties grid
# vis.audio : audio
# vis.video : videos
# vis.svg : SVG object
# vis.matplot : matplotlib plot

# vis.close : 通过ID关闭一个窗口
# vis.delete_env : delete an environment by env_id
# vis.win_exists : 通过id检查一个窗口是否已经存在
# vis.get_env_list : get a list of all of the environments on your server
# vis.win_hash: get md5 hash of window's contents
# vis.get_window_data: get current data for a window
# vis.check_connection: 检查服务器是否连接
# vis.replay_log: replay the actions from the provided log file

vis = visdom.Visdom()
trace = dict(x=[1, 2, 3], y=[4, 5, 6], mode="markers+lines", type='custom',
             marker={'color': 'red', 'symbol': 104, 'size': "10"},
             text=["one", "two", "three"], name='1st Trace')
layout = dict(title="First Plot", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})

vis._send({'data': [trace], 'layout': layout, 'win': 'mywin'})

#%% ----------------- 通用的可视化options
# (除了plot.image和plot.text外）
#     opts.title : figure title
#     opts.width : figure width
#     opts.height : figure height
#     opts.showlegend : show legend (true or false)
#     opts.xtype : type of x-axis ('linear' or 'log')
#     opts.xlabel : label of x-axis
#     opts.xtick : show ticks on x-axis (boolean)
#     opts.xtickmin : first tick on x-axis (number)
#     opts.xtickmax : last tick on x-axis (number)
#     opts.xtickvals : locations of ticks on x-axis (table of numbers)
#     opts.xticklabels : ticks labels on x-axis (table of strings)
#     opts.xtickstep : distances between ticks on x-axis (number)
#     opts.ytype : type of y-axis ('linear' or 'log')
#     opts.ylabel : label of y-axis
#     opts.ytick : show ticks on y-axis (boolean)
#     opts.ytickmin : first tick on y-axis (number)
#     opts.ytickmax : last tick on y-axis (number)
#     opts.ytickvals : locations of ticks on y-axis (table of numbers)
#     opts.yticklabels : ticks labels on y-axis (table of strings)
#     opts.ytickstep : distances between ticks on y-axis (number)
#     opts.marginleft : left margin (in pixels)
#     opts.marginright : right margin (in pixels)
#     opts.margintop : top margin (in pixels)
#     opts.marginbottom: bottom margin (in pixels)

#%% ----------------- vis.scatter 2D或3D数据的散点图
vis = visdom.Visdom()
# 2D scatterplot with custom intensities (red channel)
vis.scatter(X=np.random.rand(255, 2),
            Y=(np.random.rand(255) + 1.5).astype(int),
            opts=dict(markersize=10,
                      markercolor=np.random.randint(0, 255, (2, 3,)),),)

#3D 散点图
Y = np.random.rand(100)
vis.scatter(X=np.random.rand(100, 3),Y=(Y + 1.5).astype(int),
            opts=dict(legend=['Men', 'Women'],markersize=5,))

#%% ----------------- 绘制随程序运行逐渐产生的值
vis = visdom.Visdom(env='my_wind')
x,y=0,0
win = vis.line(X=np.array([x]),Y=np.array([y]),
               opts=dict(title='two_lines'))
for i in range(1000):
    x+=i
    y+=i
    vis.line(X=np.array([x]),Y=np.array([y]),
        win=win,#win要保持一致
        update='append')

#%% -----------------     tensorboardx  ----------------------
#%% ----------------- 安装与启动
# 安装
    # pip install tensorboard
    # pip install tensorboardX
# 启动
    # tensorboard --logdir=tensorboard_log -host=127.0.0.1
    # http://127.0.0.1:6006

from tensorboardX import SummaryWriter
writer = SummaryWriter(log_dir='tensorboard_log/demo', 
						comment='demo')

# add_scalar
for epoch in range(100):
    writer.add_scalar('test', np.random.rand(), epoch)
    writer.add_scalars('scalars_test', 
                       {'xsinx': epoch * np.sin(epoch), 
                        'xcosx': epoch * np.cos(epoch)}, epoch)

writer.close()

# graph
model = Net1()
# with 语句，可以避免因w.close未写造成的问题
with SummaryWriter(log_dir='tensorboard_log/graph', comment='Net1') as w:
    w.add_graph(model, (dummy_input,))

writer.add_figure('matplotlib', fig)
writer.add_image('Image', x, n_iter)
writer.add_audio('myAudio', dummy_audio, n_iter, sample_rate=sample_rate)
writer.add_text('Text', 'text logged at step:' + str(n_iter), n_iter)
writer.add_pr_curve('xoxo', np.random.randint(2, size=100), np.random.rand(100), n_iter)
writer.add_embedding(out,metadata=label_batch.data,
						label_img=data_batch.data,
    					global_step=n_iter)
for name, param in resnet18.named_parameters():
    writer.add_histogram(name, param.clone().cpu().data.numpy(), n_iter)

#%% ----------------- GPU
from tensorboardX import SummaryWriter
import time
import torch

try:
    import nvidia_smi
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)  # gpu0
except ImportError:
    print('This demo needs nvidia-ml-py or nvidia-ml-py3')
    exit()

with SummaryWriter(log_dir='tensorboard_log/nvidia_smi', comment='nvidia_smi') as writer:
    x = []
    for n_iter in range(50):
        x.append(torch.Tensor(1000, 1000).cuda())
        res = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
        writer.add_scalar('nv/gpu', res.gpu, n_iter)
        res = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
        writer.add_scalar('nv/gpu_mem', res.used, n_iter)
        time.sleep(0.1)

#%% -----------------     tensorflow  ----------------------


















#%% -----------------     tensorboard  ----------------------
















