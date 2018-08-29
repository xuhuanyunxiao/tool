
class StatsFeatures_cor(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        self.neg = set() # 负面词
        f = open("corpus/neg_words.txt","r+", encoding='UTF-8')
        for content in f:
            self.neg.add(content.strip())
        f.close()
        
        self.company = set() # 公司
        f = open("corpus/insurance_company_20180803.txt","r+", encoding='UTF-8')
        for content in f:
            self.company.add(content.strip())
        f.close()

        self.regulators = set() # 监管机构及领导
        f = open("corpus/insurance_regulators_20180804.txt","r+", encoding='UTF-8')
        for content in f:
            self.regulators.add(content.strip())
        f.close()        
        
    def fit(self, X, y=None):
        return self

    def getcnt(self,x):        
        return len(list(set(x)))

    def getnegcnt(self,x):
        ''' 计算负面词词频 '''
        negcnt = 0
        words = x.split()
        for w in words:
            if w in self.neg:
                negcnt = negcnt+1
        return negcnt
    
    def getorgcnttf(self,x):
        ''' 计算公司、机构词频 '''
        companycnt=0
        companytf=0
        regcnt = 0
        regtf = 0
        
        words = x.split()
        words_set=set(words)
        for w in words_set:
            if w in self.company:
                companycnt = companycnt+1
                companytf=companytf+words.count(w)
                
            if w in self.regulators:
                regcnt = regcnt+1
                regtf=regtf+words.count(w)            
                
        return companycnt, companytf, regcnt, regtf
    
    def transform(self, X):
        data = []
        for x in X:
            if len(x) == 0:
                length  = 1
            else :
                length = len(x)
            companycnt, companytf, regcnt, regtf=self.getorgcnttf(x)
            data.append([len(x),self.getcnt(x),self.getcnt(x)/length,
                         self.getnegcnt(x),self.getnegcnt(x)/length,
                         companycnt, companytf, regcnt, regtf])            
        return data


class Statskeywords(BaseEstimator, TransformerMixin):
    
    def __init__(self, topk = 100):
        self.topk = topk
        self.keywords = set()  # 各类关键词：textrank算法选取
        f = open("corpus/keywords.txt","r+", encoding='UTF-8')
        num = 0
        for content in f:
            if num < topk:
                self.keywords.add(content.strip().replace('\n', ''))
            num += 1
        f.close() 
        
        #初始化字典liwc
        self.liwc = {} 
        f2 = open("corpus/scliwc.txt",'r', encoding = 'gb18030')
        for ii in f2:     #ii在scliwc.txt中循环
            i = ii.strip().split() 
            self.liwc[i[0]] = i[1:len(i)]
        f2.close      
        
        self.category = set()
        for i in list(self.liwc.values()):
            for j in i:
                self.category.add(j) 
    
    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        '''
        文本中关键词的词频
        '''                        
        data = []
        for x in X:
            words = x.split()
            word_tf = []
            keycnt = 0
            for kw in self.keywords:
                word_tf.append(words.count(kw)) # 各个关键词的词频
                if kw in words:keycnt+=1
            word_tf.append(keycnt) # 关键词的个数
            
            tw_tf = []
            for tw in self.otherwords:
                tw_tf.append(words.count(tw))
            
            psy = []
            for w in words:
                if w in self.liwc: #是否liwc字典包含分词结果列表words的哪些分词
                    psy += self.liwc[w]                      
            cat_tf = []
            for cat in self.category:
                cat_tf.append(psy.count(cat))                
                
            data.append(word_tf + tw_tf + cat_tf)            
        return data        



pipeline = Pipeline([
    ('features', FeatureUnion([
        # 使用文本的 tf_idf 作为特征，并用卡方检验挑选一定数量的形成特征向量（k = 20000)
        ('tf_idf', Pipeline([
            ('counts', CountVectorizer(max_df=0.95, min_df=2)), # 词袋，选取词频大于1，且词在所有文档中出现的比例小于0.95
            ('tf_idf', TfidfTransformer()),  # 计算 tf-idf 
            ('chi', SelectKBest(chi2, k=20000)) # 卡方检验
        ])),   
        # 内容特征：计算 文本长度、词的个数、去重后的词所占比例、公司个数、公司总次数、机构个数、机构总次数等
        ('len_stats', StatsFeatures_cor()),
        # 使用 textrank 算法对每类挑选一定数量的词作为特征，这些词在所有类中出现的次数小于4，再用卡方检验挑选。
        ('tf', Pipeline([
            ('tf_k', Statskeywords(topk = 2000)),  # 各类关键词的词频
            ('chi', SelectKBest(chi2, k=500))])), # 卡方检验
    ])),
    ('standard', StandardScaler(with_mean=False)),
    ('classifier', XGBClassifier(max_depth=7,objective='multi:softmax', num_class=8))
])

pipeline.fit(X_train, y_train)
print(pipeline.score(X_train, y_train))
pipeline





<<<<<<< HEAD
=======



>>>>>>> 7d6db793841c9e6d26ea9396856d3da7ba6e9fcd
