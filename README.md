# Flask后端

## 项目架构

```python
- app
  - auth #蓝图模块:用户登录验证
    - __init__.py
    - forms.py #表单验证
    - views.py #视图文件,已被弃用,新的路由在resources中定义      
  - libs 
	- error.py #定义异常处理对象
    - error_code.py #自定义异常逻辑处理
  - model #存储数据库
	- auth_user.py #管理用户信息的数据库
  - resources
    - __init__.py   
    - user_api.py #处理Api接口的后端逻辑
  - __init__.py #工厂模式创建Flask应用
- .gitnore
- app_helloWorld.py #启动应用的主程序
- requirements.txt #项目依赖
- config.py #应用配置
- Dorkerfile #Dorker配置文件
- guni.conf.py #gunicorn配置文件
- string_convert.py #无用的文件,忽略
```

## 快速开始

1. `git clone`项目到本地
2. 创建虚拟环境，根据`requirements.txt`安装依赖
3. `python app_helloWorld.py`启动应用

## 部署到服务器上

采用Docker进行容器化部署，目前在服务上已部署Flask容器和MySQL容器

#### 在更新项目后重新部署

本地端：

1. 更新docker镜像：`sudo docker build -t flask_project .`
2. push到docker hub：`sudo docker push flask_project`，项目名称要与docker hub上的仓库名称相同

服务器端：

1. 暂停当前容器：`sudo docker stop flask_container`
2. 删除当前容器：`sudo docker rm flask_container`
3. 拉取新镜像：`sudo docker pull flask_project`
4. 启动新容器：`sudo docker run -itd --name flask -p 5005:5005 --link mysql:mysql kingyaaayaaa/myflask`

#### 容器化部署`Flask`的相关配置

##### `gunicorn` + `gevent`库

编辑配置，确定端口为`5005`，项目的`__init__.py`中配置的5001端口将会失效

```python
# guni.conf.py
workers = 5
worker_class = "gevent"
bind = "0.0.0.0:5005"
```

##### 使用Docker封装应用

```dockerfile
# Dorkerfile
FROM python:3.8 
# WORKDIR： 文件在容器中的存储路径
WORKDIR /Flask/demo  

COPY requirements.txt ./
RUN pip install -r requirements.txt 

COPY . .

CMD ["gunicorn", "app_helloWorld:app", "-c", "./guni.conf.py"]
```

#### 容器化部署`MySQL`的相关配置

##### docker拉取`MySQL`仓库，导入/创建数据库表

`sudo docker run -itd --name mysql -p 3303:3306 -e MYSQL_ROOT_PASSWORD=windyword2023 mysql `

`sql`数据库：**user_test**；`sql`数据库表：user

`sql`用户名：root；`sql`密码：`windyword2023`

`sql`容器名和端口：`mysql:3306`；映射到宿主机和端口：`localhost:3303`

```mysql
# 将项目文件中的data.sql拷贝到MySQL容器中
docker cp test_user.sql mysql:/root
# 进入MySQL容器
docker exec -it mysql /bin/bash
# 连接数据库
mysql -uroot -p
# 创建数据库
#create database 数据库名 default charset=utf8mb4;
create database user_test default charset=utf8mb4;
# 导入data.sql
use user_test;
source test_user.sql;
```

##### `Flask`连接`MySQL`

`sudo docker run -itd --name flask -p 5005:5005 --link mysql:mysql kingyaaayaaa/myflask`

```python
#config.py
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:windyword2023@mysql:3306/user_test?charset=utf8mb4'

```

##### `nginx`反向代理 

`Nginx`所在目录：`usr/local/nginx/conf/nginx.conf`

设定`url`为：`https://windyword.com/testflask/`

**成功的访问界面**

![image-20230614162049156](../AppData/Roaming/Typora/typora-user-images/image-20230614162049156.png)

