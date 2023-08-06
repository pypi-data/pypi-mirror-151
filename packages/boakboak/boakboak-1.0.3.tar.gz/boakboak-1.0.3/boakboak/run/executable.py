import errno, inspect, os, sys
import boakboak.run.settings as sts

class Executable:

    def get_executable(self, *args, appPath, **kwargs):
        """
            gets the executable from a project or package and returns it
            also checks if project is a package or not (packages are then called differently)
        """
        # simple modules are called from inside the project, packages from one level above
        self.isPackage = os.path.isfile(os.path.join(appPath, sts.packageIndicator))
        activatorPath = self.find_venv(appPath, **kwargs)
        if activatorPath.endswith(sts.activators[0]):
            self.executable = self.exec_from_dot_venv(activatorPath, *args, **kwargs)
        elif activatorPath.endswith(sts.activators[1]):
            self.executable = self.exec_from_pipfile(activatorPath, appPath, *args, **kwargs)
        if not self.executable.startswith(os.path.expanduser('~')):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), sts.activators)
        return self.executable, self.isPackage

    def exec_from_dot_venv(self, activatorPath, *args, **kwargs):
        # pipenv uses .venv files which hold path to executable. This returns that path.
        if os.path.isfile(activatorPath):
            with open(activatorPath, 'r') as f:
                venvPath = f.read().strip()
        else:
            venvPath = os.path.join(activatorPath)
        if not venvPath.endswith(sts.venvsPaths[os.name][1][-10:]):
            venvPath = os.path.join(venvPath, sts.venvsPaths[os.name][1])
        return venvPath


    def exec_from_pipfile(self, activatorPath, appPath, *args, **kwargs):
        # if a Pipfile is found, then there should be a similarily named environment
        # the path to the executable from that environment is returned
        venvsPath = os.path.join(os.path.expanduser('~'), sts.venvsPaths[os.name][0])
        # pipenvs directories start with the name of the folder in which they where created
        projectName = os.path.split(appPath)[-1]
        venvDirs = [d for d in os.listdir(venvsPath) if d.startswith(projectName)]
        if venvDirs:
            # if a matching direcory exists, then return the executable from the path
            return os.path.join(venvsPath, venvDirs[0], sts.venvsPaths[os.name][1])
        else:
            return 'not found'

    def find_venv(self, appPath, *args, **kwargs):
        """
            walks throu all folders of a project until it finds a .venv or Pipflie
            returns the path to .venv or Pipfile
            this can then be used to find the executable for the project
        """
        for activator in sts.activators:
            for d, ds, fs in os.walk(appPath):
                for f in fs:
                    if f == activator:
                        activatorPath = os.path.join(d, f)
                        return activatorPath
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), sts.activators)
