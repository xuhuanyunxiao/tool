#!/usr/bin/python
# -*- coding:utf-8 -*-

from sklearn.pipeline import Pipeline,FeatureUnion
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import StandardScaler    

from toolkits.nlp import myclass_cor
from toolkits.nlp.utils import DataFrameSelector

#%%
def get_feature_cor_circ(title_content, label):
	'''
	保监会：相关模型特征

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
	        ('len_stats', myclass_cor.StatsFeatures_cor_circ()),
	        ('tf', myclass_cor.Statskeywords_cor(topk = 5000,types = 'circ'))
	    ])),
	    ('standard', StandardScaler(with_mean=False))
		])

	feature_pipeline = pipeline.fit(title_content, label)
	X_features = feature_pipeline.transform(title_content)
	print('X_features: ', X_features.shape)

	return feature_pipeline, X_features, label

# from sklearn.externals import joblib
# joblib.dump(pipeline_train, "model/circ_pipeline_20181105.pkl.z")
# joblib.dump(X_features, "model/circ_features_20181105.pkl.z")
# joblib.dump(label, "model/circ_labels_20181105.pkl.z")

#%%
def get_feature_cor_title_circ(title_or_content, label):
	'''
	保监会：相关模型特征，标题和正文分开作为特征

	title_or_content [[title1, content1], [title2, content2], ......]
		shape: (n_samples, 2)
	'''
	step1_1 = Pipeline([('title_sel', DataFrameSelector([0])), 
	                    ('title_features', myclass_cor.StatsFeatures_cor_circ())])
	step1_2 = Pipeline([('content_sel', DataFrameSelector([1])), 
	                    ('content_features', FeatureUnion([
					        ('tf_idf', Pipeline([
					            ('counts', CountVectorizer(max_df=0.95, min_df=2)),
					            ('tf_idf', TfidfTransformer()),
					            ('chi', SelectKBest(chi2, k=20000))
					        ])),
					        ('len_stats', myclass_cor.StatsFeatures_cor_circ()),
	        				('tf', myclass_cor.Statskeywords_cor(topk = 5000,types = 'circ'))
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

#%%
def get_feature_cor_clic(title_content, label):
	'''
	中国人寿：相关模型特征

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
	        ('len_stats', myclass_cor.StatsFeatures_cor_circ()),
	        ('tf', myclass_cor.Statskeywords_cor(topk = 5000, types = 'clic')),
	        ('clic_tf', myclass_cor.StatsFeatures_tf_clic()),
	    ])),
	    ('standard', StandardScaler(with_mean=False))
		])

	feature_pipeline = pipeline.fit(title_content, label)
	X_features = feature_pipeline.transform(title_content)
	print('X_features: ', X_features.shape)

	return feature_pipeline, X_features, label

#%%
def get_feature_cor_title_clic(title_or_content, label):
	'''
	中国人寿：相关模型特征，标题和正文分开作为特征

	title_or_content [[title1, content1], [title2, content2], ......]
		shape: (n_samples, 2)
	'''
	step1_1 = Pipeline([('title_sel', DataFrameSelector([0])), 
	                    ('title_features', myclass_cor.StatsFeatures_cor_circ())])
	step1_2 = Pipeline([('content_sel', DataFrameSelector([1])), 
	                    ('content_features', FeatureUnion([
					        ('tf_idf', Pipeline([
					            ('counts', CountVectorizer(max_df=0.95, min_df=2)),
					            ('tf_idf', TfidfTransformer()),
					            ('chi', SelectKBest(chi2, k=20000))
					        ])),
					        ('len_stats', myclass_cor.StatsFeatures_cor_circ()),
	        				('tf', myclass_cor.Statskeywords_cor(topk = 5000,types = 'clic')),
	        				('clic_tf', myclass_cor.StatsFeatures_tf_clic()),
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

#%%
def get_feature_cor_picc(title_content, label):
	'''
	中国人保：相关模型特征

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
	        ('len_stats', myclass_cor.StatsFeatures_cor_circ()),
	        ('tf', myclass_cor.Statskeywords_cor(topk = 5000, types = 'picc')),
	        ('picc_tf', myclass_cor.StatsFeatures_tf_picc()),
	    ])),
	    ('standard', StandardScaler(with_mean=False))
		])

	feature_pipeline = pipeline.fit(title_content, label)
	X_features = feature_pipeline.transform(title_content)
	print('X_features: ', X_features.shape)

	return feature_pipeline, X_features, label

#%%
def get_feature_cor_title_picc(title_or_content, label):
	'''
	中国人保：相关模型特征，标题和正文分开作为特征

	title_or_content [[title1, content1], [title2, content2], ......]
		shape: (n_samples, 2)
	'''
	step1_1 = Pipeline([('title_sel', DataFrameSelector([0])), 
	                    ('title_features', myclass_cor.StatsFeatures_cor_circ())])
	step1_2 = Pipeline([('content_sel', DataFrameSelector([1])), 
	                    ('content_features', FeatureUnion([
					        ('tf_idf', Pipeline([
					            ('counts', CountVectorizer(max_df=0.95, min_df=2)),
					            ('tf_idf', TfidfTransformer()),
					            ('chi', SelectKBest(chi2, k=20000))
					        ])),
					        ('len_stats', myclass_cor.StatsFeatures_cor_circ()),
	        				('tf', myclass_cor.Statskeywords_cor(topk = 5000,types = 'picc')),
	        				('picc_tf', myclass_cor.StatsFeatures_tf_picc()),
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

#%%
def get_feature_cor_cbrc(title_content, label):
	'''
	银监会：相关模型特征

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
	        ('len_stats', myclass_cor.StatsFeatures_cor_cbrc()),
	        ('tf', myclass_cor.Statskeywords_cor(topk = 5000,types = 'cbrc'))
	    ])),
	    ('standard', StandardScaler(with_mean=False))
		])

	feature_pipeline = pipeline.fit(title_content, label)
	X_features = feature_pipeline.transform(title_content)
	print('X_features: ', X_features.shape)

	return feature_pipeline, X_features, label

#%%
def get_feature_cor_title_cbrc(title_or_content, label):
	'''
	银监会：相关模型特征，标题和正文分开作为特征

	title_or_content [[title1, content1], [title2, content2], ......]
		shape: (n_samples, 2)
	'''
	step1_1 = Pipeline([('title_sel', DataFrameSelector([0])), 
	                    ('title_features', myclass_cor.StatsFeatures_cor_cbrc())])
	step1_2 = Pipeline([('content_sel', DataFrameSelector([1])), 
	                    ('content_features', FeatureUnion([
					        ('tf_idf', Pipeline([
					            ('counts', CountVectorizer(max_df=0.95, min_df=2)),
					            ('tf_idf', TfidfTransformer()),
					            ('chi', SelectKBest(chi2, k=15000))
					        ])),
					        ('len_stats', myclass_cor.StatsFeatures_cor_cbrc()),
	        				('tf', myclass_cor.Statskeywords_cor(topk = 5000,types = 'cbrc'))
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