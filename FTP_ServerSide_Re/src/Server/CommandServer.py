import socketserver
import json
import os

from src.Settings import *
from src.utility.Log import logger
from src.utility.Folder import *
from src.utility.MsgTranStandardize import *
from src.Server.FileTransServer import *

with open(os.path.join(WorkDir, "user.json"), 'r') as f:
    userList = json.load(f)
username_list = [a['name'] for a in userList]
main_path = os.path.join(WorkDir, "File")
print(userList)


class CommandServer(socketserver.ThreadingTCPServer):
    pass


class CommandHandler(socketserver.BaseRequestHandler):
    log_data = {'ip': "null", 'user': 'no user'}
    cur_path = os.path.join(main_path, "share")
    userInfo = {}
    authenticated = False
    connected = True

    num_of_none_pack = 0

    def handle(self):

        self.log_data['ip'] = self.client_address

        logger.info(self.request.recv(1024), extra=self.log_data)
        self.send_welcome()

        while self.connected:
            try:
                data = self.recv_data()
                if data is None:
                    self.Exit_Detect()
                    continue
                elif self.num_of_none_pack != 0:
                    self.Reset_num_of_none_pack()

                if " " in data:
                    cmd, arg = data.split(" ", maxsplit=1)
                else:
                    cmd = data
                    arg = ''
                try:
                    cmd = cmd.upper()
                    func = getattr(self, cmd)
                    func(arg)
                except AttributeError:
                    logger.warning("No such function " + cmd, extra=self.log_data)
            except BaseException as e:
                logger.error(e, extra=self.log_data)


    def recv_data(self, length=1024):

        data = self.request.recv(length)
        if data is None:
            print("None")
            return data

        while not data.endswith(bytes("\r\n", "utf-8")):
            data += self.request.recv(length)
        data = data[:-2]
        print(data)
        try:
            data = data.decode("utf-8")
        except AttributeError:
            data = str(data, "utf-8")
        return data


    def send_command(self, ack, string):

        self.request.sendall(bytes(ack + " " + string + "\r\n", encoding="utf-8"))


    def USER(self, user):
        # TODO:
        #   Anonymous Mode

        if not user:
            self.send_command("501", "Syntax error in parameters or arguments.")

        elif user not in username_list:
            self.send_command("501", "No such user.")
            logger.warning("Invalid logging request from " + user, extra=self.log_data)

        else:
            self.log_data['user'] = user
            logger.info("Log in request from {}, password required".format(user), extra=self.log_data)
            self.send_command("331", "User name okay, need password.")


    def PASS(self, passwd):

        if not passwd:
            self.send_command("501", "Syntax error in parameters or arguments.")

        elif self.log_data['user'] == 'no user':
            self.send_command("503", "Bad sequence of commands.")
            logger.warning("Invalid logging request for no username", extra=self.log_data)

        else:
            for i in userList:
                if i['name'] == self.log_data['user'] and passwd == i['passwd']:
                    self.send_command("230", "User logged in, proceed")
                    logger.info("Success log in from " + self.log_data['user'], extra=self.log_data)
                    self.authenticated = True
                    self.userInfo = i
                    self.cur_path = os.path.join(main_path, i['folder'])
                    os.chdir(self.cur_path)
                    break

            else:
                self.send_command("502", "Pass word error")
                logger.warning("Wrong pass word " + passwd, extra=self.log_data)


    def QUIT(self, arg):

        logger.info("Quit", extra=self.log_data)
        self.send_command("221", "Good Bye")
        self.finish()


    def LIST(self, path):

        if not self.authenticated:
            self.send_command("530", "User not logged in.")
            return

        if not path:
            path = '.'

        if not os.path.isdir(path):
            logger.warning("No such folder " + path, extra=self.log_data)
            self.send_command("553", "No such folder")
            return

        self.send_command("212", standardize_list(get_folder_info(path)))


    def CDUP(self, path):

        if not self.authenticated:
            self.send_command("530", "User not logged in.")
            return

        elif self.userInfo['privilege'] < 20:
            self.send_command("502", "The operation is not permmitted.")
            logger.warning("No permmision to change parent path", extra=self.log_data)
            return

        self.cur_path = path
        os.chdir(self.cur_path)


    def RETR(self, arg):
        # TODO:
        #   Launch the trans server

        if not self.authenticated:
            self.send_command("530", "User not logged in.")
            return

        if os.path.isdir(arg):
            path = arg
        elif os.path.isfile(arg):
            path = os.path.join(self.cur_path, arg)
        else:
            self.send_command("502", "No such file")
            logger.warning("Fail downloading " + arg, extra=self.log_data)
            return

        logger.info("File trans begin " + path, extra=self.log_data)



    def STOR(self, arg):
        # TODO:
        #   the store module

        if not self.authenticated:
            self.send_command("530", "User not logged in.")
            return

        elif self.userInfo['privilege'] < 10:
            self.send_command("502", "The operation is not permmitted."
                                     "Please contact your administrator.")
            logger.warning("Fail to store", extra=self.log_data)
            return


    def MKD(self, foldername):

        if not self.authenticated:
            self.send_command("530", "User not logged in.")
            return

        elif self.userInfo['privilege'] < 10:
            self.send_command("502", "The operation is not permmitted."
                                     "Please contact your administrator.")
            logger.warning("Fail to make folder " + foldername, extra=self.log_data)
            return

        os.mkdir(foldername)


    def DELE(self, arg):

        if not self.authenticated:
            self.send_command("530", "User not logged in.")
            return

        elif not ALLOW_DELETE:
            self.send_command("502", "The server dosen't permmit delete opertion")
            return

        elif self.userInfo['privilege'] < 10:
            self.send_command("502", "The operation is not permmitted."
                                     "Please contact your administrator.")
            logger.warning("[Privilege]Fail to delete file " + arg, extra=self.log_data)
            return

        if os.path.isfile(arg):
            os.remove(arg)
        elif os.path.isfile(arg):
            os.removedirs(arg)
        else:
            self.send_command("501", "The file not found.")
            logger.warning("[Not found]Fail to delete file " + arg, extra=self.log_data)


    def HELP(self, arg):
        help_message = """
            USER\t
            PASS\t
            QUIT\t
            LIST\t
            CDUP\t
            RETR\t
            STOR\t
            DELE\t
            MKD\t
        """
        self.send_command("202", help_message)

    def send_welcome(self):
        string = """
        *************************************
        * Welcome to HanniServer FTP System *
        *************************************\r\n
        """
        self.request.sendall(bytes(string, encoding='utf-8'))

    def Exit_Detect(self):
        self.num_of_none_pack += 1
        if self.num_of_none_pack >= 5:
            logger.warning("Broken Pipe", extra=self.log_data)
            self.finish()


    def finish(self):
        self.connected = False
        self.request.close()

    def is_authenticated(self):
        if not self.authenticated:
            self.send_command("530", "User not logged in.")
            return False
        return True
