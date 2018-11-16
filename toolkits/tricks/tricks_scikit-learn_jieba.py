#%% -----------------     jieba  ----------------------

# 基于TextRank算法进行关键词抽取
from jieba import analyse
# 引入TextRank关键词抽取接口
textrank = analyse.textrank
text = "线程是程序执行时的最小单位，它是进程的一个执行流，\
    是CPU调度和分派的基本单位，一个进程可以由很多个线程组成，\
    线程间共享进程的所有资源，每个线程有自己的堆栈和局部变量。\
    线程由CPU独立调度执行，在多CPU环境下就允许多个线程同时运行。\
    同样多线程也可以实现并发操作，每个请求分配一个线程来处理。"
 
keywords = textrank(text)

# 基于TF-IDF算法进行关键词抽取
from jieba import analyse
# 引入TF-IDF关键词抽取接口
tfidf = analyse.extract_tags
keywords = tfidf(text)


#%% -----------------     wordcloud  ----------------------

from wordcloud import WordCloud,STOPWORDS
import random

def random_color(word, font_size, position, orientation, random_state=None, **kwargs):
    return "#%06x" % random.randint(0, 0xFFFFFF)

# samsung_mask=np.array(Image.open('Samsung-Galaxy-Note-7.jpg'))
wordcloud_model = WordCloud(font_path = r'C:\Windows\Fonts\STKAITI.TTF', 
                      background_color='white',mode='RGB', # 背景颜色                      
                      # mask=back_coloring,  # 设置背景图片  mask=samsung_mask
                      max_words=1000,  # 词云显示的最大词数
                      random_state=42, max_font_size=60,  # 字体最大值
                      # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存
                      width=1000, height=860, 
                      margin=2,# margin为词语边缘距离
                     )

# wordcloud_res = wordcloud_model.generate(wordcloud_data)
# wordcloud_model.generate_from_frequencies(txt_freq)
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]

# image_colors = ImageColorGenerator(back_coloring)
# plt.imshow(wc.recolor(color_func=image_colors))
# plt.imshow(wordcloud.recolor(color_func=random_color))

for index, class_name in enumerate(list(np.unique(label))):
    wordcloud_data = " ".join([i for i,j in zip(title_content, label) if j == class_name])
    wordcloud_res = wordcloud_model.generate(wordcloud_data)
    plt.figure(figsize = (15,16))
    plt.title('%s Title = %s'%(index, class_name), fontsize = 30)
#     plt.imshow(wordcloud_res)
    plt.imshow(wordcloud_res.recolor(color_func=random_color))
    plt.axis("off")
    plt.show()
#     wordcloud.to_file('test.png')


#%% -----------------     scikit learn  ----------------------
#%% 加载数据集  ----------------------
from sklearn.datasets import load_iris
iris=load_iris()
iris.keys()
#dict_keys(['target', 'DESCR', 'data', 'target_names', 'feature_names'])
#数据的条数和维数
n_samples,n_features=iris.data.shape
print("Number of sample:",n_samples)  
#Number of sample: 150
print("Number of feature",n_features)
#Number of feature 4

# 文本特征  ----------------------
# 计算词频 --------
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
 
corpus = ["我 来到 北京 清华大学",
        "他 来到 了 网易 杭研 大厦",
        "小明 硕士 毕业 与 中国 科学院",
        "我 爱 北京 天安门"]
 
# token_pattern指定统计词频的模式, 不指定, 默认如英文, 不统计单字
vectorizer = CountVectorizer(token_pattern='\\b\\w+\\b')
# norm=None对词频结果不归一化（整数），默认归一化（小数）
# use_idf=False, 因为使用的是计算tfidf的函数, 所以要忽略idf的计算；默认计算 tf-idf
transformer = TfidfTransformer(norm=None, use_idf=False)
vec_count = vectorizer.fit_transform(corpus)
tf = transformer.fit_transform(vec_count )

word = vectorizer.get_feature_names()
weight = tf.toarray()
 
for i in range(len(weight)):
    for j in range(len(word)):
        print(word[j], ':', weight[i][j], end=' ', sep='')


# 分割测试集、训练集  ----------------------
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# 并行处理  ----------------------
# 整体并行处理 --------
# 　　pipeline包提供了FeatureUnion类来进行整体并行处理：
from numpy import log1p
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import Binarizer
from sklearn.pipeline import FeatureUnion
 
#新建将整体特征矩阵进行对数函数转换的对象
step2_1 = ('ToLog', FunctionTransformer(log1p))
#新建将整体特征矩阵进行二值化类的对象
step2_2 = ('ToBinary', Binarizer())
#新建整体并行处理对象
#该对象也有fit和transform方法，fit和transform方法均是并行地调用需要并行处理的对象的fit和transform方法
#参数transformer_list为需要并行处理的对象列表，该列表为二元组列表，第一元为对象的名称，第二元为对象
step2 = ('FeatureUnion', FeatureUnion(transformer_list=[step2_1, step2_2, step2_3]))

# 部分并行处理 --------
# 　　整体并行处理有其缺陷，在一些场景下，我们只需要对特征矩阵的某些列进行转换，而不是所有列。
#   pipeline并没有提供相应的类（仅OneHotEncoder类实现了该功能），需要我们在FeatureUnion的基础上进行优化：

# 对特征矩阵的第1列（花的颜色）进行定性特征编码，
# 对第2、3、4列进行对数函数转换，
# 对第5列进行定量特征二值化处理。
# 使用FeatureUnionExt类进行部分并行处理的代码如下：
from numpy import log1p
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import Binarizer
 
#新建将部分特征矩阵进行定性特征编码的对象
step2_1 = ('OneHotEncoder', OneHotEncoder(sparse=False))
#新建将部分特征矩阵进行对数函数转换的对象
step2_2 = ('ToLog', FunctionTransformer(log1p))
#新建将部分特征矩阵进行二值化类的对象
step2_3 = ('ToBinary', Binarizer())
#新建部分并行处理对象
#参数transformer_list为需要并行处理的对象列表，该列表为二元组列表，第一元为对象的名称，第二元为对象
#参数idx_list为相应的需要读取的特征矩阵的列
step2 = ('FeatureUnionExt', 
        FeatureUnionExt(transformer_list=[step2_1, step2_2, step2_3], 
                        idx_list=[[0], [1, 2, 3], [4]]))


from sklearn.pipeline import FeatureUnion, _fit_one_transformer, _fit_transform_one, _transform_one 
from sklearn.externals.joblib import Parallel, delayed
from scipy import sparse
import numpy as np
 
#部分并行处理，继承FeatureUnion
class FeatureUnionExt(FeatureUnion):
    #相比FeatureUnion，多了idx_list参数，其表示每个并行工作需要读取的特征矩阵的列
    def __init__(self, transformer_list, idx_list, n_jobs=1, transformer_weights=None):
        self.idx_list = idx_list
        FeatureUnion.__init__(self, transformer_list=map(lambda trans:(trans[0], trans[1]), transformer_list), 
            n_jobs=n_jobs, transformer_weights=transformer_weights)
 
    #由于只部分读取特征矩阵，方法fit需要重构
    def fit(self, X, y=None):
        transformer_idx_list = map(lambda trans, idx:(trans[0], trans[1], idx), 
            self.transformer_list, self.idx_list)
        transformers = Parallel(n_jobs=self.n_jobs)(
            #从特征矩阵中提取部分输入fit方法
            delayed(_fit_one_transformer)(trans, X[:,idx], y)
            for name, trans, idx in transformer_idx_list)
        self._update_transformer_list(transformers)
        return self
 
    #由于只部分读取特征矩阵，方法fit_transform需要重构
    def fit_transform(self, X, y=None, **fit_params):
        transformer_idx_list = map(lambda trans, idx:(trans[0], trans[1], idx), 
            self.transformer_list, self.idx_list)
        result = Parallel(n_jobs=self.n_jobs)(
            #从特征矩阵中提取部分输入fit_transform方法
            delayed(_fit_transform_one)(trans, name, X[:,idx], y,
                                        self.transformer_weights, **fit_params)
            for name, trans, idx in transformer_idx_list)
 
        Xs, transformers = zip(*result)
        self._update_transformer_list(transformers)
        if any(sparse.issparse(f) for f in Xs):
            Xs = sparse.hstack(Xs).tocsr()
        else:
            Xs = np.hstack(Xs)
        return Xs
 
    #由于只部分读取特征矩阵，方法transform需要重构
    def transform(self, X):
        transformer_idx_list = map(lambda trans, idx:(trans[0], trans[1], idx), 
            self.transformer_list, self.idx_list)
        Xs = Parallel(n_jobs=self.n_jobs)(
            #从特征矩阵中提取部分输入transform方法
            delayed(_transform_one)(trans, name, X[:,idx], self.transformer_weights)
            for name, trans, idx in transformer_idx_list)
        if any(sparse.issparse(f) for f in Xs):
            Xs = sparse.hstack(Xs).tocsr()
        else:
            Xs = np.hstack(Xs)
        return Xs

# pipeline ----------------------
import psutil
print ('获取内存占用率： '+(str)(psutil.virtual_memory().percent)+'%')

# Pipeline、FeatureUnion
# CountVectorizer、TfidfTransformer
# cv_results_、best_score_、best_params_ 、、、、
from sklearn.pipeline import Pipeline,FeatureUnion
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

# 流水线处理 --------
# pipeline包提供了Pipeline类来进行流水线处理。流水线上除最后一个工作以外，
# 其他都要执行fit_transform方法，且上一个工作输出作为下一个工作的输入。
# 最后一个工作必须实现fit方法，输入为上一个工作的输出；
# 但是不限定一定有transform方法，因为流水线的最后一个工作可能是训练！
from numpy import log1p
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import Binarizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
 
#新建计算缺失值的对象
step1 = ('Imputer', Imputer())
#新建将部分特征矩阵进行定性特征编码的对象
step2_1 = ('OneHotEncoder', OneHotEncoder(sparse=False))
#新建将部分特征矩阵进行对数函数转换的对象
step2_2 = ('ToLog', FunctionTransformer(log1p))
#新建将部分特征矩阵进行二值化类的对象
step2_3 = ('ToBinary', Binarizer())
#新建部分并行处理对象，返回值为每个并行工作的输出的合并
step2 = ('FeatureUnionExt', 
            FeatureUnionExt(transformer_list=[step2_1, step2_2, step2_3], 
                idx_list=[[0], [1, 2, 3], [4]]))
#新建无量纲化对象
step3 = ('MinMaxScaler', MinMaxScaler())
#新建卡方校验选择特征的对象
step4 = ('SelectKBest', SelectKBest(chi2, k=3))
#新建PCA降维的对象
step5 = ('PCA', PCA(n_components=2))
#新建逻辑回归的对象，其为待训练的模型作为流水线的最后一步
step6 = ('LogisticRegression', LogisticRegression(penalty='l2'))
#新建流水线处理对象
#参数steps为需要流水线处理的对象列表，该列表为二元组列表，第一元为对象的名称，第二元为对象
pipeline = Pipeline(steps=[step1, step2, step3, step4, step5, step6])

pipeline = Pipeline([
    ('features', FeatureUnion([
        ('tf_idf', Pipeline([
            ('counts', CountVectorizer()),
            ('tf_idf', TfidfTransformer()),
            ('chi', SelectKBest(chi2, k=20000))
        ])),
        ('tf', Pipeline([
            ('counts', CountVectorizer()),
            ('tf_idf', TfidfTransformer(use_idf=False))
        ])),
        ('len_stats', StatsFeatures())
    ])),
    ('classifier', XGBClassifier(max_depth=7,objective='multi:softmax', num_class=2))
])

pca = PCA(n_components=2)
selection = SelectKBest(k=1)
combined_features = FeatureUnion([("pca", pca), ("univ_select", selection)])
X_features = combined_features.fit(X, y).transform(X)
svm = SVC(kernel="linear")
pipeline = Pipeline([("features", combined_features), ("svm", svm)])
param_grid = dict(features__pca__n_components=[1, 2, 3],
                  features__univ_select__k=[1, 2],
                  svm__C=[0.1, 1, 10])
grid_search = GridSearchCV(pipeline, param_grid=param_grid, verbose=10)
grid_search.fit(X, y)

# 参数寻优：gridsearch、cv   --------
from sklearn.pipeline import Pipeline
>>> text_clf = Pipeline([('vect', CountVectorizer()),
...                      ('tfidf', TfidfTransformer()),
...                      ('clf', MultinomialNB()),
... ])
# 名称 vect, tfidf 和 clf （分类器）都是任意的。

# 命名规则：
pipeline = Pipeline([(‘tree‘, clf), ("svm", svm)])
param_test = dict(tree__min_samples_leaf=range(5, 16, 2), 
    tree__criterion=["gini","entropy"]，
    svm__C=[0.1, 1, 10])
# ‘tree‘(自己设定的名称)通过“__”连接estimator的参数（min_samples_leaf），range代表取值范围。

>>> from sklearn.model_selection import GridSearchCV
>>> parameters = {'vect__ngram_range': [(1, 1), (1, 2)], # 使用词袋或者二元模型
...               'tfidf__use_idf': (True, False),  # 使用或者不使用 idf
...               'clf__alpha': (1e-2, 1e-3),
... }

# 有多个 CPU，通过设置 n_jobs 参数可以进行并行处理。 
# 如果我们将该参数设置为 -1 ， 该方法会使用机器的所有 CPU 核心
>>> gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)

# 网格搜索的操作跟 scikit-learn 中常见的模型的操作是类似的。 
>>> gs_clf = gs_clf.fit(twenty_train.data[:400], twenty_train.target[:400])
>>> gs_clf.best_score_                                  
# 0.900...
>>> for param_name in sorted(parameters.keys()):
...     print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))
...
# clf__alpha: 0.001
# tfidf__use_idf: True
# vect__ngram_range: (1, 1)

# 交叉验证 --------
# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

scores = ['precision', 'recall']

# verbose： 如果为0则不输出日志，如果为1，则每隔一段时间输出日志，大于1输出日志会更频繁。
for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(SVC(), tuned_parameters, cv=5, verbose = 10， 
                       scoring='%s_macro' % score)
    clf.fit(X_train, y_train)

    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))


# 分类模型评价指标  ----------------------
from sklearn import metrics
# 准确率指所有分类正确的百分比
# 准确率的一个缺点是其不能表现任何有关测试数据的潜在分布。
print('accuracy_score: ', metrics.accuracy_score(lab, y_pred_class)) 
# 空准确率（null accuracy） 是指当模型总是预测比例较高的类别，那么其正确的比例是多少。
# calculate null accuracy(for binary classification problems coded as 0/1)
max(y_test.mean(), 1-y_test.mean())
# calculate null accuracy (for multi-class classification problems)
y_test.value_counts().head(1) / len(y_test)

# 考虑类不平衡问题，其中感兴趣的主类是稀少的。
# 即数据集的分布反映负类显著地占多数，而正类占少数。
# 故面对这种问题，需要其他的度量，评估分类器正确地识别正例数据的情况和正确地识别负例数据的情况。
print('recall_score: ', metrics.recall_score(lab, y_pred_class)) # 正确识别的正例数据在实际正例数据中的百分比
print('precision_score: ', metrics.precision_score(lab, y_pred_class)) # 标记为正类的数据实际为正例的百分比
print('precision_score: ', metrics.f1_score(lab, y_pred_class)) # 精度和召回率的方法组合
average_precision = metrics.average_precision_score(y_test, y_score)
print('Average precision-recall score: {0:0.2f}'.format(average_precision))
metrics.confusion_matrix(lab, y_pred_class)
#		 predict  0 （N）    1（P） 
# actual  0       12（TN）   13（FP）
#		  1       14（FN）   14（TP）
# 评估报告
print(metrics.classification_report(lab, y_pred_class))

precision, recall, thresholds = metrics.precision_recall_curve(lab, y_pred_class)
# AUC 值
f_pos, t_pos, thresh = metrics.roc_curve(lab, y_pred_class)
auc_area = metrics.auc(f_pos, t_pos)

# PRC 曲线
# 一条曲线（总和结果）
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
from sklearn.utils.fixes import signature

precision, recall, _ = precision_recall_curve(y_test, y_score)

# In matplotlib < 1.5, plt.fill_between does not have a 'step' argument
step_kwargs = ({'step': 'post'}
               if 'step' in signature(plt.fill_between).parameters
               else {})
plt.step(recall, precision, color='b', alpha=0.2,
         where='post')
# plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(
          average_precision))


def plotRUC(yt, ys, title=None):
    '''
    绘制ROC-AUC曲线
    :param yt: y真值
    :param ys: y预测值
    '''
    from sklearn import metrics
    from matplotlib import pyplot as plt
    f_pos, t_pos, thresh = metrics.roc_curve(yt, ys)
    auc_area = metrics.auc(f_pos, t_pos)
    print('auc_area: {}'.format(auc_area))

    plt.plot(f_pos, t_pos, 'darkorange', lw=2, label='AUC = %.2f' % auc_area)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.title('ROC-AUC curve for %s' % title)
    plt.ylabel('True Pos Rate')
    plt.xlabel('False Pos Rate')
    plt.show()
    plt.savefig(os.path.join(CWD, 'middlewares/roc-' + title + '.png'))

# 交叉验证 + 评分
from sklearn.model_selection import cross_val_score
clf = svm.SVC(kernel='linear', C=1)
scores = cross_val_score(clf, iris.data, iris.target, cv=5)
scores.mean()
# 对交叉验证方式进行指定，如验证次数，训练集测试集划分比例等
from sklearn.model_selection import ShuffleSplit
n_samples = iris.data.shape[0]
cv = ShuffleSplit(n_splits=3, test_size=.3, random_state=0)
cross_val_score(clf, iris.data, iris.target, cv=cv)
# 在cross_val_score 中同样可使用pipeline 进行流水线操作
from sklearn import preprocessing
from sklearn.pipeline import make_pipeline
clf = make_pipeline(preprocessing.StandardScaler(), svm.SVC(C=1))
cross_val_score(clf, iris.data, iris.target, cv=cv)


# 回归模型评价指标
print('平均绝对误差（MAE）：', metrics.mean_absolute_error(y_test, y_predict)) 
print('平均方差（MSE）：', metrics.mean_squared_error(y_test, y_predict)) 
print('R平方值：', metrics.r2_score(y_test, y_predict)) 
print('中值绝对误差：', metrics.median_absolute_error(y_test, y_predict)) 


# 稀疏数据转换 ----------------------
class DenseTransformer(TransformerMixin):

    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self

# 降维 ----------------------
# PCA 
from sklearn.decomposition import TruncatedSVD, SparsePCA, PCA

pca_1 = TruncatedSVD(n_components = 3) # 处理稀疏数据
data_pca_1 = pca_1.fit_transform(X_features)
print('-- TruncatedSVD: ')
print(pca_1.explained_variance_ratio_) # 降维后的各主成分的方差值占总方差值的比例
print(pca_1.explained_variance_) # 降维后的各主成分的方差值
print(data_pca_1.shape)
# print(data_pca_1)

pca_2 = PCA(n_components = 3, whiten = True)
data_pca_2 = pca_2.fit_transform(DenseTransformer().fit_transform(X_features))
print('-- PCA: ')
print(pca_2.explained_variance_ratio_)
print(pca_2.explained_variance_)
print(data_pca_2.shape)
data_pca_2

# LDA：判别分析、降维
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis(n_components=3)
lda.fit(X_features_dense, y_train)
feature_lda = lda.transform(X_features_dense)
print('-- lda: ')
print(feature_lda.shape)
# print("截距: ", lda.intercept_)
# print("系数: ", lda.coef_)
print("各维度的方差值占总方差值的比例: ", lda.explained_variance_ratio_) 
print("各维度的方差值之和占总方差值的比例: ", np.sum(lda.explained_variance_ratio_))
feature_lda









