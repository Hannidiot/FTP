class User(object):
    name = ''
    password = ''
    folder = 'share'
    max_file_size = 0
    max_folder_size = 0
    upload = False
    privilege = ''

    def __init__(self):
        pass

    def is_null(self):
        if self.name == '':
            return True
        return False

    def clear(self):
        self.name = ''
        self.password = ''
        self.folder = 'share'
        self.max_folder_size = 0
        self.max_file_size = 0
        self.upload = False

    def create(self, n, password, folder, upload, maxfilesz, maxfdsz):
        self.name = n
        self.password = password
        self.folder = folder
        self.upload = upload
        self.max_file_size = maxfilesz
        self.max_folder_size = maxfdsz


class UserList(object):
    _userlist = []

    def __init__(self, userlist):
        for i in userlist:
            pass