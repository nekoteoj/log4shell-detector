import argparse
import json
import os
from log4shell_scanner.dep import src, jar
from log4shell_scanner.log import log_detect
from log4shell_scanner.exploit import exploiter

def parse_arguments():
    parser = argparse.ArgumentParser(description="Log4Shell Scanner")

    subparsers = parser.add_subparsers(dest="mode")

    src_parser = subparsers.add_parser("src");
    src_parser.add_argument("--path", type=str, help="Path to project directory")

    jar_parser = subparsers.add_parser("jar")
    jar_parser.add_argument("--path", type=str, help="Path to jar file")

    log_parser = subparsers.add_parser("log")
    log_parser.add_argument("--path", type=str, help="Path to log file")

    exploit_parser = subparsers.add_parser("exploit")
    exploit_parser.add_argument("--target-payload", type=str, help="Exploit Location (header, query, json, form)")
    exploit_parser.add_argument("--target-key", type=str, help="Key to exploit")
    exploit_parser.add_argument("--url", type=str, help="Request url")
    exploit_parser.add_argument("--headers", type=str, help="Json encoded request header", default="{}")
    exploit_parser.add_argument("--querys", type=str, help="Json encoded request params", default="{}")
    exploit_parser.add_argument("--datas", type=str, help="Json encoded request data payload", default="{}")
    exploit_parser.add_argument("--method", type=str, help="Http request method (get, post, put, patch, delete)")
    exploit_parser.add_argument("--payload-method", type=str, help="Data payload encoded type (form, json)", default="json")

    args = vars(parser.parse_args())

    return args

def main(args: dict):
    mode = args["mode"]
    match mode:
        case "src":
            if src.gradle.is_gradle_project(args["path"]):
                print("Detected gradle project.")
                src.gradle.detect(args["path"])
            elif src.maven.is_maven_project(args["path"]):
                print("Detected maven project.")
                src.maven.detect(args["path"])
            else:
                print("Unsupported project structure: Project directory is not gradle or maven project!")
        case "jar":
            if not os.path.exists("tmp/jar"):
                os.mkdir("tmp/jar")
            jar.detect(args["path"], "tmp/jar")
        case "log":
            log_detect.scan_log(args["path"])
        case "exploit":
            headers = json.loads(args["headers"])
            querys = json.loads(args["querys"])
            datas = json.loads(args["datas"])

            request = exploiter.Request(
                args["url"],
                headers,
                querys,
                datas,
                args["method"],
                args["payload_method"]
            )

            exploiter.run_exploit(request, args["target_payload"], args["target_key"])
        case _:
            raise NotImplementedError

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
