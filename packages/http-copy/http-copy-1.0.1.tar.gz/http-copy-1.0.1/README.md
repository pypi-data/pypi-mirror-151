# http-copy

Install the tool via the setup tools:

    python setup.py install

or pypi:

    pip install http-copy

Simply use the `http-copy` command to copy a local file or directory to the remote url through http:

    usage: Upload a file or all files in a directory recursively through HTTP. Supports ignore-like file.
        [-h] [--params PARAMS] [--ignore-file IGNORE_FILE] [--disable-tqdm] local_path_or_dir remote_url

    positional arguments:
    local_path_or_dir
    remote_url

    optional arguments:
    -h, --help            show this help message and exit
    --params PARAMS       Additional URL params
    --ignore-file IGNORE_FILE
    --disable-tqdm