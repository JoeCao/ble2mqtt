# Ble2mqtt
### 收集指定mac地址的蓝牙信标的广播消息，加上rssi信息发送到mqtt服务中
- 目前只适配树莓派。在Raspberry Pi 4 / Raspberry Pi Zero 上测试通过
- 操作系统版本Raspbian buster

### 下载代码
<code>
  git clone https://github.com/JoeCao/ble2mqtt.git
</code>

### 安装

安装必要的依赖，为了加速，可以切换为阿里云的apt源
````shell
sudo nano /etc/apt/sources.list
````
进入编辑界面，注释掉原来的内容，将下列内容加入
````shell
deb http://mirrors.aliyun.com/raspbian/raspbian/ buster main non-free contrib rpi
deb-src http://mirrors.aliyun.com/raspbian/raspbian/ buster main non-free contrib rpi
````
更新软件索引清单
````shell
  sudo apt-get update
````
然后执行代码目录下的install.sh
````shell
  sh install.sh
````
安装pip
````shell
  sudo apt-get install python-pip
````
安装python依赖
````shell
sudo pip install -r requirements.txt
````
### 修改为自己的mqtt服务器
````shell
nano scan.py
````
找到 
````python
client.connect
````
后面的部分修改

### 运行
````shell
  sh start.sh
````
### 停止
````shell
  sh stop.sh
````
