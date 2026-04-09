import sys, os, json
from os import path, mkdir, listdir, rename, environ, rmdir


def get_desktop_path():
    if sys.platform == "win32":
        return path.join(environ["USERPROFILE"], "Desktop")

    elif sys.platform in ["linux", "darwin"]:
        return environ.get("TEST_DIR") or path.join(environ["HOME"], "Desktop")
    raise NotImplementedError(f"{sys.platform} not supported")


class OrganiseDesktop:
    """
    Contains desktop organisation helper functions
    """

    pattern_rules = {}  # filename keyword → category overrides
    extensions = {}
    separator = "/"
    desktopdir = ""
    Alldesktopdir = None

    def __init__(self, extensions):
        self.desktopdir = get_desktop_path()
        # Pull out _PatternRules before passing to extension logic
        self.pattern_rules = extensions.pop("_PatternRules", {})
        self.extensions = extensions

    def create_dir_path(self, directory):
        return os.path.join(self.desktopdir, directory)

    def makedir(self, folders_to_make):
        """
        This function makes the needed folders if they are not already found.
        For all the folders in the folder_to_make list, if that folder does not
        exist on the main_desktop, create that folder.
        """
        directories = [self.create_dir_path(directory) for directory in folders_to_make]
        for directory in directories:
            if not path.isdir(directory):
                mkdir(directory)

    def removedir(self, folders_i_made):
        """
        This function will check folders that this program made.
        If the folder is empty, it will delete that folder. simple job.
        """
        directories = [self.create_dir_path(directory) for directory in folders_i_made]

        for directory in directories:
            if not listdir(directory):
                rmdir(directory)

    def match_by_pattern(self, filename):
        """
        Check filename (case-insensitive) against PatternRules keywords.
        Returns the matching category name, or None if no match found.
        Runs BEFORE extension matching, so game/IDE/tool shortcuts are
        routed correctly instead of falling into generic Shortcuts/.
        """
        name_lower = filename.lower()
        for category, keywords in self.pattern_rules.items():
            # Only match if this category folder actually exists in extensions
            if category not in self.extensions:
                continue
            for keyword in keywords:
                if keyword.lower() in name_lower:
                    return category
        return None

    def mover(self):
        """
        Moves desktop files into their sorted folders.

        Priority:
          1. Skip this program's own shortcuts
          2. PatternRules keyword match  (Games, Dev Tools, System Tools)
          3. Extension match             (Images, Music, Text, etc.)
          4. Folder catch-all            (unrecognised directories → Folders/)
          5. Log anything that didn't sort
        """
        content = listdir(self.desktopdir)

        # On older Windows, merge All Users desktop first
        if sys.platform == "win32" and self.Alldesktopdir:
            try:
                if sys.getwindowsversion().major < 10:
                    for item in listdir(self.Alldesktopdir):
                        rename(
                            os.path.join(self.Alldesktopdir, item),
                            os.path.join(self.desktopdir, item),
                        )
            except AttributeError:
                pass

        # Only process items that aren't already category folders
        to_be_cleaned = [
            entry
            for entry in content
            if entry not in self.extensions and not entry.startswith(".")
        ]

        for item in to_be_cleaned:
            # Skip this program's own shortcuts
            if item in ("Clean.lnk", "Clean.exe.lnk"):
                continue

            src = os.path.join(self.desktopdir, item)
            found = False

            # ── Priority 1: Pattern match (keyword in filename) ──────────────
            pattern_category = self.match_by_pattern(item)
            if pattern_category:
                dst = os.path.join(self.desktopdir, pattern_category, item)
                try:
                    rename(src=src, dst=dst)
                    found = True
                    print(f"[Pattern] {item!r}  →  {pattern_category}/")
                except PermissionError:
                    print(f"[Locked]  {item!r}  (file in use)")
                except Exception as e:
                    print(f"[Error]   {item!r}  {e}")

            # ── Priority 2: Extension match ───────────────────────────────────
            if not found:
                item_lower = item.lower()
                for sorting_folder, ext_list in self.extensions.items():
                    for extension in ext_list:
                        if item_lower.endswith(extension):
                            dst = os.path.join(self.desktopdir, sorting_folder, item)
                            try:
                                rename(src=src, dst=dst)
                                found = True
                            except PermissionError:
                                print(f"[Locked]  {item!r}  (file in use)")
                            except Exception as e:
                                print(f"[Error]   {item!r}  {e}")
                            break  # stop checking extensions for this folder
                    if found:
                        break  # stop checking sorting folders

            # ── Priority 3: Folder catch-all ──────────────────────────────────
            if not found and os.path.isdir(src) and "Folders" in self.extensions:
                dst = os.path.join(self.desktopdir, "Folders", item)
                try:
                    rename(src=src, dst=dst)
                    found = True
                except PermissionError:
                    print(f"[Locked]  {item!r}  (folder in use)")
                except Exception as e:
                    print(f"[Error]   {item!r}  {e}")

            if not found:
                print(f"Did not sort: {item!r}")

    def write_log(self, content):
        """
        This function writes the two lists of all the items left on the desktop
        just in case something isn't right and we need a log.
        """
        log_dir = path.dirname(os.getcwd()) + "/log"
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        with open(log_dir + "/modifications.log", "w") as f:
            f.write(
                "This is a list of all items on your desktop before it was cleaned.\n"
                "Email this list to kalimbatech@gmail.com if anything is not working as planned.\n\n"
            )
            for desktop_entry in content:
                for i in desktop_entry:
                    f.write(i + "\n")


def organise_desktop(extensions):
    """
    Cleans up the desktop
    """
    # Find working directory
    pwd = os.path.dirname(os.path.abspath(__file__))

    # The oh-so-magnificent main function keeping the stuff in order

    # Initialize the OrganiseDesktop class
    organizer = OrganiseDesktop(extensions)

    # Make the directories
    organizer.makedir(organizer.extensions)

    # Move the files to their appropriate locations
    organizer.mover()

    # Remove directories created by this program but empty
    organizer.removedir(organizer.extensions)

    # Get the maps of the directories
    maps = organizer.list_directory_content()

    # Log the original files
    organizer.write_log(maps)


def undo():
    """
    Restores the changes from organising your desktop
    """

    Extensions = json.load(
        open(os.path.dirname(os.path.abspath(__file__)) + "/Extension.json")
    )  # noqa

    desk_to_dir = get_desktop_path()
    desktop_items = listdir(desk_to_dir)

    for folder in desktop_items:
        if folder in Extensions:
            contents = listdir(path.join(desk_to_dir, folder))
            for file_name in contents:
                try:
                    rename(
                        src=os.path.join(desk_to_dir, folder, file_name),
                        dst=os.path.join(desk_to_dir, file_name),
                    )
                except Exception:
                    print(f"File is being used by another process: {file_name}")
            try:
                rmdir(os.path.join(desk_to_dir, folder))
            except Exception:
                pass


if __name__ == "__main__":
    organise_desktop()
