__author__ = "Remigius Kalimba"
'''Add a timer so it does this automatically everyday at a set time'''


from os import path, mkdir, listdir, rename
from getpass import getuser
import time

class Project21():
    def __init__(self):
        '''
        This is an initialization function, I do not wish to explain this.

        This is a smart way to get the username
        We could also have used os.environ, this brings a list and a lot of information we can manipulate.
        '''
        user = getuser()

        '''these two variables store their respective locations, lol like i had to explain that'''
        self.desktopdir = 'C:\\Users\\'+user+'\\Desktop'
        self.Alldesktopdir = 'C:\\Users\\Public\\Desktop'

        '''list of folders to be created'''
        self.folder_names = ["Folders", "Shortcuts", "Zips", "Executables", "Pictures", "Music", "Movies", "Docs"]
        self.special_folders = []

    def makdir(self):
        '''
        This function makes the needed folders if they are not already found.
        '''
        try:
            '''For all the folders in the folder_name list, if that folder is not(False) on the main_desktop
               than create that folder.
            '''
            for nam in range(0, len(self.folder_names)):
                if path.isdir(self.desktopdir+'\\'+self.folder_names[nam]) == False:
                    mkdir(self.desktopdir+"\\"+self.folder_names[nam])
                    print(self.folder_names[nam]+" has been created!")
                else:
                    print("Folder already exists!")
        except Exception as e:
            print(e)

    def mapper(self):
        '''
        This function checks the two folders (current user desktop and all user desktop)
        it takes all the items there and puts them into two respective lists which are
        returned and used by the mover function
        '''
        map = listdir(self.desktopdir)
        map2 = listdir(self.Alldesktopdir)
        maps = [map, map2]
        return maps

    def mover(self, map, map2):
        '''
        This function gets two lists with all the things on the desktops
        and copies them into their respective folders, using a forloop and if statements
        '''
        map = map
        map2 = map2
        '''
        Extension Lists
        '''
        shorcuts_extentions = [".lnk"]
        executable_extentions = [".exe", ".msi"]
        zip_extentions = [".zip", ".tar"]
        images_extentions = [".jpg", ".jpeg", ".png","PNG", ".bmp", ".jpg-large", ".ico", ]
        music_extentions = [".mp3", ".wav"]
        movie_extensions = [".mp4", ".avi", ".mkv", ]
        text_extensions = [".doc", ".docx", ".txt", ".pdf", ".xlsx",".log" ".pub", ".pptx", ".ptt", ".accdb", ".jnt", ".csv", ".css",
                           ".html", ".arff", ".wbk", ".pub", ".c", ".cpp", ".ini"]
        D3_work = [".ma", ".fbx", ".mb"]

        try:

            '''Anything from the All_users_desktop goes to shortcuts, mainly because that's all that's ever there (i think)'''
            for item in map2:
                '''This is a cmd command to move items from one folder to the other'''
                rename(self.Alldesktopdir+'\\'+item, self.desktopdir+"\\"+self.folder_names[1]+"\\"+item)

            for a in range(0, len(map)):
                for b in shorcuts_extentions:
                    if str(map[a].lower()).endswith(b) and str(map[a]) != "Clean.lnk" and str(map[a]) != "Clean.exe.lnk":
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[1]+"\\"+map[a])

                for b in executable_extentions:
                    if str(map[a].lower()).endswith(b) and str(map[a].lower()) != "Clean.exe":
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[3]+"\\"+map[a])

                for b in zip_extentions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[2]+"\\"+map[a])

                for b in images_extentions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[4]+"\\"+map[a])

                for b in music_extentions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[5]+"\\"+map[a])

                for b in movie_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[6]+"\\"+map[a])

                for b in text_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[7]+"\\"+map[a])

                '''This weird part looks for the ".", if its not there this must be a folder'''
                if "." not in str(map[a]) and map[a] not in self.folder_names:
                    rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[0]+"\\"+map[a])
                else:
                    '''Just some error handling here'''
                    if map[a].lower() not in self.folder_names:
                        print("I do not know what to do with "+map[a]+" please update me!")
                    pass
        except Exception as e:
            print(e)

    def writter(self, maps):
        '''
        This function writes the two lists of all the items left on the desktop
        just incase something isnt right and we need a log.
        '''
        lists1 = maps[0]
        lists2 = maps[1]
        writeOB = open('Read_Me.txt', 'w')
        writeOB.write("This is a list of all the items on your desktop before it was cleaned.\n"
                      "Email this list to kalimbatech@gmail.com if anything is not working as planned, it will help with debugging\n"
                      "Together we can make a better app\n\n")

        for i in lists1:
            writeOB.write(i)
            writeOB.write("\n")

        for i in lists2:
            writeOB.write(i)
            writeOB.write("\n")
        writeOB.close()

def automate():
    '''This function keeps the program running and scans the desktop and cleans it after a set time'''

def run_at_time():
    while True:
        tim = time.strftime('%X')
        if str(tim).startswith('6:30:00'):
            main()
            time.sleep(1)
            run_at_time()

def main():
    ''' The oh so magnificent main function keeping shit in order '''
    projectOB = Project21()
    projectOB.makdir()
    maps = projectOB.mapper()
    projectOB.mover(maps[0], maps[1])
    projectOB.writter(maps)

main()
run_at_time()