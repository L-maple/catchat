### 系统环境

Ubuntu18.04

Ubuntu18.04默认安装了Python3.6



### 环境安装

1. 安装pip3 和 pipenv

```shell
sudo apt install python3-pip
# 用"--user 用户名"来指定用户安装, 用"-i source"指定安装的程序源
sudo pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  pipenv --user maple
# 更新~/.profile文件，在~/.profile文件中添加pipenv的目录
python3 -m site --user-base  #Result: /home/maple/.local
vim ~/.profile
export PATH=$PATH:$HOME/.local/bin # 在~/.profile中最后一行添加
# 退出vim编辑器后，手动更新~/.profile
source ~/.profile
# 检验下pipenv安装成功
pipenv --version # Result: pipenv, version 2018.11.26
```

Note: 在我安装过程中pipenv --version失败, 提示

```
from pipenv import cli 
ModuleNotFoundError: No module named 'pipenv'
```

可能是因为权限的原因，后来运行以下命令后成功。

```shell
sudo chmod -R 777 ~/.local/lib
```

2. 创建虚拟环境

```shell
# 假设创建的项目目录为 letschat, 则可以在该目录中创建虚拟环境
cd letschat
pipenv install
# 使用pipenv shell显式地激活虚拟环境
pipenv shell  # Note: 当需要退出虚拟环境时，使用exit命令
```

3. 安装Flask

在我们刚刚创建的虚拟环境里安装Flask

```shell
pipenv install flask 
```

4. Pycharm（IDE）安装

访问 http://jetbrains.com/即可安装。



### 功能实现

#### 1. 注册/登录

##### 1.1 注册

功能说明：根据用户的email和密码来创建新的用户名。若email已存在，则注册出错。

##### 1.2 登录

功能说明：若用户已注册，可根据email和密码登录。

##### 1.3 退出

功能说明：退出用户登录，此时显示聊天室主界面。



#### 2. 聊天室

##### 2.1 聊天室创建

功能说明：根据用户输入的用户名进行创建新的聊天室。

##### 2.2 聊天室删除

功能说明：如果登录用户是该聊天室的所有者，可以删除该聊天室。

##### 2.3 聊天室进入

功能说明：若用户拥有该聊天室，可进入该聊天室。

##### 2.4 聊天室搜索

功能说明：用户可根据聊天室名，搜索相关的聊天室。

##### 2.5 聊天室成员显示

功能说明：显示该聊天室中所有成员。



#### 3. 在线人数统计

功能说明：统计目前该聊天室中登录的用户数量。



#### 4. 消息管理

##### 4.1 消息发送

功能说明：在聊天室中发送消息，该聊天室中所有用户都可接收该消息。

##### 4.2 消息撤回

功能说明：若用户是该消息的所有者，则可以删除该消息。

##### 4.3 匿名消息

功能说明：可以匿名发送消息。



#### 5. 用户信息管理

##### 5.1 信息获取

功能说明：获取该用户的基本信息。

##### 5.2 信息修改

功能：修改该用户的基本信息。

