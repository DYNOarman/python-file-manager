from pathlib import Path                # library for working with file paths
import shlex                            # library for shell like operations
import os                               # library for working with file system
import shutil                           # library for working with file system
import datetime                         # library for working with date and time
import platform                         # library for working with operating system


# defining situational colors for easy use
class Colors:
    OKBLUE = '\033[94m'                 # blue
    OKGREEN = '\033[92m'                # green
    WARNING = '\033[93m'                # yellow
    CANCEL = '\033[31m'                 # dim red
    ERROR = '\033[91m'                  # bright red
    ENDC = '\033[0m'                    # reset colors

# centralized print function
def console(*messages, end="\n"):
    colors = {
        "info": Colors.OKBLUE,
        "success": Colors.OKGREEN,
        "warning": Colors.WARNING,
        "cancel": Colors.CANCEL,
        "error": Colors.ERROR,
        "reset": Colors.ENDC
    }

    output_string = ""
    for message, type in messages:
        color = colors.get(type, Colors.ENDC)
        output_string += f"{color}{message}{Colors.ENDC}"

    print(output_string, end=end)


# gives a readable size of bytes
def format_size(raw_size):
    if raw_size < 1024:
        size = f"{raw_size:.2f}" + "B"
    elif 1048576 > raw_size > 1024 :
        size = f"{(raw_size / 1024):.2f}" + "KB"
    elif 1073741824 > raw_size > 1048576:
        size = f"{(raw_size / 1048576):.2f}" + "MB"
    else:
        size = f"{(raw_size / 1073741824):.2f}" + "GB"
    return size


# ask user for confirmation for the operation
def confirmation(operation):
    choice = input(f"{Colors.WARNING}{operation.upper()} (Yes/no): {Colors.ENDC}").strip().lower()

    if choice in ("yes", "y", ""):
        return True
    elif choice in ("no", "n"):
        console("Operation cancelled", "cancel")
        return False
    else:
        console("Invalid choice, Operation cancelled", "cancel")
        return False


# gives an absolute path
def absolute_path(path, exists=True):
    try:
        if path == "*":
            return Path(drive_spawn()[0])
        elif path == "~":
            return Path(Path.home())
        else:
            return Path(path).expanduser().resolve(strict=exists)
    except Exception as e:
        return False


# resolves and validates the final destination path for operations
def resolve_destination_path(source_path, destination_path):
    # checking and validating the destination_path
    if destination_path.exists() and destination_path.is_dir():
        final_path = absolute_path(destination_path/source_path.name, exists=False)

        if final_path.exists():
            raise FileExistsError(f"Destination already exists: {final_path}")
        
        return final_path
    
    if not destination_path.exists() and destination_path.parent.exists():
        return destination_path
    
    raise ValueError(f"Destination path not found: {destination_path}")


# gives drive list currently available in the system
def drive_spawn():
    system = platform.system()
    system_drives = []

    # windows system
    if system == "Windows":
        drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if Path(f"{d}:\\").exists()]
        for drive in drives:
            system_drives.append(drive)
        
    # linux or mac system
    elif system == "Linux" or system == "Darwin":
        system_drives.append("/")

    # something else
    else:
        console(f"System didn't recognised: {system}", "error")
        return []

    return system_drives


# gives current working directory path
def current_working_path():
    return Path.cwd()


# changes the current working directory
def change_directory(path):
    current_path = current_working_path()
    destination_path = absolute_path(path)

    if destination_path:
        os.chdir(destination_path)
        console((current_path, "info"), ("  --->  ", "success"), (destination_path, "info"))


# lists items from the given path or current working directory
def list_items(list_type, path):
    if path != None:
        path = absolute_path(path)
    else:
        path = current_working_path()

    sorted_files = []
    sorted_directories = []

    if path:
        # sort files and directories
        for item in list(path.iterdir()):
            if item.is_file():
                sorted_files.append(item)
            elif item.is_dir():
                sorted_directories.append(item)

        # listing in simple layout
        if list_type == "simple":
            for directory in sorted_directories:
                console((directory.name, "info"), end="   ")
            for file in sorted_files:
                console((file.name, "success"), end="   ")
            print()

        # listing in detailed layout
        elif list_type == "detailed":
            for lists in [sorted_directories, sorted_files]:
                for item in lists:
                    data = os.stat(item)
                    creation_date = datetime.datetime.fromtimestamp(data.st_ctime).strftime('%Y-%m-%d   %H:%M:%S')
                    size = format_size(data.st_size)

                    if  lists == sorted_directories:     
                        console((f"    {creation_date:<22}  {'<DIR>':<8}  {item.name:<20}", "info"))
                    elif lists == sorted_files:
                        console((f"    {creation_date:<22}  {size:<8}  {item.name:<20}", "success"))


# checks if the given name is valid
def name_validation(name):
    invalid_chars = set('\\/:*?"<>|')

    if not any(char in invalid_chars for char in name):
        return True
    else:
        console((f"Invalid characters: {name}  --->  ({', '.join(str(char) for char in invalid_chars)})", "error"))


# create or remove files and directories
def create_remove(names, operation, target):
    if confirmation(f"{operation} {target}"):
        # create files and directories
        if operation == "Create":
            for name in names:
                if name_validation(name):
                    path = absolute_path(current_working_path()/name, exists=False)

                    try:
                        if target == "File":
                            path.touch()
                        elif target == "Directory":
                            path.mkdir()
                        console((f"{target} created: {path.name}", "success"))
                    except FileExistsError:
                        console((f"{target} already exists: {path.name}", "warning"))

        # remove files and directories
        elif operation == "Remove":
            for name in names:
                path = absolute_path(current_working_path()/name)
                
                if path:
                    try:
                        if target == "File" and path.is_file():
                            path.unlink()
                        elif target == "Directory" and path.is_dir():
                            path.rmdir()
                        else:
                            console((f"Not a {target}: {path.name}", "error"))
                            return
                        console((f"{target} deleted: {path.name}", "cancel"))
                    except OSError:
                        console((f"{target} is not empty: {path.name}", "warning"))
                else:
                    console((f"{target} not found: {name}", "error"))


# match extensions of given files
def extension_validation(source_path, destination_path):
    if source_path.suffixes == destination_path.suffixes:
        return True
    else:
        console(("Extension mismatch: ", "warning"), (source_path, "info"), ("  --->  ", "warning"), (destination_path, "info"))


# copy, move or rename files and directories
def copy_move_rename(paths, operation):
    try:
        source_path = absolute_path(paths[0])
        destination_path = resolve_destination_path(source_path, absolute_path(paths[1], exists=False))
    except (FileExistsError, ValueError, Exception) as e:
        console((e, "error"))
        return

    if confirmation(operation) and extension_validation(source_path, destination_path) and name_validation(destination_path.name):
        # copy files and directories
        if operation == "Copy":
            if source_path.is_file():
                shutil.copy2(source_path, destination_path)
            elif source_path.is_dir():
                shutil.copytree(source_path, destination_path)
            console(("Copied ", "success"), (source_path, "info"), ("  --->  ", "success"), (destination_path, "success"))

        # move files and directories
        elif operation == "Move":
            if source_path.is_dir():
                try:
                    destination_path.relative_to(source_path)
                    console(("Cannot move a directory into itself", "error"))
                    return
                except ValueError:
                    pass
                
            shutil.move(source_path, destination_path)
            console(("Moved ", "success"), (source_path, "info"), ("  --->  ", "success"), (destination_path, "info"))


# searches for files and directories, matching with patterns within a given directory
def search(search_directory, search_type, pattern_list):
    searched_list = set()
    result_list = []

    try:
        # serach and add matching items into searched_list
        for pattern in pattern_list:
            for item in search_directory.rglob(pattern):
                searched_list.add(item)

        for item in searched_list:
            if item.is_file() and "file" in search_type:
                result_list.append(item)
            elif item.is_dir() and "directory" in search_type:
                result_list.append(item)

        result_list = sorted(result_list)
        # show the result_list in formatted layout
        for index, item in enumerate(result_list, start=1):
            console((f"{index:<5}", "success"), (item, "info"))
            
    except Exception as e:      
        console((e, "error"))
        return

    console((f"\nResult found: {len(result_list)}", "info"))
    # goto the parent directory of any result
    if len(result_list) > 0:
        choice = input(f"{Colors.WARNING}Go to Result 1-{len(result_list)}: {Colors.ENDC}").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(result_list):
            change_directory(result_list[int(choice) - 1].parent)
        else:
            return


# displays the help guide
def help_guide(inputs):
    guides = {
        "rules": (
            f"\n{Colors.OKGREEN}Rules:"
            f"\n{Colors.OKBLUE}  [...]      optional and can be skipped"
            "\n  <...>      compulsary"
            "\n  path       path of the file or directory"
            "\n  name       name of the file or directory"
            "\n  command    name of the command"
            f"\n\n{Colors.OKGREEN}Special paths:"
            f"\n{Colors.OKBLUE}  *          spawn directory"
            "\n  ~          home directory"
            "\n  .          current working directory"
            f"\n  ..         parent directory of the current working directory{Colors.ENDC}"
        ),
        "ls": (
            f"\n{Colors.OKGREEN}  ls [options] [path]"
            f"\n{Colors.OKBLUE}    List files and directories"
            f"\n\n{Colors.OKGREEN}    [options]:"
            f"\n{Colors.OKBLUE}      -d        Detailed view{Colors.ENDC}"
        ),
        "cwd": (
            f"\n{Colors.OKGREEN}  cwd"
            f"\n{Colors.OKBLUE}    Show current working directory{Colors.ENDC}"
        ),
        "cd": (
            f"\n{Colors.OKGREEN}  cd <path>"
            f"\n{Colors.OKBLUE}    Change current directory{Colors.ENDC}"
        ),
        "mkdir": (
            f"\n{Colors.OKGREEN}  mkdir <name> [name...]"
            f"\n{Colors.OKBLUE}    Create one or more directories{Colors.ENDC}"
        ),
        "rmdir": (
            f"\n{Colors.OKGREEN}  rmdir <name> [name...]"
            f"\n{Colors.OKBLUE}    Remove empty directories{Colors.ENDC}"
        ),
        "touch": (
            f"\n{Colors.OKGREEN}  touch <name> [name...]"
            f"\n{Colors.OKBLUE}    Create one or more files{Colors.ENDC}"
        ),
        "rm": (
            f"\n{Colors.OKGREEN}  rm <name> [name...]"
            f"\n{Colors.OKBLUE}    Remove files{Colors.ENDC}"
        ),
        "mv": (
            f"\n{Colors.OKGREEN}  mv <source_path> <destination_path>"
            f"\n{Colors.OKBLUE}    Move or rename file or directory{Colors.ENDC}"
        ),
        "cp": (
            f"\n{Colors.OKGREEN}  cp <source_path> <destination_path>"
            f"\n{Colors.OKBLUE}    Copy file or directory{Colors.ENDC}"
        ),
        "sh": (
            f"\n{Colors.OKGREEN}  sh [options] <pattern...>"
            f"\n{Colors.OKBLUE}    Search files and directories by the name patterns"
            f"\n\n{Colors.OKGREEN}    [options]:"
            f"\n{Colors.OKBLUE}      -f        Files only"
            "\n      -d        Directories only"
            "\n      -b        Search from base directory"
            f"\n\n{Colors.OKGREEN}    <pattern>:"
            f"\n{Colors.OKBLUE}      pattern      File or directory name"
            "\n      pattern*     File or directory name starts with pattern"
            "\n      *pattern     File or directory name ends with pattern"
            f"\n      *pattern*    File or directory name contains pattern{Colors.ENDC}"
        ),
        "help": (
            f"\n{Colors.OKGREEN}  help [command]"
            f"\n{Colors.OKBLUE}    Show help information{Colors.ENDC}"
        ),
        "exit": (
            f"\n{Colors.OKGREEN}  exit"
            f"\n{Colors.OKBLUE}    Exit the program{Colors.ENDC}"
        )
    }

    # show guide based on user inputs
    if inputs:
        for command in inputs:
            if command in guides:
                print(f"{guides[command]}")
            else:
                print(f"{Colors.ERROR}Unknown command: {command}{Colors.ENDC}")

    # show the complete guide
    else:
        print(guides["rules"])
        print(f"\n{Colors.OKGREEN}Commands:{Colors.ENDC}")
        for command in guides.keys():
            if command != "rules":
                print(f"{guides[command]}")     
        

# gets user inputs
def user_inputs():
    while True:
        # get input_command and seperate them as function, parameters and arguments
        try:
            input_command = shlex.split(input("\n>> ").strip())
            function = input_command[0]
            parameters = []
            arguments = []

            for piece in input_command[1:]:
                if piece.startswith("-"):
                    parameters.append(piece)
                else:
                    arguments.append(piece)
        except IndexError:
            continue
        except ValueError as e:
            console((e, "error"))
            continue

        # if the function is "ls"
        if function == "ls" and len(parameters) <= 1 and len(arguments) <= 1:
            if "-d" in parameters:
                list_type = "detailed"
                parameters.remove("-d")
            else:
                list_type = "simple"

            if arguments:
                path = arguments[0]
            else:
                path = None

            if parameters:
                console((f"Invalid parameter: {parameters[0]}", "error"))
            else:
                list_items(list_type, path)

        # if the function is "cwd"
        elif function == "cwd" and not parameters and not arguments:
            console((current_working_path(), "info"))

        # if the function is "cd"
        elif function == "cd" and not parameters and len(arguments) == 1:
            change_directory(arguments[0])

        # if the function is "mkdir"
        elif function == "mkdir" and not parameters and arguments:
            create_remove(arguments, "Create", "Directory")    

        # if the function is "rmdir"
        elif function == "rmdir" and not parameters and arguments:
            create_remove(arguments, "Remove", "Directory")

        # if the function is "touch"
        elif function == "touch" and not parameters and arguments:                  
            create_remove(arguments, "Create", "File")

        # if the function is "rm"
        elif function == "rm" and not parameters and arguments:
            create_remove(arguments, "Remove", "File")

        # if the function is "mv"
        elif function == "mv" and not parameters and len(arguments) == 2:
            copy_move_rename(arguments, "Move")

        # if the function is "cp"
        elif function == "cp" and not parameters and len(arguments) == 2:
            copy_move_rename(arguments, "Copy")

        # if the function is "sh"
        elif function == "sh" and len(parameters) <= 2 and arguments:
            if "-d" in parameters:
                search_type = ["directory"]
                parameters.remove("-d")
            elif "-f" in parameters:
                search_type = ["file"]
                parameters.remove("-f")
            else:
                search_type = ["file", "directory"]

            if "-b" in parameters:
                base_path = absolute_path("D:/Admin")
                parameters.remove("-b")
            else:
                base_path = current_working_path()

            search(base_path, search_type, arguments)

        # if the function is "help"
        elif function == "help":
            help_guide(arguments)

        # if the function is "exit"
        elif function == "exit":
            console(("Exiting File Explorer. Goodbye!", "success"), end="\n\n")
            exit()

        # if the command is invalid
        else:
            console(("Invalid inputs", "error"), end="\n\n")


# initiate starter functionss
def start_program():
    console(("Welcome to the File Explorer!", "warning"))
    drives = drive_spawn()

    # if drives are available
    if drives:
        os.chdir(drives[0])
        user_inputs()


# starts the program
if __name__ == "__main__":
    start_program()