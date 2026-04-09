import Clean, pickle, os

settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.txt")

with open(settings_path, "rb") as setting_file:
    folders = pickle.load(setting_file)

Clean.main(folders)
