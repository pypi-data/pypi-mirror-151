# development_time_predict
### Install package:
```
pip install icmodel
```
### Usage:
```
import icmodel
# Load data
test_data = sc.read_h5ad('DATA/PATH')
# Predict time
test_data = icmodel.Predict(test_data,pred='development time',NN=True,n=5)
# Predict celltype
test_data = icmodel.Predict(test_data,pred='cell type')
```