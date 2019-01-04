#!/usr/bin/python
# -*- coding:utf-8 -*-

from sklearn.pipeline import Pipeline,FeatureUnion
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import StandardScaler

from toolkits.nlp import myclass_tendency
from toolkits.nlp.utils import DataFrameSelector

#%%
def get_feature_tendency(title_content, label):
	'''
	倾向性模型特征
	
	title_content： [title1 + content1, title2 + content2, ......]
		shape: (n_samples, 1)
	'''
	pipeline = Pipeline([
	    ('features', FeatureUnion([
	        ('tf_idf', Pipeline([
	            ('counts', CountVectorizer(max_df=0.95, min_df=2)),
	            ('tf_idf', TfidfTransformer()),
	            ('chi', SelectKBest(chi2, k=20000))
	        ])),
	        ('len_stats', myclass_tendency.StatsFeatures_tendency()),
	    ])),
	    ('standard', StandardScaler(with_mean=False))
		])

	feature_pipeline = pipeline.fit(title_content, label)
	X_features = feature_pipeline.transform(title_content)
	print('X_features: ', X_features.shape)

	return feature_pipeline, X_features, label    

#%%
def get_feature_tendency_title(title_or_content, label):
	'''
	倾向性模型特征，标题和正文分开作为特征
	
	title_or_content = np.array([[t,c] for t,c in zip(title, content)])
	title_or_content [[title1, content1], [title2, content2], ......]
		shape: (n_samples, 2)
	'''
	step1_1 = Pipeline([('title_sel', DataFrameSelector([0])), 
	                    ('title_features', myclass_tendency.StatsFeatures_tendency())])
	step1_2 = Pipeline([('content_sel', DataFrameSelector([1])), 
	                    ('content_features', FeatureUnion([
					        ('tf_idf', Pipeline([
					            ('counts', CountVectorizer(max_df=0.95, min_df=2)),
					            ('tf_idf', TfidfTransformer()),
					            ('chi', SelectKBest(chi2, k=20000))
					        ])),
					        ('len_stats', myclass_tendency.StatsFeatures_tendency()),
					    ]))])

	pipeline = Pipeline([('cal_features', FeatureUnion(transformer_list=[
	                                                ("title_fea", step1_1),
	                                                ("content_fea", step1_2),])),
	                     ('standard', StandardScaler(with_mean=False))
	                 	])

	feature_pipeline = pipeline.fit(title_or_content, label)
	X_features = feature_pipeline.transform(title_or_content)
	print('X_features: ', X_features.shape)

	return feature_pipeline, X_features, label