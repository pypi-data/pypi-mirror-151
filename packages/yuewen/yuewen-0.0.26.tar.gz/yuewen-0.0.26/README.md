# yuewen

#### 介绍
阅文工具箱

#### 软件架构
软件架构说明


#### 安装教程

1.  pip安装
```shell script
pip install yuewen
```
2.  pip安装（使用阿里镜像加速）
```shell script
pip install yuewen -i https://mirrors.aliyun.com/pypi/simple
```

#### 使用说明

1.  demo
```python
import yuewen
test_res = yuewen.get_menu(cookie='test')
```

2. 参数含义
```text
coop_id：合作方式代码
    1：微信分销
    9：陌香快应用（共享包）
    11：快应用（独立包）

```
