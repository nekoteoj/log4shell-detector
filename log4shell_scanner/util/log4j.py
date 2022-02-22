# Pattern and parsing guide from https://runpanther.io/blog/panthers-guide-to-log4j-exploitation-prevention-and-detection/

def lookup_parser(s: str):
    if len(s) == 0:
        return ""
    i = 0
    query = s[2: len(s) - 1]
    while i < len(query):
        start_loc = query.find("${", i)
        if start_loc == -1:
            break
        j = start_loc + 2
        cnt = 1
        while j < len(query):
            if query[j] == "}":
                cnt -= 1
                if cnt == 0:
                    break
            elif query[j] == "{" and query[j - 1] == "$":
                cnt += 1
            j += 1
        if cnt != 0:
            i = start_loc + 2
            continue
        parsed = lookup_parser(query[start_loc: j + 1])
        query = query[:start_loc] + parsed + query[j + 1:]
        i += len(parsed)
    tokens = query.split(":")
    if len(tokens) <= 1:
        return query
    data = ":".join(tokens[1:])
    if tokens[0].lower() == "upper":
        return data.lower()
    if tokens[0].lower() == "lower":
        return data.lower()
    return "${" + query + "}"


def get_patterns():
    return [
        "jndi:ldap:/",
        "jndi:rmi:/:",
        "jndi:ldaps:/",
        "jndi:dns:/",
        "jndi:nis:/",
        "jndi:nds:/",
        "jndi:corba:/",
        "jndi:iiop:/",
        "jndi:${",
        "${jndi:",
        "${lower:",
        "${upper:",
        "${env:",
        "${sys:",
        "${java:",
        "${date:",
        "${::-j",
    ]
