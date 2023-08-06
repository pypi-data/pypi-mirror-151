import nmslib
import numpy as np
from scipy.sparse import issparse
def fastKnn(X1, 
            X2=None, 
            n_neighbors=20, 
            metric='euclidean', 
            M=40, 
            post=0, # Buffer memory error occur when post != 0
            efConstruction=100,
            efSearch=200):
    if metric == 'euclidean':
        metric = 'l2'
    if metric == 'cosine':
        metric = 'cosinesimil'
    if metric == 'jaccard':
        metric = 'bit_jaccard'
    if metric == 'hamming':
        metric = 'bit_hamming'
    # efConstruction: improves the quality of a constructed graph but longer indexing time
    index_time_params = {'M': M,
                         'efConstruction': efConstruction, 
                         'post' : post} 
    # efSearch: improves recall at the expense of longer retrieval time
    efSearch = max(n_neighbors, efSearch)
    query_time_params = {'efSearch':efSearch}
    
    if issparse(X1):
        if '_sparse' not in metric:
            metric = f'{metric}_sparse'
        index = nmslib.init(method='hnsw', space=metric, data_type=nmslib.DataType.SPARSE_VECTOR)
    else:
        index = nmslib.init(method='hnsw', space=metric, data_type=nmslib.DataType.DENSE_VECTOR)
    index.addDataPointBatch(X1)
    index.createIndex(index_time_params, print_progress=False)
    index.setQueryTimeParams(query_time_params)
    if X2 is None:
        neighbours = index.knnQueryBatch(X1, k=n_neighbors)
    else:
        neighbours = index.knnQueryBatch(X2, k=n_neighbors)
    
    distances = []
    indices = []
    for i in neighbours:
        if len(i[0]) != n_neighbors:
            vec_inds = np.zeros(n_neighbors)
            vec_dist = np.zeros(n_neighbors)
            vec_inds[:len(i[0])] = i[0]
            vec_dist[:len(i[1])] = i[1]
            indices.append(vec_inds)
            distances.append(vec_dist)        
        else:
            indices.append(i[0])
            distances.append(i[1])
    distances = np.vstack(distances)
    indices = np.vstack(indices)
    indices = indices.astype(np.int)
    if metric == 'l2':
        distances = np.sqrt(distances)
    
    return(distances, indices)
