class Exit(Exception):#定义退出模块
    pass
class loadError(Exception):#读取超时
    pass
class ToolateError(Exception):#获取超时
    pass
class MsgError(Exception):#获取消息错误
    pass
class HelpError(Exception):#获取帮助超时
    pass