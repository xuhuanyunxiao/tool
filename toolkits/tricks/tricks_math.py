
#%% -----------------     概率论  ----------------------










#%% -----------------     统计学  ----------------------
import numpy as np
t = np.linspace(-6, 6, 20)
sin_t = np.sin(t)
cos_t = np.cos(t)

# 假设检验: 比较两个组  ----------------------
from scipy import stats
# 单样本 t-检验: 检验总体平均数的值
# scipy.stats.ttest_1samp()检验数据总体的平均数是否可能等于给定值 
# (严格来说是否观察值来自于给定总体平均数的正态分布)。
# 它返回一个T统计值以及p-值 (见函数的帮助):
stats.ttest_1samp(data['VIQ'], 0)
(30.088099970849328, 1.3289196468728067e-28)

# 双样本 t-检验: 检验不同总体的差异 scipy.stats.ttest_ind()
# 我们已经看到男性和女性总体VIQ平均数是不同的。要检验这个差异是否是显著的，
female_viq = data[data['Gender'] == 'Female']['VIQ']
male_viq = data[data['Gender'] == 'Male']['VIQ']
stats.ttest_ind(female_viq, male_viq)
(-0.77261617232750113, 0.44452876778583217)

# 配对实验: 同一个体的重复测量
# PIQ、VIQ和FSIQ给出了IQ的3种测量值。让我检验一下FISQ和PIQ是否有显著差异。
stats.ttest_ind(data['FSIQ'], data['PIQ'])
(0.46563759638096403, 0.64277250094148408)
# 使用这种方法的问题是忘记了两个观察之间有联系: 
# FSIQ 和 PIQ 是在相同的个体上进行的测量。因此被试之间的差异是混淆的，
# 并且可以使用"配对实验"或"重复测量实验"来消除。
stats.ttest_rel(data['FSIQ'], data['PIQ'])
(1.7842019405859857, 0.082172638183642358)
# 这等价于单样本的差异检验:
stats.ttest_1samp(data['FSIQ'] - data['PIQ'], 0)
(1.7842019405859857, 0.082172638183642358)

# T-tests假定高斯误差。我们可以使用威尔科克森符号秩检验, 放松了这个假设:
stats.wilcoxon(data['FSIQ'], data['PIQ'])
(274.5, 0.10659492713506856)
# 注意: 非配对实验对应的非参数检验是曼惠特尼U检验, scipy.stats.mannwhitneyu()。
# 男性和女性重量的差异。
# 使用非参数检验来检验男性和女性VIQ的差异。
# 结论: 我们发现数据并不支持男性和女性VIQ不同的假设。


#%% -----------------     线性代数  ----------------------









#%% -----------------     微积分  ----------------------

