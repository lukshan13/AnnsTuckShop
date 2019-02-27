URL = "/lukshan13/AnnsTuckShop"

def run():
        print("\nchecking for updates")
        from urllib.request import urlopen
        import os
        try:
                content = urlopen("https://raw.githubusercontent.com"+URL+"/master/Main/version.txt").read().decode()
        except:
                print("Unable to contact github.\nCannot check for updates\n")
                return

        try:
                with open("main/version.txt", "r+t") as version:
                        Version = version.read()
        except:
                print("Version file does not exist. Regenerating\n")
                temp = open("version.txt", "w+b")
                temp.write(b'1.0')
                temp.close()
                run()


        if content <= Version:
                print ("Program up to date\n")
        else:
                print ("Update available, program will be updated\n")
                update()
def update():
        from urllib.request import urlretrieve
        import zipfile
        urlretrieve("https://github.com"+URL+"/archive/master.zip", "download.zip")
        with zipfile.ZipFile("download.zip","r") as zip_ref:
                    zip_ref.extractall("../")
        import os, shutil
        os.remove("download.zip")
        


run()

