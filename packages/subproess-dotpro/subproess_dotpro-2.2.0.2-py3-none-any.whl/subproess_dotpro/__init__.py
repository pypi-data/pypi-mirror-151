"""
".命令"pro 子程序模块
# 子程序标准模块

本模块为".命令"pro 版本的

"""

__authon__  ="梦境中雨"
__version__ ="2.2.0.2"
import asyncio
import websockets
from sys import exit as _exit
from sys import argv as argv_list
from . import error
from . import run_load




def run(version,authon,name)->tuple:# 初始化读取消息
    """".命令" pro读取初始启动头的内容
    version:插件版本
    authon:作者
    name:软件名
    port:主程序提交的端口"""
    if len(argv_list) !=5:
        _exit()
    else:
        server =int(argv_list[1])
        password =int(argv_list[2])
        dot_version =argv_list[3]
        port = int(argv_list[4])
        return server,password,dot_version,port
def exit()->None:# 结束子程序
    """".命令" pro 结束运行的功能"""
    print("exit")
    _exit()
    