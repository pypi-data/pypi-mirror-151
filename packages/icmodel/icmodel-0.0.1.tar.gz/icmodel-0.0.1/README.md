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
### Build Docker image:
Install Docker:[tutorial](https://yeasy.gitbook.io/docker_practice/install)
```
 cd development_time_predict
 docker build -t time-predict:v1 .
 # Successfully built xxxxxxxxx
 # Successfully tagged time-predict:v1
 docker run --name task_name -u $(id -u):$(id -g) -p $port:8888 -it -v /local/path:/home/jovyan/work time-predict:v1
```
