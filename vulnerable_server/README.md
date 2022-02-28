# Simple Log4Shell vulnerable server

This is a simple web server which use vulnerable Log4j version. It was written in Java programming language and use Javalin as the web framework.

## Dependencies

* Javalin 4.3.0
* Log4j 2.5.0
* Slf4j 1.8.0 beta 4


## Requirement

* Java 11 or greater

## Building project

For windows using PowerShell

```sh
.\mvnw.cmd assembly:assembly
```

For unix based system
```sh
./mvnw assembly:assembly
```

The compile artifact should be in `target/vulnerable_server-1.0-SNAPSHOT-jar-with-dependencies.jar`

## Running server

```
java -Dcom.sun.jndi.ldap.object.trustURLCodebase=true -jar vulnerable_server-1.0-SNAPSHOT-jar-with-dependencies.jar
```
