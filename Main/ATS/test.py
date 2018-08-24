import os.path


def checkSKfile():
    if (os.path.isfile("static/sk.txt")):
        fileSK_exists = True
    else:
        fileSK_exists = False
    print (fileSK_exists)

checkSKfile()