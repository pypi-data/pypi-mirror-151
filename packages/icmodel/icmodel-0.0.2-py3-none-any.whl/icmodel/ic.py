import lightgbm as lgb
import os
import scanpy as sc
import pandas as pd
import numpy as np
import scipy as sci
import json
from sklearn import preprocessing
import tqdm
from . import fastkNN
from scipy import sparse
import warnings
import pkg_resources
warnings.filterwarnings('ignore')

ct_npy_path = pkg_resources.resource_filename("icmodel", "model/Cell_Type_Classification.npy")
celltype_label = np.load(file=ct_npy_path,allow_pickle=True)
label_coder = preprocessing.LabelEncoder()
label_coder.fit_transform(celltype_label)
def load_model(pred):
    '''
    :param pred: choose predict 'cell type' or 'development time'
    :return: time_model or celltype model
    '''

    if pred == 'development time':
        use_model = lgb.Booster(model_file=pkg_resources.resource_filename("icmodel", "model/Cell_Develop_Time_Prediction.model"))
        return use_model
    elif pred == 'cell type':
        use_model = lgb.Booster(model_file=pkg_resources.resource_filename("icmodel", "model/Cell_Type_Classification.model"))
        return use_model
    else:
        raise Exception("Invalid predicted type", pred)

def preprocess_data(raw_data,model,normalize):
    '''
    :param raw_data: anndata
    :param model: LightGBM model
    :param normalize: choose to normalize or not,default is True
    :return: dataframe
    '''
    use_model = model
    use_feature = use_model.feature_name()
    data = raw_data
    if normalize:
        sc.pp.normalize_total(data, target_sum=1e4)
        sc.pp.log1p(data)
    pre_data = data[:,data.var_names.isin(use_feature)]
    if sparse.issparse(pre_data.X):
        df = pd.DataFrame(pre_data.X.A)
    else:
        df = pd.DataFrame(pre_data.X)
    df.index = pre_data.obs_names.tolist()
    df.columns = pre_data.var_names.tolist()
    difference = list(set(use_feature).difference(set(pre_data.var_names)))
    for i in difference:
        df[i] = 0
    print(len(difference),"of",len(use_feature),"genes not in the data, will set to zero!")
    return df[use_feature]


def smooth_time(time_df,data,neighb = None,use_col='Predict_time',n=5):
    '''
    calculate mean of N nearest neigbors predicted time
    '''
    from tqdm import tqdm
    #from sklearn.neighbors import NearestNeighbors
    time_dict={}
    for i in range(len(time_df)):
        time_dict[str(i)] = time_df[use_col][i]
    result=[]
    if neighb == None:
        print('Calculating neighbors......')
        nb= fastkNN.fastKnn(X1=data,n_neighbors=n)[1]
    else:
        nb = neighb
    for i in tqdm(range(len(nb))):
        neighbor = nb[i]
        temp=[]
        for j in neighbor:
            temp.append(time_dict.get(str(j)).tolist())
        result.append(np.mean(temp))
    return result

def Predict(data,pred='development time',normalize=True,NN=False,neighb=None,n=5):
    '''
    :param data: anndata
    :param pred: choose predict 'cell type' or 'development time'
    :param normalize: choose to normalize or not,default is True
    :return: anndata
    '''
    use_model = load_model(pred)
    data_df = preprocess_data(data, use_model, normalize=normalize)
    if pred == 'development time':
        data.obs['Predict_time'] = use_model.predict(data_df)
        if NN:
            data.obs['Predict_timeNN'] = smooth_time(data.obs,data.obsm['X_pca'],neighb=neighb,n=n)
        return data
    elif pred == 'cell type':
        result = use_model.predict(data_df)
        result_transform = transform_label(result,label_coder)
        data.obs['Predict_celltype'] = result_transform[0]
        data.obs['Predict_celltype_proba'] = result_transform[1]
        return data




##########################################################################################################
def build_celltype_trainning_data(adata,colname='celltype_annotation_20210507',max_cell_number=100):
    '''
    细胞类型数据集采样
    :param adata: 原始的anndata
    :param colname: 细胞注释列名
    :param max_cell_number: 每种细胞类型采样上限
    :return:采样后的anndata文件
    '''
    sampling_cells = []
    indice = np.arange(adata.shape[0])
    # 不同时间点随机抽样：
    for i in adata.obs[colname].unique():
        sub_indice = indice[adata.obs[colname].isin([i]).values]
        if len(sub_indice) > max_cell_number:
            np.random.seed(111)
            rds = np.random.choice(len(sub_indice), max_cell_number, replace=False)  # 细胞数下采样
            sampling_cells += list(sub_indice[rds])
        else:
            sampling_cells += list(sub_indice)
    sampling_cells = np.unique(sampling_cells)
    adata.obs['random_down_sampling'] = pd.Series(indice).isin(sampling_cells).values
    return adata[adata.obs['random_down_sampling']==True]

def build_celltime_trainning_data(adata,colname='celltype_annotation_20210507',max_cell_number=100):
    '''
    不同细胞类型不同时期采样
    :param adata: 原始的anndata
    :param colname: 细胞注释列名
    :param max_cell_number: 每种细胞类型每个时期的采样上限
    :return: 采样后的anndata文件
    '''
    total_sampling_cells = []
    # 不同cell type时间点随机抽样：
    for i in adata.obs[colname].unique():
        print(i)
        adata_time = adata[adata.obs[colname] == i]
        indice = np.arange(adata_time.shape[0])
        sampling_cells = []
        for j in adata_time.obs["embryonic_period"].unique():
            sub_indice = indice[adata_time.obs["embryonic_period"].isin([j]).values]
            if len(sub_indice) > max_cell_number:
                np.random.seed(111)
                rds = np.random.choice(len(sub_indice), max_cell_number, replace=False)  # 细胞数下采样
                sampling_cells.extend(list(sub_indice[rds]))
            else:
                sampling_cells.extend(list(sub_indice))
        sampling_cells = np.unique(sampling_cells)
        adata_time.obs['random_down_sampling'] = pd.Series(indice).isin(sampling_cells).values
        subindex = adata_time[adata_time.obs['random_down_sampling'] == True].obs.index.tolist()
        total_sampling_cells.extend(subindex)
    adata.obs['random_down_sampling'] = adata.obs.index.isin(total_sampling_cells)
    return adata[adata.obs['random_down_sampling'] == True]

def transform_label(result,label_coder,filter_prob=0):
    '''
    :param result: lightgbm predict result
    :param label_coder: cell type label_coder
    :param filter_prob: less than filter_prob will set to 'unknown'
    :return: cell type label list and celltype proba
    '''
    celltype = []
    celltype_proba = []
    ind = []
    for i in tqdm.tqdm(range(len(result))):
        celltype.append(result[i].argmax())
        celltype_proba.append(result[i].max())
        if result[i].max() < filter_prob:
            ind.append(i)
    ct_result = label_coder.inverse_transform(celltype).astype(str)
    ct_result[ind] = 'unknown'
    return ct_result,celltype_proba

def top_n(prob,label_coder,n=3):
    '''
    预测的前n个值,输入为概率值矩阵,输出一个字典
    :param prob: 概率值矩阵
    :param label_coder: 模型的标签对应的编码器
    :param n: 概率值排序前n个
    :return: 概率值排序前n个的label
    '''
    final = {}
    for i in tqdm.tqdm(range(len(prob))):
        idx = np.argpartition(prob[i], -n)[-n:]
        indices = idx[np.argsort((-prob[i])[idx])]
        label = label_coder.inverse_transform(indices)
        final[str(i+1)]=label
    return final

def celltype_NN_vote(pred_prob,data,n=5):
    '''
    最近邻校正
    :param pred_prob: top_n的结果，概率值排序前n的标签矩阵
    :param data: 处理后的表达矩阵
    :param n: 最近邻数
    :return: 最近邻投票后的标签列表
    '''
    from tqdm import tqdm
    #from sklearn.neighbors import NearestNeighbors
    from collections import Counter
    result=[]
    nb= fastkNN.fastKnn(X1=data,n_neighbors=n)[1]
    for i in tqdm(range(len(nb))):
        neighbor = nb[i]
        temp=[]
        temp.extend(pred_prob.get(str(i+1)).tolist()) #添加自己的信息
        for j in neighbor:
            temp.extend(pred_prob.get(str(j+1)).tolist())
        max_counts = Counter(temp)
        top_one = max_counts.most_common(1)[0][0]
        result.append(top_one)
    return result
