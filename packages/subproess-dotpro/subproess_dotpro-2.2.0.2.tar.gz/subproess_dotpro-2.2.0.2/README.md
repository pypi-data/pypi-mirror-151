本库作为 ".命令" pro 的子程序基础包
因此您可以使用本库做与".命令"pro相匹配的子程序
子程序的实现不限制编程语言，你只需要能让".命令"系统本体明白你的意思即可

基础函数:
    subproess_dotpro.run()
        获取".命令"pro的启动信息：
        返回:
            server:租赁服号：int
            password:租赁服密码:int
            port:该租赁服号的启动端口:int
            dot_version:".命令"系统的启动版本:str
    subproess_dotpro.exit()
        结束子程序
        返回值:None


