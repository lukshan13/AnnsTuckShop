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

        try:
                db = open("main/ATS/ats.db", 'r+b')
                db = db.read()
        except:
                print ("unable to save file (db). Ignore this is this is the first time running this server")
                db = None
                
        try:
                config = open("main/ATS/static/config.json", 'r+b')
                config = config.read()
        except:
                print ("unable to save file (config). Ignore this is this is the first time running this server")
                db = False
                
        try:
                sk = open("main/ATS/secrets/sk.txt", 'r+b')
                sk=sk.read()
        except:
                print ("unable to save file (sk). Ignore this is this is the first time running this server")
                db = None



        
        from urllib.request import urlretrieve
        import zipfile

        

        urlretrieve("https://github.com"+URL+"/archive/master.zip", "download.zip")
        with zipfile.ZipFile("download.zip","r") as zip_ref:
                zip_ref.extractall("../")
        import os, shutil
        os.remove("download.zip")
        
        with open("main/ATS/ats.db", 'wb') as db1:
                db1.write(db)
        if config:
                with open("main/ATS/static/config.json", 'wb') as config1:
                        config1.write(config)
        with open("main/ATS/static/sk.txt", 'wb') as sk1:
                sk1.write(sk)



run()
#update()
