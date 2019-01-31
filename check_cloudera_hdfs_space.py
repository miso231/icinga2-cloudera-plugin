#! /usr/bin/env python

import requests
import argparse
import sys
import os
from decimal import Decimal

def build_parser():
    parser = argparse.ArgumentParser(description='Check status of cloudera')
    parser.add_argument('-H', '--host',  type=str,         required=True,  dest='host')
    parser.add_argument('-P', '--port',  type=int,         required=False, dest='port', default=50070)
    parser.add_argument('-d', '--disk',  type=str,         required=True,  dest='disk')
    parser.add_argument('-w', '--warn',  type=percent_int, required=True,  dest='warn')
    parser.add_argument('-c', '--crit',  type=percent_int, required=True,  dest='crit')
    return parser


def percent_int(value):
    try:
        value_int = int(value)
    except:
        raise argparse.ArgumentTypeError('Integer value expected from range (0,100)')
    if value_int < 0 or value_int > 100:
        raise argparse.ArgumentTypeError('Integer value expected from range (0,100)')
    return value_int


def main():
    parser  = build_parser()
    args    = parser.parse_args()

    host    = args.host
    port    = args.port
    disk    = args.disk
    warn    = args.warn
    crit    = args.crit

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
        if item["name"] == "Hadoop:service=NameNode,name=BlockStats":
            data = item["StorageTypeStats"]
            break

    disk_data = ""
    for item in data:
        if item["key"] == disk:
            disk_data = item
            break

    # Calculate capacity in PB, TB and percent
    dfs_capacity_pb      = float(disk_data['value']['capacityTotal']) / 1024.0 / 1024.0 / 1024.0 / 1024.0 / 1024.0
    dfs_capacity_used_pb = float(disk_data['value']['capacityUsed']) / 1024.0 / 1024.0 / 1024.0 / 1024.0 / 1024.0
    dfs_capacity_tb      = dfs_capacity_pb * 1024
    dfs_capacity_used_tb = dfs_capacity_used_pb * 1024

    dfs_capacity_used_warn_pb = dfs_capacity_pb * warn / 100
    dfs_capacity_used_crit_pb = dfs_capacity_pb * crit   / 100
    dfs_capacity_used_warn_tb = dfs_capacity_used_warn_pb * 1024
    dfs_capacity_used_crit_tb = dfs_capacity_used_crit_pb * 1024
    dfs_capacity_free_tb      = dfs_capacity_pb - dfs_capacity_used_pb

    dfs_capacity_used_percent = dfs_capacity_used_pb / dfs_capacity_pb * 100

    print("{0}: Used {1:.2f} PB of {2:.2f} PB ({3:.2f}%)|USED={4:.0f}TB;{5:.0f};{6:.0f};0;{7:.0f}".format(disk, dfs_capacity_used_pb, dfs_capacity_pb, dfs_capacity_used_percent, dfs_capacity_used_tb, dfs_capacity_used_warn_tb, dfs_capacity_used_crit_tb, dfs_capacity_tb))

    if dfs_capacity_used_percent > crit:
        exit(2)
    elif dfs_capacity_used_percent > warn:
        exit(1)
    else: exit(0)


if __name__ == "__main__":
    main()
    sys.exit(0)
