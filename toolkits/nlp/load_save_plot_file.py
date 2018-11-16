#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.base import BaseEstimator, TransformerMixin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import seaborn as sns

colors = sns.color_palette("Set2", 8)

def title_content_label(filepath):
    title = []
    filename = filepath + 'titles.txt'
    fid = open(filename, "r+", encoding='UTF-8')
    for f in fid:
        title.append(f.strip().replace('\n', ''))
    fid.close()
    print('title num: ', len(title))
    print(title[:2])

    content = []
    filename = filepath + 'contents.txt'
    fid = open(filename, "r+", encoding='UTF-8')
    for f in fid:
        content.append(f.strip().replace('\n', ''))
    fid.close()
    print('content num: ', len(content))
    # content[:2]

    title_content = [t + ' ' + c for t,c in zip(title, content)]
    print('title_content num: ', len(title_content))

    label = []
    filename = filepath + 'labels.txt'
    fid = open(filename, "r+", encoding='UTF-8')
    for f in fid:
        label.append(f.strip().replace('\n', ''))
    fid.close()
    print('label num: ', len(label))
    print(label[:5])
    
    return title_content, label, title, content


def plot2(features, class_name_dict):
    # % matplotlib inline

    f = plt.figure(figsize=(15, 9))
    ax = f.add_subplot(111)
    
    a = 0
    for i in range(1,len(class_name_dict) + 1):
        if len(class_name_dict) == 2:
               a = 2
        ax.scatter(features[features['label']==i-a]['f1'],
                   features[features['label']==i-a]['f2'],
                   color=colors[i-1], label=i-a, alpha=.8) 
    
    ax.set_title("Truncated SVD, 2 Components")    
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    print(class_name_dict)
    
    plt.show()


def plot3(features, class_name_dict):    
    # % matplotlib notebook

    f = plt.figure(figsize=(15, 9))
    ax = f.add_subplot(111, projection='3d')  # 创建一个三维的绘图工程
    
    a = 0
    for i in range(1,len(class_name_dict) + 1):
        if len(class_name_dict) == 2:
               a = 2        
        ax.scatter(features[features['label']==i-a]['f1'],
                   features[features['label']==i-a]['f2'],
                   features[features['label']==i-a]['f3'],
                   color=colors[i-1], label=i-a, alpha=.8)

    ax.set_zlabel('f3')  # 坐标轴
    ax.set_ylabel('f2')
    ax.set_xlabel('f1')
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    print(class_name_dict)

    plt.show()


class DenseTransformer(TransformerMixin):
    '''sparse data to dense data'''

    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self
























