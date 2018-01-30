# Surepatch CLI Application
Surepatch CLI App - is a complex solution for your projects and OS security.
This application is designed to work with the Surepatch Project without using the web interface. You can use it both in manual and automatic mode in operating systems with a graphical interface and on server stations without a graphical interface. You can use the application as part of scripts for automatic builds to test the security of your application and the operating system packages after each change. You can constantly maintain the current state of security packages, including the application in the schedule. You can completely control your platforms, projects and component sets without using a browser, receive actual reports and solutions from periodically updated vulnerability database.
# Features
- Main Features:
    - Create, delete, archive and restore Platforms
    - Create, delete, archive and restore Projects
    - Create Component Sets
    - Print and export to files Platforms, Projects, Components and Issues
- Operating modes:
    - Automatic
    - Manual
- Supported formats:
    - System formats for package manager like shell, python pip, gem, npm.
    - User format for special files with custom packages
- Packages Management:
    - Collect Packages from Windows, MacOS, Linux Operation Systems
    - Collect Packages from Python PIP and requirements.txt sources
    - Collect Packages from NPM, NodeJS package.json and package-lock.json sources
    - Collect Packages from Ruby, Gemfile and Gemfile.lock spurces
    - Collect Packages from user format file resources and in interactive mode

# Installation
## From pip install
...
## From OS package
...
## From Gihtub
[Package](link)

# Usage examples
## CLI App arguments
|Argument|Value|Description|
|-|-|-|
|--team| <your_team> | Your Team on Surepatch project|
|--user| <your_username> | Your username (e-mail)|
|--password| <your_password> | Your password|
|--action| <action_type> | CLI App action:|
| | save_config | Save account paramters |
| | create_platform | Create New Platform |
| | create_project | Create New Project in defined Platform |
| | create_set | Create New Components Set in defined Platform/Project|
| | delete_platform | Delete Platform |
| | delete_project | Delete Project in defined Platform|
| | archive_platform | Archive Platform |
| | archive_project | Archive Project for defined Platform |
| | restore_platform | Restore Platform |
| | restore_project | Restore Project in defined Platform |
| | show_platforms | Print all Platforms in account |
| | show_projects | Print all Projects in defined Platform |
| | show_set | Print current component set for defined Platform/Project |
| | show_issues | Print issues for defined Platform/Project |
|--platform| <platform_name> | Name of Platform for different actions|
|--description| <platform_description>| Description of Platform |
|--project|<project_name>| Name of Project for different actions |
|--set|<set_name>| Name of set for different actions |
|--target|<target_type>| CLI App Targets: |
||os| Target is Operation system Packages |
||pip| Target is Python pip Packages |
||req| Target is Python PIP Packages |
||requirements| Target is Python requirements.txt file |
||npm| Target is NPM Packages |
||npm_local| Target is NPM Packages from defined directory |
||package_json| Target is NPM package.json file |
||package_lock_json| Target is NPN package-lock.json file |
||gem| Target is Ruby gem Packages |
||gemfile| Target is Ruby Gemfile source |
||gemfile_lock| Target is Ruby Gemfile.lock source |
|--method:|<method_type>|CLI App Methods:|
||auto|Collect Packages automatically |
||manual|Collect Packages in interactive mode |
|--format|<format_type>|CLI App Formats:|
||system| System Format Packages (from package managers or OS) |
||user| User defined Packages format <name>=<version>|
|--file|<path_to_file_or_dir>| Path to file with Packages or Directory |

# CLI App Config:
### Create local config file
A local configuration file will be created in home directory (~/.surepatch.yaml).
```sh
@ surepatch.py --action=save_config --team=testers --user=user@gmail.com --password=test_password
```
# Platforms:
### Create your first Platform
```sh
@ surepatch.py --action=create_platform --platform=autotest1 --description="New Platform for Autotest"
```
# Projects:
### Create Project from OS Packages, collected by shell command inside CLI App. Note, that this operation require root privileges
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_os_none --target=os --method=auto --format=system
```
### Create Project from OS Packages, pre-uploaded to an external file, for example /home/user/os_packages.txt
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_os_path --target=os --method=auto --format=system --file=/home/user/os_packages.txt
```
### Create Project from Python PIP Packages, collected by shell command inside CLI App.
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_pip_none --target=pip --method=auto --format=system
```
### Create Project from Python PIP Packages, pre-unloaded to an external file, for example /home/user/pip_freeze_packages.txt
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_pip_path --target=pip --method=auto --format=system --file=/home/user/pip_freeze_packages.txt
```
### Create Project from Python Packages, collected in requirements.txt
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_req_path --target=req --method=auto --format=system --file=c:\requirements.txt
```
### Create Project from NPM Packages, collected by shell command (npm list --json) inside CLI App (from root path)
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_npm_none --target=npm --method=auto --format=system
```
### Create Project from NPM Packages, collected by shell command (npm list --json) inside ALI App (from defined directory), for example /home/user/workspace/node_project
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_local_none --target=npm_local --method=auto --format=system --file=/home/user/workspace/node_project
```
### Create Project from NPM Packages, collected by shell command (npm list --json) before and pre-unloaded to an external file, for example /home/user/npm.txt
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_npm_path --target=npm --method=auto --format=system --file=/home/user/npm.txt
```
### Create Project from NPM Packages, collected in packaje.json file
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_npm_package_json --target=package_json --method=auto --format=system --file=c:\package.json
```
### Create Project from NPM Packages, collected in package-lock.json file
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_npm_package_lock_path --target=package_lock_json --method=auto --format=system --file=c:\package-lock.json
```
### Create Project from Ruby Packages, collected by shell command
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_gem_none --target=gem --method=auto --format=system
```
### Create Project from Ruby Packages, collected by shell command before and pre-unloaded to an external file, for example /home/user/gem.list
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_gem_path --target=gem --method=auto --format=system --file=/home/user/gem.list
```
### Create Project from Ruby Packages, collected in Gemfile, for example /home/user/Gemfile
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_gemfile_path --target=gemfile --method=auto --format=system --file=/home/user/Gemfile
```
### Create Project from Ruby Packages, collected in Gemfile.lock, for example /home/user/Gemfile.lock
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_gemfile_lock_path --target=gemfile_lock --method=auto --format=system --file=c:\Gemfile.lock
```
### Create Project from User defined source file, for example /home/user/user_packages.txt, where packages defined as lines in <name>=<version> format
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_any_user_path  --method=auto --format=user --file=c:\user_packages.txt
```
### Create Project from User defined format in interactive mode
```sh
@ surepatch --action=create_project --platform=autotest1 --project=autotest_any_user_none --method=manual --format=user
```
# Components:
###
### Create set - OS packages, collected by shell command
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=os_none.1 --target=os --method=auto --format=system
```
### Create set autotest_os_path - OS packages, collected from shell command, unloaded to file
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=os_path.1 --target=os --method=auto --format=system --file=c:\windows_packages.txt
```
### Create set autotest_pip_none - PIP Packages, collected from shell command
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=pip_none.1 --target=pip --method=auto --format=system
```
### Create set autotest_pip_path - PIP packages, collected from shell command, unloaded to file
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=os_path.1 --target=pip --method=auto --format=system --file=c:\pip_freeze_packages.txt
```
### Create set autotest_req_path - Python packages from requirements.txt
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=req_path.1 --target=req --method=auto --format=system --file=c:\requirements.txt
```
### Create set autotest_npm_none - NPM packages, collected from shell command (npm list --json) from root dir
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=npm_none.1 --target=npm --method=auto --format=system
```
### Create set autotest_npm_path - NPM packages, collected from shell command (npm list --json) from root dir, unloaded to file
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=npm_path.1 --target=npm --method=auto --format=system --file=c:\npm.txt
```
### Create set autotest_local_none - NPM packages, collected from shell command (npm list --json) from local dir
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=npm_local_path.1 --target=npm_local --method=auto --format=system --file=c:\workspace\node
```
### Create set autotest_npm_package_lock_path - NPM packages, collected from package-lock.json file
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=npm_package_json_lock_path.1 --target=package_lock_json --method=auto --format=system --file=c:\package-lock.json
```
### Create set autotest_npm_package_json - NPM packages, collected from package.json file
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=npm_package_json_path.1 --target=package_json --method=auto --format=system --file=c:\package.json
```
### Create set autotest_gem_none - Ruby packages, collected from shell command
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test  --set=gem_none.1 --target=gem --method=auto --format=system
```
### Create set autotest_gem_path - Ruby packages, collected from shell commend, unloaded to file
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=gem_path.1 --target=gem --method=auto --format=system --file=c:\gem.list
```
### Create set autotest_gemfile_path - Ruby packages, collected from Gemfile
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=gem_gemfile_path.1 --target=gemfile --method=auto --format=system --file=c:\Gemfile
```
### Create set autotest_gemfile_path - Ruby packages, collected from Gemfile.lock
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=gem_gemfile_lock_path.1 --target=gemfile_lock --method=auto --format=system --file=c:\Gemfile.lock
```
### Create set autotest_any_user_path - User packages formatted as name=version
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=user_path.1  --method=auto --format=user --file=c:\user_packages.txt
```
### Create set autotest_any_user_none - User packages asked from console
```sh
@ surepatch --action=create_set --platform=autotest1 --project=autotest_set_test --set=user_manual.1 --method=manual --format=user
```
# Show:
### Show platforms
```sh
@ surepatch --action=show_platforms
```
### Show projects
```sh
@ surepatch --action=show_projects --platform=autotest1
```
### Show set
```sh
@ surepatch --action=show_set --platform=autotest1 --project=autotest_set_test
```
### Show issues
```sh
@ surepatch --action=show_issues --platform=autotest1 --project=autotest_set_test
```

# License
...
# (c) WebSailors, 2018.