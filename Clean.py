__author__ = "Remigius Kalimba"
'''Add a timer so it does this automatically everyday at a set time'''

from os import path, mkdir, listdir, rename, environ
from getpass import getuser
import time
import sys

if sys.version_info >= (3,):
    from tkinter import *
    from tkinter import messagebox as tkMessageBox
else:
    from Tkinter import *
    import tkMessageBox

import Globals

class App(Frame):
    def clean(self):
        main()

    def quit_all(self):
        quit()
        sys.exit(0)

    def check(self, item):
        if item == 0:
            Globals.sc = not Globals.sc
        elif item == 1:
            Globals.zips = not Globals.zips
        elif item == 2:
            Globals.audio = not Globals.audio
        elif item == 3:
            Globals.img = not Globals.img
        elif item == 4:
            Globals.exes = not Globals.exes
        elif item == 5:
            Globals.mov = not Globals.mov
        elif item == 6:
            Globals.txt = not Globals.txt
        elif item == 7:
            Globals.cad = not Globals.cad
        elif item == 8:
            Globals.programming = not Globals.programming

    def create(self):
        self.winfo_toplevel().title("Desktop Cleaner")

        self.shortcuts = Checkbutton(self)
        self.shortcuts["text"] = "Shortcuts"
        self.shortcuts.select()
        self.shortcuts["command"] = lambda: self.check(0)
        self.shortcuts.pack({"side":"top"})

        self.zip = Checkbutton(self)
        self.zip["text"] = "Archives"
        self.zip.select()
        self.zip["command"] = lambda: self.check(1)
        self.zip.pack({"side": "top"})

        self.music = Checkbutton(self)
        self.music["text"] = "Music"
        self.music.select()
        self.music["command"] = lambda: self.check(2)
        self.music.pack({"side": "top"})

        self.images = Checkbutton(self)
        self.images["text"] = "Images"
        self.images.select()
        self.images["command"] = lambda: self.check(3)
        self.images.pack({"side": "top"})

        self.exe = Checkbutton(self)
        self.exe["text"] = "Executables"
        self.exe.select()
        self.exe["command"] = lambda: self.check(4)
        self.exe.pack({"side": "top"})

        self.movies = Checkbutton(self)
        self.movies["text"] = "Movies"
        self.movies.select()
        self.movies["command"] = lambda: self.check(5)
        self.movies.pack({"side": "top"})

        self.text = Checkbutton(self)
        self.text["text"] = "Text"
        self.text.select()
        self.text["command"] = lambda: self.check(6)
        self.text.pack({"side": "top"})

        self.d3 = Checkbutton(self)
        self.d3["text"] = "CAD Files"
        self.d3.select()
        self.d3["command"] = lambda: self.check(7)
        self.d3.pack({"side": "top"})

        self.code = Checkbutton(self)
        self.code["text"] = "Code"
        self.code.select()
        self.code["command"] = lambda: self.check(8)
        self.code.pack({"side": "top"})

        self.clean_button = Button(self)
        self.clean_button["text"] = "Clean"
        self.clean_button["command"] = self.clean
        self.clean_button.pack({"side": "left"})

        self.quit_button = Button(self)
        self.quit_button["text"] = "Exit"
        self.quit_button["command"] = self.quit_all
        self.quit_button.pack({"side":"left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create()


class Project21():
    def __init__(self):
        '''
        This is an initialization function, I do not wish to explain this.

        This is a smart way to get the username
        We could also have used os.environ, this brings a list and a lot of information we can manipulate.
        '''
        user = getuser()

        # References:   https://en.wikipedia.org/wiki/Environment_variable#Default_values
        #               https://en.wikipedia.org/wiki/Windows_NT#Releases
        #
        #
        if sys.platform == 'win32':
            self.desktopdir = path.join(environ['USERPROFILE'],'Desktop')

            # Determine Windows version; check if this is XP; accordingly, read target folders
            if sys.getwindowsversion().major < 6:
                self.Alldesktopdir = path.join(environ['ALLUSERSPROFILE'],'Desktop')
            else:
                self.Alldesktopdir = path.join(environ['PUBLIC'],'Desktop')

            '''list of folders to be created'''
            self.folder_names = ["Folders", "Shortcuts", "Zips", "Executables", "Pictures", "Music", "Movies", "Docs", "Code"]
            self.special_folders = []
        else:
            print("{} version not implemented".format(sys.platform))
            raise NotImplementedError

    def makdir(self):
        '''
        This function makes the needed folders if they are not already found.
        '''
        try:
            '''For all the folders in the folder_name list, if that folder is not(False) on the main_desktop
               then create that folder.
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
        shortcuts_extensions = [".kys",".lnk",".mat",".pif",".shb",".url","xnk"]

        executable_extensions = [".action",".apk",".app",".bin",".eham",".exe",".ham",".msi",".osx",".out",".pex",".plx",".prg",".run",".scr",".upx"]

        #zip extensions source: http://bit.ly/2fnWz4D
        zip_extensions = [".0",".000",".7z",".7z.001",".7z.002",".a00",".a01",".a02",".ace",".agg",".ain",".alz",".apz",".ar",".arc",".archiver",".arduboy",".arh",
                          ".ari",".arj",".ark",".asr",".b1",".b64",".ba",".bdoc",".bh",".bndl",".boo",".bundle",".bz",".bz2",".bza",".bzip",".bzip2",".c00",".c01",
                          ".c02",".c10",".car",".cb7",".cba",".cbr",".cbt",".cbz",".cdz",".comppkg.hauptwerk.rar",".comppkg_hauptwerk_rar",".cp9",".cpgz",".cpt",
                          ".cxarchive",".czip",".dar",".dd",".deb",".dgc",".dist",".dl_",".dz",".ecs",".edz",".efw",".egg",".epi",".f",".fdp",".fp8",".fzbz",".fzpz",
                          ".gca",".gmz",".gz",".gz2",".gza",".gzi",".gzip",".ha",".hbc",".hbc2",".hbe",".hki",".hki1",".hki2",".hki3",".hpk",".hyp",".iadproj",".ice",
                          ".ipg",".ipk",".ish",".isx",".ita",".ize",".j",".jar.pack",".jgz",".jic",".jsonlz4",".kgb",".kz",".layout",".lbr",".lemon",".lha",".lhzd",
                          ".libzip",".lnx",".lqr",".lz",".lzh",".lzm",".lzma",".lzo",".lzx",".md",".mint",".mou",".mpkg",".mzp",".nex",".nz",".oar",".oz",".p01",
                          ".p19",".pack.gz",".package",".pae",".pak",".paq6",".paq7",".paq8",".paq8f",".paq8l",".paq8p",".par",".par2",".pax",".pbi",".pcv",".pea",
                          ".pet",".pf",".pim",".pit",".piz",".pkg",".pkg.tar.xz",".psz",".pup",".puz",".pwa",".qda",".r0",".r00",".r01",".r02",".r03",".r04",".r1",
                          ".r2",".r21",".r30",".rar",".rev",".rk",".rnc",".rp9",".rpm",".rss",".rte",".rz",".s00",".s01",".s02",".s7z",".sar",".sbx",".sdc",".sdn",
                          ".sea",".sen",".sfg",".sfs",".sfx",".sh",".shar",".shk",".shr",".sifz",".sit",".sitx",".smpf",".snappy",".snb",".spt",".sqx",".srep",
                          ".stproj",".sy_",".tar.bz2",".tar.gz",".tar.gz2",".tar.lz",".tar.lzma",".tar.xz",".tar.z",".taz",".tbz",".tbz2",".tg",".tgz",".tlz",
                          ".tlzma",".trs",".tx_",".txz",".tz",".uc2",".ufs.uzip",".uha",".uzip",".vem",".vip",".voca",".vsi",".wa",".waff",".war",".wlb",".wot",
                          ".xapk",".xar",".xef",".xez",".xip",".xmcdz",".xx",".xz",".xzm",".y",".yz",".yz1",".z",".z01",".z02",".z03",".z04",".zap",".zfsendtotarget",
                          ".zi",".zip",".zipx",".zix",".zl",".zoo",".zpi",".zsplit",".zw",".zz"]

        #image extensions source: https://fileinfo.com/filetypes/raster_image, https://fileinfo.com/filetypes/vector_image, and https://fileinfo.com/filetypes/camera_raw
        images_extensions = [".3fr",".ai",".ari",".arr",".arw",".avatar",".awd",".bmp",".bpg",".cdmz",".cdr",".cr2",".crw",".ct",".dcr",".dds",
                             ".ded",".djvu",".dng",".eip",".eps",".exr",".fff",".fpx",".gif",".hdr",".hpgl",".i3d",".ico",".icon",".itc2",".iwi",
                             ".j2c",".j2k",".jbig2",".jfif",".jif",".jp2",".jpc",".jpe",".jpeg",".jpg",".jpg-large",".jpx",".jxr",".k25",".kdc",
                             ".lip",".mfw",".mos",".msp",".nef",".nrw",".orf",".ota",".pat",".pcd",".pcx",".pdn",".pi2",".pic",".picnc",".piskel",
                             ".png",".ppf",".psb",".psd",".pspbrush",".pwp",".pxd",".pxr",".raf",".raw",".rw2",".rwz",".sai",".spr",".sprite",
                             ".sprite2",".srf",".sumo",".svg",".tbn",".tga",".tif",".tiff",".tn",".tn3",".ufo",".vsdx",".webp",".x3f",".xcf",".xpm"]

        #music extensions source: https://fileinfo.com/filetypes/audio
        music_extensions = [".aiff", ".aac", ".alac", ".flp", ".mp3", ".aimppl", ".aup", ".ang", ".mscz", ".vdj", ".ram", ".sf2", ".sfk", ".xfs",
                            ".dff", ".als", ".bidule", ".bnk", ".bww", ".cgrp", ".csh", ".cwb", ".dfc", ".dig", ".dm", ".dmsa", ".dmse", ".dsf",
                            ".dsm", ".dtm", ".f4a", ".fev", ".h5b", ".h5s", ".ins", ".isma", ".krz", ".kt3", ".mbr", ".mmlp", ".mtp", ".nbs", ".omg",
                            ".ovw", ".pca", ".pcg", ".ptxt", ".qcp", ".r1m", ".rip", ".rns", ".rol", ".rso", ".saf", ".sbi", ".sfpack", ".sgp", ".slp",
                            ".sou", ".sprg", ".sseq", ".sxt", ".syn", ".syw", ".trak", ".ust", ".vsqx", ".w64", ".wus", ".zpa", ".zvd", ".flac", ".afc",
                            ".mui", ".abm", ".pla", ".vag", ".act", ".wav", ".bun", ".gsm", ".midi", ".m3u", ".mmm", ".pkf", ".sng", ".m4r", ".mpga",
                            ".omf", ".rx2", ".flm", ".gp5", ".sdt", ".ac3", ".mid", ".xspf", ".nkm", ".nsa", ".ply", ".sbg", ".sdat", ".toc", ".tg",
                            ".ogg", ".wma", ".amr", ".m3u8", ".5xe", ".aif", ".frg", ".minigsf", ".pcast", ".vyf"]

        #movie extensions source: http://bit.ly/2wvYjyr
        movie_extensions = [".264",".3g2",".3gp",".3gp2",".3gpp",".3gpp2",".3mm",".3p2",".60d",".787",".890",".aaf",".aec",".aecap",".aegraphic",".aep",
                            ".aepx",".aet",".aetx",".ajp",".ale",".am",".amc",".amv",".amx",".anim",".anx",".aqt",".arcut",".arf",".asf",".asx",".avb",
                            ".avc",".avchd",".avd",".avi",".avm",".avp",".avs",".avv",".awlive",".axm",".axv",".bdm",".bdmv",".bdt2",".bdt3",".bik",".bin",
                            ".bix",".bmc",".bmk",".bnp",".box",".bs4",".bsf",".bu",".bvr",".byu",".camproj",".camrec",".camv",".cdz",".ced",".cel",".cine",
                            ".cip",".clk",".clpi",".cmmp",".cmmtpl",".cmproj",".cmrec",".cmv",".cpi",".cpvc",".crec",".cst",".cvc",".cx3",".d2v",".d3v",
                            ".dash",".dat",".dav",".db2",".dce",".dck",".dcr",".ddat",".dif",".dir",".divx",".dlx",".dmb",".dmsd",".dmsd3d",".dmsm",
                            ".dmsm3d",".dmss",".dmx",".dnc",".dpa",".dpg",".dream",".dsy",".dv",".dv-avi",".dv4",".dvdmedia",".dvr",".dvr-ms",".dvx",
                            ".dxr",".dzm",".dzp",".dzt",".edl",".evo",".exo",".eye",".eyetv",".ezt",".f4f",".f4m",".f4p",".f4v",".fbr",".fbz",".fcarch",
                            ".fcp",".fcproject",".ffd",".ffm",".flc",".flh",".fli",".flic",".flv",".flx",".fpdx",".ftc",".fvt",".g2m",".g64",".gcs",
                            ".gfp",".gifv",".gl",".gom",".grasp",".gts",".gvi",".gvp",".gxf",".h264",".hdmov",".hdv",".hkm",".ifo",".imovielibrary",
                            ".imoviemobile",".imovieproj",".imovieproject",".inp",".int",".ircp",".irf",".ism",".ismc",".ismclip",".ismv",".iva",".ivf",
                            ".ivr",".ivs",".izz",".izzy",".jdr",".jmv",".jss",".jts",".jtv",".k3g",".kdenlive",".kmv",".ktn",".lrec",".lrv",".lsf",
                            ".lsx",".lvix",".m15",".m1pg",".m1v",".m21",".m2a",".m2p",".m2t",".m2ts",".m2v",".m4e",".m4u",".m4v",".m75",".mani",".meta",
                            ".mgv",".mj2",".mjp",".mjpeg",".mjpg",".mk3d",".mkv",".mmv",".mnv",".mob",".mod",".modd",".moff",".moi",".moov",".mov",
                            ".movie",".mp21",".mp2v",".mp4",".mp4.infovid",".mp4v",".mpe",".mpeg",".mpeg1",".mpeg2",".mpeg4",".mpf",".mpg",".mpg2",
                            ".mpg4",".mpgindex",".mpl",".mpls",".mproj",".mpsub",".mpv",".mpv2",".mqv",".msdvd",".mse",".msh",".mswmm",".mt2s",".mts",
                            ".mtv",".mvb",".mvc",".mvd",".mve",".mvex",".mvp",".mvy",".mxf",".mxv",".mys",".n3r",".ncor",".nfv",".nsv",".ntp",".nut",
                            ".nuv",".nvc",".ogm",".ogv",".ogx",".orv",".osp",".otrkey",".pac",".par",".pds",".pgi",".photoshow",".piv",".pjs",".playlist",
                            ".plproj",".pmf",".pmv",".pns",".ppj",".prel",".pro",".pro4dvd",".pro5dvd",".proqc",".prproj",".prtl",".psb",".psh",".pssd",
                            ".pva",".pvr",".pxv",".qt",".qtch",".qtindex",".qtl",".qtm",".qtz",".r3d",".rcd",".rcproject",".rcrec",".rcut",".rdb",".rec",
                            ".rm",".rmd",".rmp",".rms",".rmv",".rmvb",".roq",".rp",".rsx",".rts",".rum",".rv",".rvid",".rvl",".san",".sbk",".sbt",".sbz",
                            ".scc",".scm",".scn",".screenflow",".sdv",".sec",".sedprj",".seq",".sfd",".sfera",".sfvidcap",".siv",".smi",".smil",".smk",
                            ".sml",".smv",".snagproj",".spl",".sqz",".srt",".ssf",".ssm",".stl",".str",".stx",".svi",".swf",".swi",".swt",".tda3mt",".tdt",
                            ".tdx",".theater",".thp",".tid",".tivo",".tix",".tod",".tp",".tp0",".tpd",".tpr",".trec",".trp",".ts",".tsp",".ttxt",".tvlayer",
                            ".tvrecording",".tvs",".tvshow",".usf",".usm",".v264",".vbc",".vc1",".vcpf",".vcr",".vcv",".vdo",".vdr",".vdx",".veg",".vem",
                            ".vep",".vf",".vft",".vfw",".vfz",".vgz",".vid",".video",".viewlet",".viv",".vivo",".vix",".vlab",".vmlf",".vmlt",".vob",".vp3",
                            ".vp6",".vp7",".vpj",".vr",".vro",".vs4",".vse",".vsp",".vtt",".w32",".wcp",".webm",".wfsp",".wgi",".wlmp",".wm",".wmd",".wmmp",
                            ".wmv",".wmx",".wot",".wp3",".wpl",".wsve",".wtv",".wve",".wvm",".wvx",".wxp",".xej",".xel",".xesc",".xfl",".xlmv",".xml",".xmv",
                            ".xvid",".y4m",".yog",".yuv",".zeg",".zm1",".zm2",".zm3",".zmv" ]

        #text extensions source: http://bit.ly/2wwcfZs
        text_extensions = [ ".1st",".abw",".accdb",".act",".adoc",".aim",".ans",".apkg",".apt",".arff",".asc",".ascii",".ase",".aty",".awp",".awt",".aww",".bad",
                           ".bbs",".bdp",".bdr",".bean",".bib",".bibtex",".bml",".bna",".boc",".brx",".btd",".bzabw",".c",".calca",".cdz",".charset",".chart",
                           ".chord",".cnm",".cod",".cpp",".crwl",".css",".csv",".cws",".cyi",".dca",".dfti",".dgs",".diz",".dne",".doc",".docm",".docx",".docxml",
                           ".docz",".dox",".dropbox",".dsc",".dvi",".dwd",".dx",".dxb",".dxp",".eio",".eit",".emf",".eml",".emlx",".emulecollection",".epp",".err",
                           ".etf",".etx",".euc",".fadein.template",".faq",".fbl",".fcf",".fdf",".fdr",".fds",".fdt",".fdx",".fdxt",".fft",".fgs",".flr",".fodt",
                           ".fountain",".fpt",".frt",".fwd",".fwdn",".gmd",".gpd",".gpn",".gsd",".gthr",".gv",".hbk",".hht",".hs",".html",".hwp",".hz",".idx",
                           ".iil",".ini",".ipf",".ipspot",".jarvis",".jis",".jnp",".jnt",".joe",".jp1",".jrtf",".kes",".klg",".knt",".kon",".kwd",".latex",".lbt",
                           ".lis",".lnt",".log",".log" ".pub",".lp2",".lst",".ltr",".ltx",".lue",".luf",".lwp",".lxfml",".lyt",".lyx",".man",".mbox",".mcw",".md5.txt",
                           ".me",".mell",".mellel",".min",".mnt",".msg",".mw",".mwd",".mwp",".nb",".ndoc",".nfo",".ngloss",".njx",".notes",".now",".nwctxt",".nwm",".nwp",
                           ".ocr",".odif",".odm",".odo",".odt",".ofl",".opeico",".openbsd",".ort",".ott",".p7s",".pages",".pages-tef",".pdf",".pdpcmd",".pfx",".pjt",".plantuml",
                           ".pmo",".pptx",".prt",".psw",".ptt",".pu",".pub",".pvj",".pvm",".pwd",".pwdp",".pwdpl",".pwi",".pwr",".qdl",".qpf",".rad",".readme",".rft",
                           ".ris",".rpt",".rst",".rtd",".rtf",".rtfd",".rtx",".run",".rvf",".rzk",".rzn",".saf",".safetext",".sam",".save",".scc",".scm",".scriv",
                           ".scrivx",".sct",".scw",".sdm",".sdoc",".sdw",".se",".session",".sgm",".sig",".skcard",".sla",".sla.gz",".smf",".sms",".ssa",
                           ".story",".strings",".stw",".sty",".sub",".sublime-project",".sublime-workspace",".sxg",".sxw",".tab",".tdf",".template",".tex",
                           ".text",".textclipping",".thp",".tlb",".tm",".tmd",".tmv",".tpc",".trelby",".tvj",".txt",".u3i",".unauth",".unx",".uof",".uot",
                           ".upd",".utf8",".utxt",".vct",".vnt",".vw",".wbk",".webdoc",".wn",".wp",".wp4",".wp5",".wp6",".wp7",".wpa",".wpd",".wpl",".wps",
                           ".wpt",".wpw",".wri",".wsd",".wtt",".wtx",".xbdoc",".xbplate",".xdl",".xlsx",".xwp",".xy",".xy3",".xyp",".xyw",".zabw",".zrtf",".zw"]

        D3_work = [".ma", ".fbx", ".mb", ".apj", ".aws", ".blk", ".dbt", ".dwg", ".dwk", ".dw2l", ".dws", ".dwt", ".dwz", ".dxe", ".dxf", ".dxx", ".gpw", ".hdi", ".lli",
                   ".mnx", ".mvi", ".pwt", ".schematic", ".shp", ".shx", ".slb", ".sld", ".blend"]

        programming_languages_extensions = [".4db", ".4th", ".a", ".a2w", ".abc", ".acd", ".addin", ".ads", ".agi", ".ahk", ".aia", ".aidl", ".alb",
                 ".am4", ".am5", ".am6", ".am7", ".ane", ".ap_", ".apa", ".appx", ".appxupload", ".aps", ".arsc", ".artproj",
                 ".as", ".as2proj", ".as3proj", ".asc", ".asi", ".asm", ".asm", ".asvf", ".au3", ".autoplay", ".awk",
                 ".b", ".bas", ".bb", ".bbc", ".bbproject", ".bbprojectd", ".bcp", ".bdsproj", ".bet", ".bluej", ".bpg", ".bpl",
                 ".brx", ".bs2", ".bsc",
                 ".c", ".c", ".caf", ".caproj", ".capx", ".cbl", ".cbp", ".cc", ".ccgame", ".ccn", ".ccp", ".ccs", ".cd", ".cdf",
                 ".cfc", ".class", ".clips", ".cls", ".clw", ".cob", ".cod", ".config", ".cp", ".cp", ".cpp", ".cs", ".csi", ".csi",
                 ".csn", ".csp", ".csproj", ".csx", ".ctl", ".ctp", ".ctxt", ".cu", ".cvsrc", ".cxp", ".cxx",
                 ".d", ".dba", ".dba", ".dbml", ".dbo", ".dbpro", ".dbproj", ".dcp", ".dcproj", ".dcu", ".dcuil", ".dec", ".def",
                 ".deviceids", ".dex", ".df1", ".dfm", ".dgml", ".dgsl", ".diff", ".dm1", ".dmd", ".dob", ".dox", ".dpk", ".dpkw",
                 ".dpl", ".dpr", ".dproj", ".dsgm", ".dsp", ".dtd",
                 ".edml", ".edmx", ".ent", ".entitlements", ".eql", ".erb", ".erl", ".ex", ".exp", ".exw",
                 ".f", ".f90", ".fbp", ".fbz7", ".fgl", ".fla", ".for", ".forth", ".fpm", ".framework", ".frx", ".fs", ".fsi",
                 ".fsproj", ".fsproj", ".fsscript", ".fsx", ".ftl", ".ftn", ".fxc", ".fxcproj", ".fxl", ".fxml", ".fxpl",
                 ".gameproj", ".gch", ".ged", ".gem", ".gemspec", ".gfar", ".gitattributes", ".gitignore", ".gld",
                 ".gm6", ".gm81", ".gmd", ".gmk", ".gmo", ".gmx", ".gorm", ".greenfoot", ".groovy", ".groupproj", ".gs", ".gs3", ".gszip",
                 ".h", ".hal", ".haml", ".has", ".hbs", ".hh", ".hpf", ".hpp", ".hs", ".hxx",
                 ".i", ".iconset", ".idb", ".idl", ".idt", ".ilk", ".iml", ".inc", ".inl", ".ino", ".ipch", ".ipr",
                 ".ipr", ".ise", ".ism", ".ist", ".iwb", ".iws",
                 ".java", ".jcp", ".jic", ".jpr", ".jpx", ".jsfl", ".jspf",
                 ".kdevelop", ".kdevprj", ".kpl",
                 ".l", ".lbi", ".lbs", ".lds", ".lgo", ".lhs", ".licenses", ".licx", ".lisp", ".lit", ".livecode",
                 ".lnt", ".lproj", ".lsproj", ".ltb", ".lua", ".luc", ".lucidsnippet", ".lxsproj",
                 ".m", ".m", ".m4", ".magik", ".mak", ".markdown", ".mcp", ".md", ".mdzip", ".mer", ".mf", ".mfa", ".mk",
                 ".ml", ".mm", ".mo", ".mod", ".mom", ".mpr", ".mrt", ".msha", ".mshc", ".mshi", ".msl", ".msp", ".mss", ".mv",
                 ".mxml", ".myapp",
                 ".nbc", ".ncb", ".ned", ".nfm", ".nib", ".nk", ".nls", ".nqc", ".nsh", ".nsi", ".nupkg", ".nuspec", ".nvv",
                 ".nw", ".nxc",
                 ".o", ".oca", ".octest", ".ocx", ".odl", ".omo", ".owl",
                 ".p", ".p3d", ".pas", ".pas", ".patch", ".pb", ".pbg", ".pbj", ".pbk", ".pbxbtree", ".pbxproj",
                 ".pbxuser", ".pch", ".pcp", ".pde", ".pdm", ".ph", ".pika", ".pjx", ".pkgdef", ".pkgundef", ".pl",
                 ".pl", ".pl1", ".playground", ".plc", ".ple", ".pli", ".pm", ".po", ".pod", ".pot", ".ppc", ".prg", ".prg",
                 ".pri", ".pri", ".pro", ".proto", ".psc", ".psm1", ".ptl", ".pwn", ".pxd", ".py", ".pyd", ".pyw", ".pyx",
                 ".qpr", ".r", ".r", ".r", ".rav", ".rb", ".rbc", ".rbp", ".rbw", ".rc", ".rc2", ".rdlc", ".refresh",
                 ".res", ".res", ".resjson", ".resources", ".resw", ".resx", ".rexx", ".rise", ".rkt", ".rnc", ".rodl", ".rpy",
                 ".rsrc", ".rss", ".rul",
                 ".s", ".s19", ".sas", ".sb", ".sb2", ".sbproj", ".sc", ".scc", ".scriptsuite", ".scriptterminology",
                 ".sdef", ".sh", ".sln", ".slogo", ".sltng", ".sma", ".smali", ".snippet", ".so", ".spec", ".sqlproj",
                 ".src", ".src", ".ss", ".ssc", ".ssi", ".storyboard", ".sud", ".suo", ".sup", ".svn", ".swc", ".swd",
                 ".swift", ".sym",
                 ".t", ".targets", ".tcl", ".tds", ".testrunconfig", ".testsettings", ".textfactory", ".tk", ".tld",
                 ".tlh", ".tli", ".tmlanguage", ".tmproj", ".tns", ".tpu", ".trx", ".tt", ".tu", ".tur", ".twig",
                 ".ui", ".uml", ".v", ".v", ".v11", ".v12", ".vb", ".vbg", ".vbp", ".vbproj", ".vbx", ".vbz", ".vc", ".vcp",
                 ".vcproj", ".vcxproj", ".vdm", ".vdp", ".vdproj", ".vgc", ".vhd", ".vm", ".vsmacros", ".vsmdi", ".vsmproj", ".vsp",
                 ".vsps", ".vspscc", ".vspx", ".vssscc", ".vsz", ".vtm", ".vtml", ".vtv",
                 ".w", ".w32", ".wdgt", ".wdgtproj", ".wdl", ".wdp", ".wdw", ".wiq", ".wixlib", ".wixmsp", ".wixmst", ".wixobj",
                 ".wixout", ".wixpdb", ".wixproj", ".workspace", ".wpw", ".wsc", ".wsp", ".wxi", ".wxl", ".wxs",
                 ".xaml", ".xamlx", ".xap", ".xcappdata", ".xcarchive", ".xcconfig", ".xcdatamodeld", ".xcodeproj",
                 ".xcsnapshots", ".xcworkspace", ".xib", ".xojo_binary_project", ".xojo_menu", ".xojo_project", ".xojo_xml_project",
                 ".xoml", ".xpp", ".xq", ".xql", ".xqm", ".xquery", ".xsd", ".xt", ".y", ".yaml", ".yml", ".ymp", ".ypr"]

        d3_work_extensions = [".apj",".aws",".blk",".dbt",".dw2l",".dwg",".dwk",".dws",".dwt",".dwz",".dxe",".dxf",".dxx",".fbx",".gpw",".hdi",".lli",".ma",".mb",".mnx",
                   ".mvi",".pwt",".shp",".shx",".slb",".sld"]

        programming_languages_extensions = [".4db",".4th",".a",".a2w",".abc",".acd",".addin",".ads",".agi",".aia",".aidl",".alb",".am4",".am5",".am6",".am7",".ane",".ap_",
                                            ".apa",".appx",".appxupload",".aps",".arsc",".artproj",".as",".as2proj",".as3proj",".asc",".asi",".asm",".asm",".asvf",".au3",
                                            ".autoplay",".awk",".b",".bas",".bb",".bbc",".bbproject",".bbprojectd",".bcp",".bdsproj",".bet",".bf",".bluej",".bpg",".bpl",".brx",
                                            ".bs2",".bsc",".c",".c",".caf",".caproj",".capx",".cbl",".cbp",".cc",".ccgame",".ccn",".ccp",".ccs",".cd",".cdf",".cfc",".class",
                                            ".clips",".cls",".clw",".cob",".cod",".config",".cp",".cp",".cpp",".cs",".csi",".csi",".csn",".csp",".csproj",".csx",".ctl",".ctp",
                                            ".ctxt",".cu",".cvsrc",".cxp",".cxx",".d",".dba",".dba",".dbml",".dbo",".dbpro",".dbproj",".dcp",".dcproj",".dcu",".dcuil",".dec",
                                            ".def",".deviceids",".dex",".df1",".dfm",".dgml",".dgsl",".diff",".dm1",".dmd",".dob",".dox",".dpk",".dpkw",".dpl",".dpr",".dproj",
                                            ".dsgm",".dsp",".dtd",".edml",".edmx",".ent",".entitlements",".eql",".erb",".erl",".ex",".exp",".exw",".f",".f90",".fbp",".fbz7",
                                            ".fgl",".fla",".for",".forth",".fpm",".framework",".frx",".fs",".fsi",".fsproj",".fsproj",".fsscript",".fsx",".ftl",".ftn",".fxc",
                                            ".fxcproj",".fxl",".fxml",".fxpl",".gameproj",".gch",".ged",".gem",".gemspec",".gfar",".gitattributes",".gitignore",".gld",".gm6",
                                            ".gm81",".gmd",".gmk",".gmo",".gmx",".gorm",".greenfoot",".groovy",".groupproj",".gs",".gs3",".gszip",".h",".hal",".haml",".has",
                                            ".hbs",".hh",".hpf",".hpp",".hs",".hxx",".i",".iconset",".idb",".idl",".idt",".ilk",".iml",".inc",".inl",".ino",".ipch",".ipr",
                                            ".ipr",".ise",".ism",".ist",".iwb",".iws",".java",".jcp",".jic",".jpr",".jpx",".jsfl",".jspf",".kdevelop",".kdevprj",".kpl",
                                            ".l",".lbi",".lbs",".lds",".lgo",".lhs",".licenses",".licx",".lisp",".lit",".livecode",".lnt",".lproj",".lsproj",".ltb",
                                            ".lua",".luc",".lucidsnippet",".lxsproj",".m",".m",".m4",".magik",".mak",".markdown",".mcp",".md",".mdzip",".mer",".mf",
                                            ".mfa",".mk",".ml",".mm",".mo",".mod",".mom",".mpr",".mrt",".msha",".mshc",".mshi",".msl",".msp",".mss",".mv",".mxml",
                                            ".myapp",".nbc",".ncb",".ned",".nfm",".nib",".nk",".nls",".nqc",".nsh",".nsi",".nupkg",".nuspec",".nvv",".nw",".nxc",
                                            ".o",".oca",".octest",".ocx",".odl",".omo",".owl",".p",".p3d",".pas",".pas",".patch",".pb",".pbg",".pbj",".pbk",".pbxbtree",
                                            ".pbxproj",".pbxuser",".pch",".pcp",".pde",".pdm",".ph",".pika",".pjx",".pkgdef",".pkgundef",".pl",".pl1",".playground",
                                            ".plc",".ple",".pli",".pm",".po",".pod",".pot",".ppc",".prg",".prg",".pri",".pri",".pro",".proto",".psc",".psm1",".ptl",".pwn",
                                            ".pxd",".py",".pyd",".pyw",".pyx",".qpr",".r",".r",".r",".rav",".rb",".rbc",".rbp",".rbw",".rc",".rc2",".rdlc",".refresh",".res",
                                            ".res",".resjson",".resources",".resw",".resx",".rexx",".rise",".rkt",".rnc",".rodl",".rpy",".rsrc",".rss",".rul",".s",".s19",
                                            ".sas",".sb",".sb2",".sbproj",".sc",".scc",".scriptsuite",".scriptterminology",".sdef",".sh",".sln",".slogo",".sltng",".sma",
                                            ".smali",".snippet",".so",".spec",".sqlproj",".src",".src",".ss",".ssc",".ssi",".storyboard",".sud",".suo",".sup",".svn",".swc",
                                            ".swd",".swift",".sym",".t",".targets",".tcl",".tds",".testrunconfig",".testsettings",".textfactory",".tk",".tld",".tlh",".tli",
                                            ".tmlanguage",".tmproj",".tns",".tpu",".trx",".tt",".tu",".tur",".twig",".ui",".uml",".v",".v",".v11",".v12",".vb",".vbg",".vbp",
                                            ".vbproj",".vbx",".vbz",".vc",".vcp",".vcproj",".vcxproj",".vdm",".vdp",".vdproj",".vgc",".vhd",".vm",".vsmacros",".vsmdi",".vsmproj",
                                            ".vsp",".vsps",".vspscc",".vspx",".vssscc",".vsz",".vtm",".vtml",".vtv",".w",".w32",".wdgt",".wdgtproj",".wdl",".wdp",".wdw",".wiq",
                                            ".wixlib",".wixmsp",".wixmst",".wixobj",".wixout",".wixpdb",".wixproj",".workspace",".wpw",".wsc",".wsp",".wxi",".wxl",".wxs",".xaml"
                                            ,".xamlx",".xap",".xcappdata",".xcarchive",".xcconfig",".xcdatamodeld",".xcodeproj",".xcsnapshots",".xcworkspace",".xib",".xojo_binary_project",
                                            ".xojo_menu",".xojo_project",".xojo_xml_project",".xoml",".xpp",".xq",".xql",".xqm",".xquery",".xsd",".xt",".y",".yaml",".yml",".ymp",".ypr"]


        try:

            '''Anything from the All_users_desktop goes to shortcuts, mainly because that's all that's ever there (i think)'''
            for item in map2:
                '''This is a cmd command to move items from one folder to the other'''
                rename(self.Alldesktopdir+'\\'+item, self.desktopdir+"\\"+self.folder_names[1]+"\\"+item)

            for a in range(0, len(map)):

                if Globals.sc:
                    for b in shortcuts_extensions:
                        if str(map[a].lower()).endswith(b) and str(map[a]) != "Clean.lnk" and str(map[a]) != "Clean.exe.lnk":
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[1]+"\\"+map[a])

                if Globals.exes:
                    for b in executable_extensions:
                        if str(map[a].lower()).endswith(b) and str(map[a].lower()) != "Clean.exe":
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[3]+"\\"+map[a])

                if Globals.zips:
                    for b in zip_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[2]+"\\"+map[a])

                if Globals.img:
                    for b in images_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[4]+"\\"+map[a])

                if Globals.audio:
                    for b in music_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[5]+"\\"+map[a])

                if Globals.mov:
                    for b in movie_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[6]+"\\"+map[a])

                if Globals.txt:
                    for b in text_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[7]+"\\"+map[a])

                if Globals.programming:
                    for b in programming_languages_extensions:
                        if str(map[a].lower()).endswith(b):
                            rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[8]+"\\"+map[a])

                for b in shortcuts_extensions:
                    if str(map[a].lower()).endswith(b) and str(map[a]) != "Clean.lnk" and str(map[a]) != "Clean.exe.lnk":
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[1]+"\\"+map[a])

                for b in executable_extensions:
                    if str(map[a].lower()).endswith(b) and str(map[a].lower()) != "Clean.exe":
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[3]+"\\"+map[a])

                for b in zip_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[2]+"\\"+map[a])

                for b in images_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[4]+"\\"+map[a])

                for b in music_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[5]+"\\"+map[a])

                for b in movie_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[6]+"\\"+map[a])

                for b in text_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[7]+"\\"+map[a])

                for b in d3_work_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[8]+"\\"+map[a])

                for b in programming_languages_extensions:
                    if str(map[a].lower()).endswith(b):
                        rename(self.desktopdir+"\\"+map[a], self.desktopdir+"\\"+self.folder_names[8]+"\\"+map[a])


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
    '''Link explains the syntax https://technet.microsoft.com/en-us/library/cc725744(v=ws.11).aspx'''
    os.system(SchTasks /Create /SC DAILY /TN “My Task” /TR “C:RunMe.bat” /ST 09:00)

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
    tkMessageBox.showinfo("Complete", "Desktop clean finished.")


root = Tk()
app = App(root)
app.mainloop()
root.destroy()
