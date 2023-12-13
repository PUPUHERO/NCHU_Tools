# import this file to create a loginSettings.ini
import os
# if no loginSettings.ini, create a new one
def check_loginSettings():
    if os.path.exists("loginSettings.ini") == False:
        with open("loginSettings.ini", "w") as f:
            f.write("[loginInfo]\n")
            f.write("account=411006xxxx\n")
            f.write("password=xxxxxxxx\n")