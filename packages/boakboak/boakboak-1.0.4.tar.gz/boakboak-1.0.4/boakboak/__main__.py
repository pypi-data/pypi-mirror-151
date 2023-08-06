# __main__.py

import os, sys, yaml
import boakboak.run.settings as sts
from boakboak.run.executable import Executable
import boakboak.run.boakboak as boakboak


def get_params(apps, *args):
    # getting runtime parameters and returning them
    # takes apps name and returns a list of dictionaries
    try:
        params = {}
        for app in apps:
            with open(os.path.join(sts.appsParamsPath, f"{app}{sts.paramsFileExt}")) as f:
                params.update({app: yaml.safe_load(f)})
    except Exception as e:
        print(f"{sts.exceptionMsg}, {e = }")
        exit()
    return params

def get_apps(alias, *args):
    if alias == sts.allApps:
        apps = [f[:-4] for f in os.listdir(sts.appsParamsPath) if f.endswith(sts.paramsFileExt)]
        assert apps, f"apps not found: {alias}"
    else:
        apps = [f"{alias}"]
    return apps

def run_apps(*args, params):
    # running the called python module
    for app, pars in params.items():
        pars['executable'], isPackage = Executable(*args, **pars).get_executable(app, **pars)
        boakboak.crow(*args[1:], isPackage=isPackage, **pars)

def main(*args):
    # when installed, args have to come via sys.argv not from main(*sys.argv)
    if not args: args = sys.argv[1:]
    if not args:
        print(f"\n{sts.appsParamsPath = }", end='')
        print(f"{sts.sysArgsException}: \n\t{os.listdir(sts.appsParamsPath)}\n")
        exit()
    apps = get_apps(*args)
    params = get_params(apps, *args)
    if params: run_apps(*args, params=params)

if __name__ == '__main__':
    main(*sys.argv[1:])