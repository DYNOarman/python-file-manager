# **Python CLI File Manager**

A lightweight, cross-platform command-line file explorer built with **Python**. This tool allows users to navigate, manage, and search their file system using a shell-like interface with color-coded feedback.

## **Features**

- **Cross-Platform**: Automatically detects OS (**Windows**, **Linux**, **macOS**) and handles drive paths accordingly.
- **Color-Coded Interface**: Visual feedback for directories, files, errors, and warnings (**Blue**, **Green**, **Red**, **Yellow**).
- **Standard Operations**: Create, remove, copy, move, and rename files and directories.
- **Smart Navigation**: Supports relative paths (`.`, `..`), home directory (`~`), and drive root (`*`).
- **Search Functionality**: Robust search tool with wildcard support (`*pattern*`) and filtering by type.
- **Safety First**: Includes confirmation prompts for destructive actions (deletions, moves).

📋 **Requirements**

- **Python 3.x**
- **Standard Libraries Only**: No external dependencies or pip install required. The script uses `pathlib`, `shlex`, `os`, `shutil`, `datetime`, and `platform`.

🚀 **Installation & Usage**

### Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Navigate to the Directory
```bash
cd YOUR_REPO_NAME
```

### Run the Script
```bash
python File_Manager.py
```


🎮 **Command Reference**

Once the program is running, you can use the following commands at the >> prompt:

| **Command** | **Usage**          | **Description** |
|-------------|---------------------|-----------------|
| **ls**      | ls [-d] [path]     | List items. Use -d for detailed view (size, date). |
| **cd**      | cd <path>          | Change current working directory. |
| **cwd**     | cwd                | Display the current working directory path. |
| **mkdir**   | mkdir <name...>    | Create one or more new directories. |
| **rmdir**   | rmdir <name...>    | Remove empty directories. |
| **touch**   | touch <name...>    | Create one or more new files. |
| **rm**      | rm <name...>       | Delete files. |
| **cp**      | cp <source> <dest> | Copy a file or directory. |
| **mv**      | mv <source> <dest> | Move or rename a file or directory. |
| **sh**      | sh [options] <pat> | Search for files/folders. See Search below. |
| **help**    | help [command]     | Show the help menu or specific command help. |
| **exit**    | exit               | Close the program. |

**Special Paths**

- `~` : Home Directory
- `*` : Root/Spawn Directory
- `.` : Current Directory
- `..`: Parent Directory

🔍 **Search (sh) Usage**

The search command is powerful. You can use wildcards and flags:

### Flags
- `-f` : Files only
- `-d` : Directories only
- `-b` : Search from base dir

### Patterns
- `*.py` : Ends with `.py`
- `test*` : Starts with `test`
- `*data*` : Contains `data`

### Example
```bash
>> sh -f *.txt
```

📸 **Usage Examples**

1. Listing files with details:

```bash
>> ls -d
    2023-10-25 10:00:00  <DIR>      Documents
    2023-10-25 10:05:00  1.20MB     image.png
```

2. Creating and moving a file:

```bash
>> mkdir Projects
>> touch main.py
>> mv main.py Projects
```

3. Searching for Python files:

```bash
>> sh -f *.py
```

🤝 **Contributing**

Contributions are welcome! If you have suggestions for new features (like file content reading or zipping), feel free to fork the repository and submit a pull request.

### Steps to Contribute
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

📄 **License**

This project is open source and available under the **MIT License**.

Created by [Your Name]