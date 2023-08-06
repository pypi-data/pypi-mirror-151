# easyfc使用介绍

### 1.  开发目的
    简化云函数开发的代码量，方便开发人员迅速组织云开发服务

### 2.  快速开始
方式1： 使用pip进行安装
```shell
pip install easyfc
```
方式2： 自行下载安装

打开[pipy](https://pypi.org/project/easyfc/)
下载.whl文件或者.tar.gz 文件安装
![下载位置](./1.png)

### 3. 演示使用
    (1)获取含有json的请求数据
```python
from easyfc.parse import get_json
environ = {} # environ是函数入口提供的参数
jsonParams = get_json(environ)
```
    (2)获取请求头内参数
```python
from easyfc.parse import get_headers
environ = {} # environ是函数入口提供的参数
params = get_headers(environ)
```
    (3)获取请求query
```python
from easyfc.parse import get_params
environ = {} # environ是函数入口提供的参数
params = get_params(environ)
```
    (4) 返回200状态并且返回文本
```python
from easyfc.response import ok_text_start_response
def handler(environ):
   return ok_text_start_response()
```