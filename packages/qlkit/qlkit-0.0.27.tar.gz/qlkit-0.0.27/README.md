# What's PyKit

# road map

## v0.0.1

- ddd
- error
- database
- cmd

# DDD 说明
## ValueObject
## Entity
## DomainService
## Repository
## ApplicationService

# gRPC的处理

GrpcApplicationServer
XXGrpcServicer
XXApplicationService

GrpcApplicationServer 抽象了gRPC的应用服务器，负责管理gRPC进程的生命周期、gRPC的路由调度等。
XXGrpcServicer 符合gRPC规则的业务服务的gRPC处理器，gRPC会将请求路由到对应的方法中，进而执行业务代码。
XXApplicationService DDD 中的 ApplicationService的子类。
ApplicationService 的返回error或者是抛出异常决定了grpc的response处理逻辑。


```python

class XXGrpcServicer(xx_pb2_grpc.XXServicer):
    def __init__(self):
        self.application_service

    @grpc_execute        
    def usecase(self):
        self.application_service.usecase()
```

## 如何构建打包
首先需要 build 和 twine 两个模块：

```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

```
打包的操作：
首先要升级版本，setup.py 里面的 version 递增。
然后开始执行构建

```
python3 -m build
```

执行之后，在 dist/ 目录下就会有打包好的程序代码如下：

```
dist/qlkit-{version}-py3-none-any.whl
dist/qlkit-{version}.tar.gz
```

最后就是把包上传到 pipy 了：

```
python3 -m twine upload dist/*
```
