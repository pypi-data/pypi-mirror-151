# dropbox-updater

Module to update python script using dropbox api

## Installation

```
pip install dropbox-updater
```

## Example

### Uploading

```
>>> from dropbox_updater.updater import upload
>>> config = [
...     {
...         'name': 'my-project',
...         'token': DROPBOX_ACCESS_TOKEN,
...         'dropbox_path': '/my-project.tar.bz2',
...         'file_path': 'dist/my-project.tar.bz2',
...         'extract_dir': '.',
...     },
... ]
>>> upload(config)
05/12/2022 02:13:54 PM - INFO - Compressing to dist/my-project.tar.bz2...
05/12/2022 02:13:54 PM - INFO - my-project requires uploading.
05/12/2022 02:13:54 PM - INFO - Uploading to /my-project.tar.bz2...
05/12/2022 02:13:54 PM - INFO - Uploading (0/1)...
05/12/2022 02:13:57 PM - INFO - Uploading (1/1)...
```

### Checking for updates

```
>>> from dropbox_updater.updater import check_for_updates
>>> config = [
...     {
...         'name': 'my-project',
...         'token': DROPBOX_ACCESS_TOKEN,
...         'dropbox_path': '/my-project.tar.bz2',
...         'file_path': 'dist/my-project.tar.bz2',
...         'extract_dir': '.',
...     },
... ]
>>> check_for_updates(config, restart=False)
05/12/2022 02:22:38 PM - INFO - Checking for updates...
05/12/2022 02:22:39 PM - INFO - Already upto date.
```
