lz4 container
===============

overview
========
This tool will use lz4 to compress/decompress files.


how to run
==========
Usage: 
```
lz4 [options] [file]
```

Examples:
```
  lz4 -c dir_name.lz4r dir_name  
  lz4 -x dir_name.lz4r          
  lz4 -c file_name.lz4r file_name
  lz4 -x file_name.lz4r
```

Options:
```
  -h, --help       show this help message and exit
  -c, --create     create a new archive
  -x, --extract    extract files from an archive
```
