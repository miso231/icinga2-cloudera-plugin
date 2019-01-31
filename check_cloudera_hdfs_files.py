#! /usr/bin/env python3

import argparse
import requests
import sys
import os
from decimal import Decimal


def build_parser():
    parser = argparse.ArgumentParser(description='Check status of cloudera')
    parser.add_argument('-H', '--host', type=str, required=True,  dest='host')
    parser.add_argument('-P', '--port', type=int, required=False, dest='port', default=50070)
    parser.add_argument('-w', '--warn', type=int, required=True,  dest='warn')
    parser.add_argument('-c', '--crit', type=int, required=True,  dest='crit')
    parser.add_argument('-m', '--max',  type=int, required=False, dest='max_files', default=140000000)
    return parser


def main():
    parser    = build_parser()
    args      = parser.parse_args()

    host      = args.host
    port      = args.port
    warn      = args.warn
    crit      = args.crit
    max_files = args.max_files

    api_url = "http://{0}:{1}/jmx".format(host, port)
    headers = { "content-type": "application/json", "Accept": "application/json" }

    try:
        resp = requests.get(api_url, headers=(headers))
    except Exception as e:
        print('Could not connect to namenode: ' + str(e))
        exit(2)

    if resp.status_code != 200:
        print('Could not connect to namenode, status code: ' + str(resp.status_code))
        exit(2)

    data = ""
    for item in resp.json()['beans']:
        if item["name"] == "Hadoop:service=NameNode,name=FSNamesystem":
            data = int(item["FilesTotal"])
            break

    if data > crit:
        print("Too many files on HDFS - {0:,}|FilesTotal={0};{1};{2};0;{3}".format(data, warn, crit, max_files))
        exit(2)
    elif data > warn:
        print("Too many files on HDFS - {0:,}|FilesTotal={0};{1};{2};0;{3}".format(data, warn, crit, max_files))
        exit(1)
    print("Total count of files on HDFS is {0:,}|FilesTotal={0};{1};{2};0;{3}".format(data, warn, crit, max_files))
    exit(0)


if __name__ == "__main__":
    main()
    sys.exit(0)
