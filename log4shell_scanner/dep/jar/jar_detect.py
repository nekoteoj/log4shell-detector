from operator import is_
import os
import re

from zipfile import ZipFile
from log4shell_scanner.util import is_vulnerable_version

def get_dir_jar(path: str, target_dir: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"provided path does not exists ({path}).")
    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"provided target directory does not exists ({path}).")
    with ZipFile(path, "r") as z:
        return z.filelist

def detect_jar(path: str, target_dir: str):
    jar_infos = get_dir_jar(path, target_dir)
    candidates = [info.filename for info in jar_infos if "log4j" in info.filename.lower()]
    candidate_vers = []
    for candidate in candidates:
        candidate_vers += re.findall(r"[0-9]+.[0-9]+.[0-9]+", candidate)
    vulnerable = False
    for i, ver in enumerate(candidate_vers):
        if is_vulnerable_version(ver):
            vulnerable = True
            print(f"Found vulnerable dependency at location: {candidates[i]}")
    if not vulnerable:
        print(f"You application is safe! No Log4Shell vulnerability detected in the provided JAR file.")
