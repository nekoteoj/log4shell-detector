def is_vulnerable_version(version: str):
    tokens = version.split(".")
    v1 = 2
    v2 = 0
    v3 = 0
    if len(tokens) > 0:
        v1 = int(tokens[0])
    if len(tokens) > 1:
        v2 = int(tokens[1])
    if len(tokens) > 2:
        v3 = int(tokens[2])

    if v1 != 2:
        return False
    if v2 == 3:
        if v3 >= 2:
            return False
    if v2 == 12:
        if v3 >= 4:
            return False
    if v2 == 17:
        if v3 >= 1:
            return False
    if v2 >= 18:
        return False

    return True
