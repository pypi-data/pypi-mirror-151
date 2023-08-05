# download-manager

Download Manager is a single python tool dedicated to help to download products from LTA and AIP.

## Download manager features

The tool has been implemented with the objective to implements the following features:

- Manage download in a configurable local folder,
- Manage partial downloads and recovery downloads,
- Manage parallelized downloads
- Manage bulk download
- Management of connections error/retry
- Monitoring of downloads (bandwidth/progress) and errors
- Run in command line (GUI is a nice to have)
- Support of multiple sources
- Manage checksum validation of downloads
- Local storage management (identification of incomplete downloads to be resume, evictions...)

- Manage/anticipate quota limitation:
    - bandwidth limitation
    - parallel transfers number
    - transfer volume per time ..
- Download list issued from an OData filter
- Manage OData endpoint notifications/action when new product matching filter is up to allow performing routine
  downloads.

## Install the download manager

Installing download-manager with execute the following in a terminal:

```
pip install download-manager
```

## Options

| Option                   |  Type   |                                                                                                             Explanation |                                                                Example |
|--------------------------|:-------:|------------------------------------------------------------------------------------------------------------------------:|-----------------------------------------------------------------------:|
| -s, --service            |  TEXT   |                                                                                    Service to requests data  [required] |                      download_manager --service odata://my_service.com |
| -f, --filters            |  TEXT   |                                     Filter to apply to requests products by default only online products are requested. | download_manager --service odata://my_service.com -f 'filter to apply' |
| -O, --order              |  TEXT   |                                                                                               Sort query (ASC or DESC). |               download_manager --service odata://my_service.com -O ASC |
| -u, --username           |  TEXT   |                                                                                            Service connection username. |              download_manager --service odata://my_service.com -u user |
| -p, --password           |  TEXT   |                                                                                            Service connection password. |               download_manager --service odata://my_service.com -p pwd |
| -P, --process_number     | INTEGER |                                                                        Number of parallel download threads (default:2). |                download_manager --service odata://my_service.com -P 16 |
| -l, --limit              | INTEGER |                                                                        Limit the number matching products (default: 10) |               download_manager --service odata://my_service.com -l 100 |
| -o, --output             |  TEXT   |                                                                            The directory to store the downloaded files. | download_manager --service odata://my_service.com -o /path/to/products |
| -q, --quiet              | BOOLEAN |                                                                                  Silent mode: only errors are reported. |                   download_manager --service odata://my_service.com -q |
| -c, --chunk-size         | INTEGER |                                                                       The size of downloaded chunks (default: 4194304). |          download_manager --service odata://my_service.com -c 16777216 |
| -v, --verify             | BOOLEAN |                                                                                         Check file integrity by hashes. |                   download_manager --service odata://my_service.com -v |
| -r, --resume             | BOOLEAN |                                                                         Resume downloading a partially downloaded file. |                   download_manager --service odata://my_service.com -r |
| -d, --database           |  TEXT   | Folder to store the database if not present the database will be in a folder /.download_manager in the home directory.. |  download_manager --service odata://my_service.com -d /path/to/your/db |
| -S, --storage_limit_size | INTEGER |                                                                                       The size max of file to download. |          download_manager --service odata://my_service.com -S 20000000 |
| -C, --continuous         | BOOLEAN |                                                       When present the download keep going download package by package. |                   download_manager --service odata://my_service.com -C |
| -b, --bulk               |  TEXT   |                                                            Path to a csv file containing name of products to downloads. | download_manager --service odata://my_service.com --bulk <Path_to_csv> |
| --help                   |         |                                                                                             Show this message and exit. |                                                download_manager --help |

## Getting started

Download one product, with one thread:

```
download_manager --service odata://service.com/ -P 1 -u user -p password -l 1
```

Download 10 products:

```
download_manager --service odata://service.com/ -u user -p password -l 10
```

Use the silent option:

```
download_manager --service odata://service.com/ -u user -p password --quiet
```

Use filter to download specific products:

```
download_manager --service odata://service.com/ -u user -p password -f "Online eq true and startswith(Name,'S1')"
```

Use the resume option:

```
download_manager --service odata://service.com/ -u user -p password --db_folder 'database_folder' --resume

```

Use the storage management option:

```
download_manager --service odata://service.com/ -u user -p password -f "Online eq true and startswith(Name,'S2')" -l 25 -S 278209392 -o tests -db resources
```

Use python code:

```python
from download_manager.download_manager import DownloadManager
from requests.auth import HTTPBasicAuth

service = 'https://odata.service.com'
auth=HTTPBasicAuth("user", "pwd")
dm = DownloadManager(service=service, auth=auth)
dm.start()

nodes = dm.find_nodes(filter="startswith(Name, 'S2B')")

for node in nodes:
    if node['Attributes']['cloudCover'].value == 0:
        dm.submit(node)

dm.join()
dm.stop()
```

## Limitation

For now only odata implementation is available, quota still not supported.

The error management is implemented but cannot be parametrized in command line.

Offline product are not yet supported.