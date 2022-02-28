# Log4Shell Scanner

![Alt text](/imgs/banner.png?raw=true "Project Banner")

Log4Shell Scanner is a tool for checking Log4Shell vulnerability in Java-based web application. It provides these functionality
- Dependency scanner for Gradle and Maven project
- Dependency scanner for JAR artifact
- Exploit evidence scanner for log files
- Exploit simulation using proof-of-concept code

## Requirements

- Python 3.10 or greater

## Dependencies

To install dependencies run

```sh
pip install -r requirements.txt
```

## Running the tool

The main executable is the file `scanner.py`. The desired functionality is selected through command-line arguments.

### Maven/Gradle project scanner

This tool can scan your project dependency graph at all depths to check if the project use vulnerable Log4j version.

To scan, run

```sh
python scanner.py src --path path-to-project
```

### JAR Artifact scanner

This tool can scan dependencies in the desired JAR file to check if the vulnaerable Log4j version is used.

To scan, run

```sh
python scanner.py jar --path path-to-project
```

### Log file scanner

This tool can scan evidence for attacking attempt in the log file. It parse any upper/lower Log4j's lookup in the file. Then it match the content in the file with our template lists. It will report vulnerability when there is at least one match in the log file.

To scan, run

```sh
python scanner.py log --path path-to-file
```

### Exploit simulation

This tool also provide proof-of-concept attack for checking if interested application is vulnerable to Log4Shell. This functionality requires 2 more tools which provided in the repository, including

1. **LDAP server**: we provided a ldap server for providing Java class file location. This server will run at port 1389 and will serve the Java class with query `ldap://localhost:1389/uid=exploit,ou=people,dc=example,dc=com`.

2. **Java class server**: we provided a static file server for serving safe java class file used to the simulation. The server will run at port 5000 and will server the Java class file at `http://localhost:5000/SafeApp.class`.

To run,

1. Start the LDAP server
    ```sh
    python ldap_server.py
    ```
2. Start the Java class server
    ```sh
    python class_server/server.py
    ```
3. Run the tool with
    ```sh
    python scanner.py exploit \
    --target-payload=exploit-location \
    --target-key=key-to-exploit \
    --url=target-url \
    --headers={"header1": "value1"} \ # Optional
    --querys={"query1": "value1"} \ # Optional
    --datas={"datas1": "value1"} \ # Optional
    --method=http-method \
    --payload-method=form-or-json-encoded # Optional
    ```
    For more information about each argument, please run `python scanner.py exploit --help`.

## Contributors

- Pisit Wajanasara (nekoteoj)
