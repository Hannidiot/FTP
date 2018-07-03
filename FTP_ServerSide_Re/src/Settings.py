# 储存设置信息
Default_MaxFileSize = 50        # MB
Default_MaxFolderSize = 200     # MB
TimeOut = 300                   # s
HOST = 'localhost'
PORT = 9999
ADDR = (HOST, PORT)
PORT_LIST = [10000, 10001, 10002, 10003, 10004]
WorkDir = '/Users/hanniko/WorkSpace/FTP_Server'

# 功能配置信息
ALLOW_DELETE = False

# 匿名配置信息
ALLOW_ANONYMOUS = False
if ALLOW_ANONYMOUS:
    pass

# 默认用户信息
default_usr = [
    {
        "name": "admin",
        "passwd": "admin",
        "folder": "share",
        "MaxFileSize": -1,
        "MaxFolderSize": -1,
        "privilege": 50
    }
]
