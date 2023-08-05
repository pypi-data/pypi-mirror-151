"""
".命令"pro 子程序模块
# 子程序标准模块

本模块为".命令"pro 版本的

"""

__authon__  ="梦境中雨"
__version__ ="2.2.0.2"

from . import error
from . import run_load

from sys import exit as _exit
def run(version,authon,name)->tuple:# 初始化读取消息
    """".命令" pro读取初始启动头的内容
    version:插件版本
    authon:作者
    name:软件名"""
    print("load_run_msg") # 获取启动信息
    server=input()
    if server=="upgrade":
        print(version)
        print(authon)
        print(name)
        server=int(input())
    else:
        server=int(server)
    password=int(input())
    port=int(input())
    dot_version=int(input())
    return server,password,port,dot_version
def exit()->None:# 结束子程序
    """".命令" pro 结束运行的功能"""
    print("exit")
    _exit()
    