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
        shorcuts_extentions = [".lnk", ".url", ".pif", ".shb", "xnk", ".mat", ".kys"]
        
        executable_extentions = [".exe", ".msi", ".action", ".apk", ".app", ".bin", ".osx", ".out", ".prg", ".run", ".scr", ".eham", ".ham", ".pex", ".plx", ".upx"]
       

        #zip extensions source: http://bit.ly/2fnWz4D
        zip_extentions = [".cdz", ".zip", ".pup", ".pkg", ".rar", ".deb", ".sit", ".a02", ".c01", ".cbt", ".cbz", ".comppkg.hauptwerk.rar", 
                          ".dar", ".ecs", ".gca", ".gzip", ".hbc", ".lemon", ".lqr", ".lzm", ".lzo", ".mint", ".mpkg", ".pf", ".qda", ".r00",
                          ".r2", ".rte", ".s7z", ".tar.lzma", ".tx_", ".uha", ".vip", ".zfsendtotarget", ".b1", ".par", ".7z", ".zix", ".pak",
                          ".7z.002", ".gz", ".nex", ".7z.001", ".bh", ".bndl", ".dl_", ".war", ".bz", ".dz", ".pcv", ".pea", ".lzma", ".sy_",
                          ".cbr", ".0", ".c00", ".arc", ".tar.xz", ".bz2", ".ar", ".r30", ".zpi", ".rpm", ".f", ".hpk", ".s00", ".shar", ".tbz",
                          ".z03", ".cxarchive", ".ace", ".rev", ".pet", ".piz", ".pup", ".cpgz", ".fdp", ".jsonlz4", ".mzp", ".s01", ".sbx", 
                          ".sitx", ".hyp", ".ita", ".r01", ".sfx", ".snb", ".000", ".a01", ".agg", ".arh", ".c10", ".cb7", ".czip", ".hbe", 
                          ".pack.gz", ".par2", ".pkg.tar.xz", ".pwa", ".r03", ".r1", ".rz", ".sdn", ".sea", ".sifz", ".ufs.uzip", ".voca", ".wa",
                          ".xez", ".xip", ".sdc", ".xapk", ".z01", ".a00", ".pax", ".yz", ".zoo", ".zz", ".tgz", ".zipx", ".arj", ".ark", 
                          ".bundle", ".ipk", ".lz", ".xz", ".z", ".package", ".alz", ".xx", ".sh", ".sfs", ".txz", ".ain", ".apz", ".archiver", 
                          ".arduboy", ".ari", ".asr", ".b64", ".ba", ".bdoc", ".c02", ".cba", ".cpt", ".dgc", ".edz", ".efw", ".gmz", ".gza", ".hki",
                          ".hki1", ".hki2", ".hki3", ".ice", ".ipg", ".isx", ".jgz", ".lnx", ".mzp", ".pbi", ".pit", ".rk", ".rp9", ".s02", ".sar", 
                          ".smpf", ".sqx", ".tar.bz2", ".tar.lz", ".taz", ".uc2", ".vsi", ".xef", ".xmcdz", ".zap", ".zl", ".zw", ".kgb", ".tar.gz", 
                          ".z02", ".dd", ".srep", ".z04", ".jar.pack", ".r0", ".shr", ".lbr", ".md", ".rnc", ".yz1", ".bzip", ".fp8", ".j", ".lhzd", 
                          ".pae", ".puz", ".r02", ".tz", ".lzh", ".bzip2", ".car", ".iadproj", ".tg", ".trs", ".layout", ".zi", ".boo", 
                          ".comppkg_hauptwerk_rar", ".cp9", ".epi", ".fzbz", ".fzpz", ".gz2", ".gzi", ".hbc2", ".ize", ".jic", ".lha", 
                          ".libzip", ".lzx", ".nz", ".oar", ".oz", ".p01", ".p19", ".paq7", ".paq8", ".paq8l", ".psz", ".r04", ".r21", 
                          ".rss", ".sbx", ".sen", ".sfg", ".stproj", ".tbz2", ".tlz", ".tlzma", ".uzip", ".vem", ".waff", ".wlb", ".xar", ".xzm", 
                          ".zsplit", ".egg", ".ha", ".kz", ".dist", ".paq6", ".snappy", ".y", ".mou", ".tar.gz2", ".tar.z", ".bza", ".ish", ".paq8f", 
                          ".paq8p", ".pim", ".shk", ".spt", ".wot"]
       
        #common image extensions
        images_extentions = [".jpg", ".jpeg", ".png", ".bmp", ".jpg-large", ".ico", ".tif", ".tiff", ".gif", ".jif", ".jfif", ".jp2", ".jpx", ".j2k", 
                             ".j2c", ".fpx", ".pcd", ".webp", ".svg", ".ai", ".eps" ]
        
        #common music extensions
        music_extentions = [".mp3", ".wav", ".aiff", ".aac", ".ogg", ".wma", ".flac", ".alac"]
        
        #movie extensions source: http://bit.ly/2wvYjyr
        movie_extensions = [".cdz", ".264", ".3g2", ".3gp", ".3gp2", ".3gpp", ".3gpp2", ".3mm", ".3p2", ".60d", ".787", ".890", ".aaf", ".aec", 
                            ".aecap", ".aegraphic", ".aep", ".aepx", ".aet", ".aetx", ".ajp", ".ale", ".am", ".amc", ".amv", ".amx", ".anim", 
                            ".anx", ".aqt", ".arcut", ".arf", ".asf", ".asx", ".avb", ".avc", ".avchd", ".avd", ".avi", ".avm", ".avp", ".avs", 
                            ".avs", ".avv", ".awlive", ".axm", ".axv", ".bdm", ".bdmv", ".bdt2", ".bdt3", ".bik", ".bin", ".bix", ".bmc", ".bmk",
                            ".bnp", ".box", ".bs4", ".bsf", ".bu", ".bvr", ".byu", ".camproj", ".camrec", ".camv", ".ced", ".cel", ".cine", 
                            ".cip", ".clk", ".clpi", ".cmmp", ".cmmtpl", ".cmproj", ".cmrec", ".cmv", ".cpi", ".cpvc", ".crec", ".cst", ".cvc", 
                            ".cx3", ".d2v", ".d3v", ".dash", ".dat", ".dav", ".db2", ".dce", ".dck", ".dcr", ".dcr", ".ddat", ".dif", ".dir", 
                            ".divx", ".dlx", ".dmb", ".dmsd", ".dmsd3d", ".dmsm", ".dmsm3d", ".dmss", ".dmx", ".dnc", ".dpa", ".dpg", ".dream", 
                            ".dsy", ".dv", ".dv-avi", ".dv4", ".dvdmedia", ".dvr", ".dvr-ms", ".dvx", ".dxr", ".dzm", ".dzp", ".dzt", ".edl", 
                            ".evo", ".evo", ".exo", ".eye", ".eyetv", ".ezt", ".f4f", ".f4m", ".f4p", ".f4v", ".fbr", ".fbr", ".fbz", ".fcarch",
                            ".fcp", ".fcproject", ".ffd", ".ffm", ".flc", ".flh", ".fli", ".flic", ".flv", ".flx", ".fpdx", ".ftc", ".fvt", ".g2m",
                            ".g64", ".gcs", ".gfp", ".gifv", ".gl", ".gom", ".grasp", ".gts", ".gvi", ".gvp", ".gxf", ".h264", ".hdmov", ".hdv", 
                            ".hkm", ".ifo", ".imovielibrary", ".imoviemobile", ".imovieproj", ".imovieproject", ".inp", ".int", ".ircp", ".irf", 
                            ".ism", ".ismc", ".ismclip", ".ismv", ".iva", ".ivf", ".ivr", ".ivs", ".izz", ".izzy", ".jdr", ".jmv", ".jss", ".jts",
                            ".jtv", ".k3g", ".kdenlive", ".kmv", ".ktn", ".lrec", ".lrv", ".lsf", ".lsx", ".lvix", ".m15", ".m1pg", ".m1v", ".m21",
                            ".m21", ".m2a", ".m2p", ".m2t", ".m2ts", ".m2v", ".m4e", ".m4u", ".m4v", ".m75", ".mani", ".meta", ".mgv", ".mj2", 
                            ".mjp", ".mjpeg", ".mjpg", ".mk3d", ".mkv", ".mmv", ".mnv", ".mob", ".mod", ".modd", ".moff", ".moi", ".moov", ".mov",
                            ".movie", ".mp21", ".mp21", ".mp2v", ".mp4", ".mp4.infovid", ".mp4v", ".mpe", ".mpeg", ".mpeg1", ".mpeg2", ".mpeg4", 
                            ".mpf", ".mpg", ".mpg2", ".mpg4", ".mpgindex", ".mpl", ".mpl", ".mpls", ".mproj", ".mpsub", ".mpv", ".mpv2", ".mqv", 
                            ".msdvd", ".mse", ".msh", ".mswmm", ".mt2s", ".mts", ".mtv", ".mvb", ".mvc", ".mvd", ".mve", ".mvex", ".mvp", ".mvp",
                            ".mvy", ".mxf", ".mxv", ".mys", ".n3r", ".ncor", ".nfv", ".nsv", ".ntp", ".nut", ".nuv", ".nvc", ".ogm", ".ogv", ".ogx",
                            ".orv", ".osp", ".otrkey", ".pac", ".par", ".pds", ".pgi", ".photoshow", ".piv", ".pjs", ".playlist", ".plproj", ".pmf",
                            ".pmv", ".pns", ".ppj", ".prel", ".pro", ".pro4dvd", ".pro5dvd", ".proqc", ".prproj", ".prtl", ".psb", ".psh", ".pssd",
                            ".pva", ".pvr", ".pxv", ".qt", ".qtch", ".qtindex", ".qtl", ".qtm", ".qtz", ".r3d", ".rcd", ".rcproject", ".rcrec", 
                            ".rcut", ".rdb", ".rec", ".rm", ".rmd", ".rmd", ".rmp", ".rms", ".rmv", ".rmvb", ".roq", ".rp", ".rsx", ".rts", ".rts",
                            ".rum", ".rv", ".rvid", ".rvl", ".san", ".sbk", ".sbt", ".sbz", ".scc", ".scm", ".scm", ".scn", ".screenflow", ".sdv",
                            ".sec", ".sec", ".sedprj", ".seq", ".sfd", ".sfera", ".sfvidcap", ".siv", ".smi", ".smi", ".smil", ".smk", ".sml", 
                            ".smv", ".snagproj", ".spl", ".sqz", ".srt", ".ssf", ".ssm", ".stl", ".str", ".stx", ".svi", ".swf", ".swi", ".swt", 
                            ".tda3mt", ".tdt", ".tdx", ".theater", ".thp", ".tid", ".tivo", ".tix", ".tod", ".tp", ".tp0", ".tpd", ".tpr", ".trec", 
                            ".trp", ".ts", ".tsp", ".ttxt", ".tvlayer", ".tvrecording", ".tvs", ".tvshow", ".usf", ".usm", ".v264", ".vbc", ".vc1", 
                            ".vcpf", ".vcr", ".vcv", ".vdo", ".vdr", ".vdx", ".veg", ".vem", ".vep", ".vf", ".vft", ".vfw", ".vfz", ".vgz", ".vid", 
                            ".video", ".viewlet", ".viv", ".vivo", ".vix", ".vlab", ".vmlf", ".vmlt", ".vob", ".vp3", ".vp6", ".vp7", ".vpj", ".vr", 
                            ".vro", ".vs4", ".vse", ".vsp", ".vtt", ".w32", ".wcp", ".webm", ".wfsp", ".wgi", ".wlmp", ".wm", ".wmd", ".wmmp", ".wmv",
                            ".wmx", ".wot", ".wp3", ".wpl", ".wsve", ".wtv", ".wve", ".wvm", ".wvx", ".wxp", ".xej", ".xel", ".xesc", ".xfl", ".xlmv", 
                            ".xml", ".xmv", ".xvid", ".y4m", ".yog", ".yuv", ".zeg", ".zm1", ".zm2", ".zm3", ".zmv" ]
        
                            #text extensions source: http://bit.ly/2wwcfZs
        text_extensions = [ ".pdf", ".xlsx",".log" ".pub", ".pptx", ".ptt", ".accdb", ".jnt", ".csv", ".css",
                           ".html", ".arff", ".wbk", ".pub", ".c", ".cpp", ".ini", ".cdz", ".1st", ".abw", ".act", ".adoc", ".aim", ".ans", ".apkg", 
                           ".apt", ".asc", ".asc", ".ascii", ".ase", ".aty", ".awp", ".awt", ".aww", ".bad", ".bbs", ".bdp", ".bdr", ".bean", ".bib", ".bib", 
                           ".bibtex", ".bml", ".bna", ".boc", ".brx", ".btd", ".bzabw", ".calca", ".charset", ".chart", ".chord", ".cnm", ".cod", ".crwl", ".cws",
                           ".cyi", ".dca", ".dfti", ".dgs", ".diz", ".dne", ".doc", ".doc", ".docm", ".docx", ".docxml", ".docz", ".dox", ".dropbox", ".dsc", ".dvi",
                           ".dwd", ".dx", ".dxb", ".dxp", ".eio", ".eit", ".emf", ".eml", ".emlx", ".emulecollection", ".epp", ".err", ".err", ".etf", ".etx", ".euc",
                           ".fadein.template", ".faq", ".fbl", ".fcf", ".fdf", ".fdr", ".fds", ".fdt", ".fdx", ".fdxt", ".fft", ".fgs", ".flr", ".fodt", ".fountain", 
                           ".fpt", ".frt", ".fwd", ".fwdn", ".gmd", ".gpd", ".gpn", ".gsd", ".gthr", ".gv", ".hbk", ".hht", ".hs", ".hwp", ".hwp", ".hz", 
                           ".idx", ".iil", ".ipf", ".ipspot", ".jarvis", ".jis", ".jnp", ".joe", ".jp1", ".jrtf", ".kes", ".klg", ".klg", ".knt", ".kon", ".kwd",
                           ".latex", ".lbt", ".lis", ".lnt", ".log", ".lp2", ".lst", ".lst", ".ltr", ".ltx", ".lue", ".luf", ".lwp", ".lxfml", ".lyt", ".lyx", ".man",
                           ".mbox", ".mcw", ".md5.txt", ".me", ".mell", ".mellel", ".min", ".mnt", ".msg", ".mw", ".mwd", ".mwp", ".nb", ".ndoc", ".nfo", ".ngloss", 
                           ".njx", ".notes", ".now", ".nwctxt", ".nwm", ".nwp", ".ocr", ".odif", ".odm", ".odo", ".odt", ".ofl", ".opeico", ".openbsd", ".ort", 
                           ".ott", ".p7s", ".pages", ".pages-tef", ".pdpcmd", ".pfx", ".pjt", ".plantuml", ".pmo", ".prt", ".prt", ".psw", ".pu", ".pvj", ".pvm",
                           ".pwd", ".pwdp", ".pwdpl", ".pwi", ".pwr", ".qdl", ".qpf", ".rad", ".readme", ".rft", ".ris", ".rpt", ".rst", ".rtd", ".rtf", ".rtfd",
                           ".rtx", ".run", ".rvf", ".rzk", ".rzn", ".saf", ".safetext", ".sam", ".sam", ".save", ".scc", ".scm", ".scriv", ".scrivx", ".sct", ".scw",
                           ".sdm", ".sdoc", ".sdw", ".se", ".session", ".sgm", ".sig", ".skcard", ".sla", ".sla.gz", ".smf", ".sms", ".ssa", ".story", ".strings", 
                           ".stw", ".sty", ".sub", ".sublime-project", ".sublime-workspace", ".sxg", ".sxw", ".tab", ".tab", ".tdf", ".tdf", ".template", ".tex", ".text",
                           ".textclipping", ".thp", ".tlb", ".tm", ".tmd", ".tmv", ".tpc", ".trelby", ".tvj", ".txt", ".u3i", ".unauth", ".unx", ".uof", ".uot", ".upd", 
                           ".utf8", ".utxt", ".vct", ".vnt", ".vw", ".wbk", ".webdoc", ".wn", ".wp", ".wp4", ".wp5", ".wp6", ".wp7", ".wpa", ".wpd", ".wpd", ".wpd", ".wpl", 
                           ".wps", ".wps", ".wpt", ".wpt", ".wpw", ".wri", ".wsd", ".wtt", ".wtx", ".xbdoc", ".xbplate", ".xdl", ".xdl", ".xwp", ".xwp", ".xwp", ".xy", ".xy3", 
                           ".xyp", ".xyw", ".zabw", ".zrtf", ".zw" ]
        
        D3_work = [".ma", ".fbx", ".mb", ".apj", ".aws", ".blk", ".dbt", ".dwg", ".dwk", ".dw2l", ".dws", ".dwt", ".dwz", ".dxe", ".dxf", ".dxx", ".gpw", ".hdi", ".lli",
                   ".mnx", ".mvi", ".pwt", ".shp", ".shx", ".slb", ".sld"]

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
