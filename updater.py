URL = "/lukshan13/AnnsTuckShop"

def run():
        print("\nchecking for updates")
        from urllib.request import urlopen
        import os
        try:
                content = urlopen("https://raw.githubusercontent.com"+URL+"/master/version").read().decode()
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

def update():
        from urllib.request import urlretrieve
        urlretrieve("https://github.com"+URL+"/archive/master.zip", "download.zip")


run()
update()
