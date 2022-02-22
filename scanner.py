import argparse
import os
from log4shell_scanner.dep import jar
from log4shell_scanner.log import log_detect

def parse_arguments():
    parser = argparse.ArgumentParser(description="Log4Shell Scanner")

    subparsers = parser.add_subparsers(dest="mode")

    jar_parser = subparsers.add_parser("jar")
    jar_parser.add_argument("--path", type=str, help="Path to jar file")

    log_parser = subparsers.add_parser("log")
    log_parser.add_argument("--path", type=str, help="Path to log file")

    args = vars(parser.parse_args())

    return args

def main(args: dict):
    mode = args["mode"]
    match mode:
        case "jar":
            if not os.path.exists("tmp/jar"):
                os.mkdir("tmp/jar")
            jar.detect(args["path"], "tmp/jar")
        case "log":
            log_detect.scan_log(args["path"])
        case _:
            raise NotImplementedError

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
