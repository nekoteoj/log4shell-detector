import os

from log4shell_scanner.util import lookup_parser, get_patterns

def scan_log(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Cannot open log file at {path}.")
    with open(path, "r") as f:
        data = f.read()
        data = data.lower()
    patterns = get_patterns()
    found = False
    for pattern in patterns:
        idx = data.find(pattern)
        if idx != -1:
            print(f"Found vulnerability using pattern '{pattern}' at position {idx}.")
            found = True
    i = 0
    while i < len(data):
        start_idx = data.find("${", i)
        if start_idx == -1:
            break
        cnt = 1
        end_idx = start_idx + 2
        if end_idx > len(data):
            break
        while end_idx < len(data):
            if data[end_idx] == "{" and data[end_idx - 1] == "$":
                cnt += 1
            if data[end_idx] == "}":
                cnt -= 1
                if cnt == 0:
                    break
            end_idx += 1
        if cnt != 0:
            i += 2
            continue
        parsed = lookup_parser(data[start_idx: end_idx + 1])
        for pattern in patterns:
            idx = parsed.find(pattern)
            if idx != -1:
                print(f"Found vulnerability using pattern '{pattern}' after parsed {data[start_idx: end_idx + 1]} to {parsed} at position {start_idx}.")
                found = True
        i = end_idx + 1
        print(i)
    if not found:
        print("You application is safe! No Log4Shell vulnerability detected in the provided log file.")
