#!/usr/bin/env python

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import sys
import os
import argparse

def build_parser():
    parser = argparse.ArgumentParser(description='Check status of cloudera')
    parser.add_argument('-H', '--host',        required=True,  dest='host')
    parser.add_argument('-P', '--port',        required=False, dest='api_port', default=443)
    parser.add_argument('-u', '--user',        required=True,  dest='api_user')
    parser.add_argument('-p', '--pass',        required=True,  dest='api_pass')
    parser.add_argument('-v', '--api_version', required=True,  dest='api_v')
    parser.add_argument('-c', '--cluster',     required=True,  dest='cluster')
    parser.add_argument('-s', '--service',     required=True,  dest='service')
    parser.add_argument('-k', '--verify_ssl',  required=False, dest='verify_ssl', type=str2bool, default=True)
    return parser


def str2bool(value):
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    parser  = build_parser()
    args    = parser.parse_args()

    host       = args.host
    api_port   = args.api_port
    api_user   = args.api_user
    api_pass   = args.api_pass
    api_v      = args.api_v
    cluster    = args.cluster
    service    = args.service
    verify_ssl = args.verify_ssl

    api_url    = 'https://%s:%s/api/%s/clusters/%s/services/%s/' % (host, api_port, api_v, cluster, service)

    try:
        resp = requests.get(api_url, auth=(api_user, api_pass), verify=verify_ssl)
    except Exception as e:
        print('Could not connect to Cloudera API:\n' + str(e))
        exit(2)

    if resp.status_code != 200:
        print('Cloudera API returns non-ok status code: %d - %s' % (resp.status_code, resp.json()['message']))
        exit(2)

    overall_status = resp.json()['healthSummary']

    if overall_status.lower() == 'good':
        print("OK - %s is in healthy state" % service)
        sys.exit(0)

    sub_status = map(
        lambda x: "%s: %s" % (x['name'].lower(), x['summary'].lower()),
        filter(lambda x: x['summary'].lower() == 'concerning' or x['summary'].lower() == 'bad', resp.json()['healthChecks']))

    if overall_status.lower() == 'concerning':
        print("Warning - there are several problems with service %s\n%s" % (service, '\n'.join(sub_status)))
        sys.exit(1)

    print("Critical - there are several problems with service %s\n%s" % (service, '\n'.join(sub_status)))
    sys.exit(2)

if __name__ == "__main__":
    main()
    sys.exit(0)
