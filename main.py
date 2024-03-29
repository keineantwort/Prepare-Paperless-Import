import os
import shutil

import yaml
import logging
from log import init_logger
from model import *

FILEINPUT = "diverse.yaml"
log = init_logger(log_level=logging.DEBUG, logfile=f"{FILEINPUT}.log")


def read_config(file: str):
    with open(file, 'r') as the_yaml:
        yaml_config = yaml.safe_load(the_yaml)
    return YamlConfig.init_from_yaml(yaml_config)


def copy_file(path: str, target: str):
    file = os.path.basename(os.path.normpath(path))
    filename, file_extension = os.path.splitext(file)
    if file_extension[1:] in config.includes:
        target_dir = os.path.dirname(target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        if os.path.exists(target):
            target_path, target_file = os.path.split(os.path.abspath(target))
            target = os.path.join(target_path, f"{os.path.basename(os.path.dirname(os.path.abspath(path)))} - {target_file}")
        log.debug(f"  > copying file {path} to {target}")
        shutil.copy2(path, target)


def import_documents(import_path: str, target_dir: str = None):
    log.debug(f" ----- Directory: {import_path} -----")
    base_path, directory_name = os.path.split(os.path.normpath(import_path))
    if import_config.excludes and directory_name in import_config.excludes:
        log.debug(f"  ! EXCLUDE {import_path}")
        return
    if import_config.flatten and directory_name in import_config.flatten:
        target_dir = os.path.join(config.target, import_config.targetdir, os.path.basename(import_path))
    if import_config.pullup and directory_name in import_config.pullup:
        target_dir = base_path
    for path in [f.path for f in os.scandir(import_path)]:
        if os.path.isdir(path):
            import_documents(path, target_dir)
        elif os.path.isfile(path):
            target_file = os.path.join(config.target, import_config.targetdir, path[len(import_dir) + 1:])
            if target_dir:
                target_file = os.path.join(target_dir, os.path.basename(os.path.normpath(path)))
            copy_file(path, target_file)


def prepare_target():
    if os.path.isdir(config.target):
        try:
            for act_path in [f.path for f in os.scandir(config.target)]:
                if os.path.isfile(act_path) or os.path.islink(act_path):
                    os.unlink(act_path)
                elif os.path.isdir(act_path):
                    shutil.rmtree(act_path)
        except Exception as e:
            log.error(f"Could not delete {act_path}. Reason: {e}")
    elif not os.path.exists(config.target):
        os.makedirs(config.target)


if __name__ == '__main__':
    config = read_config(FILEINPUT)
    prepare_target()
    for import_config in config.imports:
        import_dir = os.path.join(config.root, import_config.dir)
        log.debug(f"Import: {import_dir}")
        import_documents(import_dir)
