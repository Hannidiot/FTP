import os

__author__ = "Niko是勇者那么谁是公主呢"
__date__ = "2018.7.2"
__version__ = "0.1"

if __name__ == "__main__":

    from src.Settings import *
    from src.utility.Folder import listdir_by_order

    # initiate
    os.chdir(WorkDir)
    if "File" not in listdir_by_order(WorkDir):
        os.mkdir("File")
    if "Logs" not in listdir_by_order(WorkDir):
        os.mkdir("Logs")
    if "user.json" not in listdir_by_order(WorkDir):
        import json

        with open("user.json", 'w') as f:
            json.dump(default_usr, f)
        del json

    from src.Server import CommandServer

    # start the system
    print("Server Begin")
    server = CommandServer.CommandServer(ADDR, CommandServer.CommandHandler)
    server.serve_forever()
