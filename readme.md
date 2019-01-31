# Cloudera checks for icinga2
This repo contains icinga plugin scripts for checking Cloudera Manager and HDFS

## Requirements

This checks depends on the following python modules:
 * requests
 * argparse

## Usage

### check_cloudera_service_status.py

```
check_cloudera_service_status.py [-h] -H HOST [-P API_PORT] -u API_USER -p API_PASS -v API_V -c CLUSTER -s SERVICE [-k VERIFY_SSL]

arguments:
  -h, --help show this help message and exit
  -H HOST, --host HOST
  -P API_PORT, --port API_PORT
  -u API_USER, --user API_USER
  -p API_PASS, --pass API_PASS
  -v API_V, --api_version API_V
  -c CLUSTER, --cluster CLUSTER
  -s SERVICE, --service SERVICE
  -k VERIFY_SSL, --verify_ssl VERIFY_SSL

## Examples

# Check YARN
./check_cloudera_service_status -H cloudera.test.example -u super_user -p super_password -v v18 -s yarn -c My_cluster
OK - yarn is in healthy state

# Check HDFS
./check_cloudera_service_status -H cloudera.test.example -u super_user -p super_password -v v18 -s hdfs -c My_cluster
Critical - there are several problems with service hdfs
hdfs_ha_namenode_health: bad
```

### check_cloudera_hdfs_files.py
```
check_cloudera_hdfs_files.py [-h] -H HOST [-P PORT] -w WARN -c CRIT [-m MAX_FILES]

arguments:
  -h, --help show this help message and exit
  -H HOST, --host HOST
  -P PORT, --port PORT
  -w WARN, --warn WARN
  -c CRIT, --crit CRIT
  -m MAX_FILES, --max MAX_FILES

## Examples

./check_cloudera_hdfs_files.py -H hadoop-namenode.example.com -w 80000000 -c 100000000 -m 200000000
Total count of files on HDFS is 64,773,022|FilesTotal=64773022;80000000;100000000;0;200000000
```

### check_cloudera_hdfs_space.py

```
check_cloudera_hdfs_space.py [-h] -H HOST [-P PORT] -d DISK -w WARN -c CRIT

Check status of cloudera

arguments:
  -h, --help show this help message and exit
  -H HOST, --host HOST
  -P PORT, --port PORT
  -d DISK, --disk DISK
  -w WARN, --warn WARN
  -c CRIT, --crit CRIT

## Examples

./check_cloudera_hdfs_space.py -H hadoop-namenode.example.com -w 40 -c 50 -d DISK
DISK: Used 3.77 PB of 6.95 PB (54.23%)|USED=3861TB;2848;3559;0;7119
```
