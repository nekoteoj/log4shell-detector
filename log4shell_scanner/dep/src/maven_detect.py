import os
import re
import subprocess
from shutil import which
from log4shell_scanner.util.version import is_vulnerable_version

def is_maven_project(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Project directory {path} not found!")
    patterns = ["pom.xml"]
    for file in os.listdir(path):
        for pattern in patterns:
            if file == pattern:
                return True
    return False

def find_maven_executable(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Project directory {path} not found!")
    pattern = ""
    match os.name:
        case "posix":
            pattern = "mvnw"
        case "nt":
            pattern = "mvnw.cmd"
    for file in os.listdir(path):
        if file == pattern:
            return os.path.abspath(os.path.join(path, pattern))
    exe = which("mvn")
    if exe is not None:
        return exe
    exe = which("mvn.cmd")
    if exe is not None:
        return exe
    return ""

def detect(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Project directory {path} not found!")
    maven_path = find_maven_executable(path)
    if len(maven_path) == 0:
        print("Error: no maven executable found!")
    print(f"Found maven at {maven_path} .")

    p = subprocess.run([maven_path, "dependency:tree"], capture_output=True, cwd=path)
    output = p.stdout.decode()
    safe = True
    for line in output.split("\n"):
        line = line.lower()
        if "log4j" in line:
            print(f"Found Log4j at dependency line: {line}")
            candidates = re.findall(r"[0-9]+\.[0-9]+\.[0-9]+", line)
            for candidate in candidates:
                if is_vulnerable_version(candidate):
                    print(f"Found vulnerable Log4 version: {candidate}!")
                    safe = False
                else:
                    print(f"Found safe Log4j version: {candidate}!")
    if safe:
        print("You application is safe! No Log4Shell vulnerability detected in the provided project.")
