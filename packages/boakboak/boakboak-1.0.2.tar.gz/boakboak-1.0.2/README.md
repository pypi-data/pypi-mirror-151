<!-- README.md -->

# Aliased Shell runner for pyhton projects

This runs your python projects/packages from anywhere inside your shell, without the need to install the package or change directory. 
NOTE: Currently only pipenvs are implemented. Only tested on Windows 10. 
Feel free to clone and extend.


# Install
- pipenv install boakboak


### dependencies
- python 3.6 - 3.10
- pyyaml



# Problem boakboak tries to solve?
I have some python based services, which I want to run occasionally from anywhere inside the
shell using an aliased shell call.

Most importantly: I dont want to install all these services into my main environment.

For example:
- I want to save my files to a archive directory, for which I have a archive.py module.
- I want to convert a table to a json or yaml file for which I use a convert.py package.

I want to be able to flexibly add/remove these services from the aliased shell call.


# Usage
Create and name a yml file like the shell call alias you like to use.
Example, name file like: /apps/packageAlias.yml -> call like: pmg packageAlias -my parameters


## Steps

#### Example: project which uses imaginary archive.py module to archive files an folders:
- I will run "python -m archive -c 'my_archive_comment'" from the shell, as I always do.
- From the executed shell command, I copy the path, cmds and optional args to archive.yml
- I save the created .yml file in: boakboak/boakboak/apps/archive.yml
- The resulting .yml file has to look something like this: boakboak/boakboak/apps/archive.yml

From the shell, I now call:
- pmg archive -c 'my_archive_comment'


## How it works

boakboak will use the parameters from apps/packageAlias.yml, to run your project/package
- It takes appPath and finds your project/package (returns the first dir with .venv in it)
- It uses .venv file/folder or project name (if Pipfile is found), to identify the executable
- It uses a subprocess call, to run your cmds using identified python.exe



## Release notes
### Version 1.0.0, 05-2022
- python 3.6 - 3.10
- venvs: pipenv
- os: tested on Windows 10