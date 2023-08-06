# UniCatDB API library

Python library for accessing API of the UniCatDB - Universal Catalog Database for biological findings.

> UniCatDB is a coherent yet flexible interdisciplinary storage solution for cataloging findings data of various research groups, focused mainly on green biology. Configurable by the researchers themselves, provides shared access enabling interoperability if desired, and is accessible by user-friendly interface on either desktop, laptop or tablet - both in the lab and on the go.

See www.unicatdb.org for more details and contact.

# Getting started

1) Install the library to your Python environment.

    Typically, for local Python on your desktop, run pip install command in shell:
    
    ```shell script
    pip install unicatdb
    ```
    
    For other environments, such as Jupiter notebook, see respective documentation for instructions on how to install pip packages.
    
    For example, in Jupiter notebook, paste this snippet the top (source: [here for details](https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/#How-to-use-Pip-from-the-Jupyter-Notebook)):
    
    ```python
    # Install a pip package in the current Jupyter kernel
    
    import sys
    !{sys.executable} -m pip install unicatdb
    ```

2) Login to the UniCatDB (https://app.unicatdb.org)
3) Obtain your API credentials (API key and Personal access token) - click on your profile in toolbar, then on *API Access* button
4) Use credentials in API client configuration, see usage examples bellow


# Structure

The core of the library is in module `unicatdb.opeapi_client` which consists of code generated via the modified
[OpenAPI Generator](https://openapi-generator.tech/) and the interface corresponds to the UniCatDB API specifications available at https://api.unicatdb.org

For more convenient access, wrappers are provided in `unicatdb.api` module - this is your entrypoint for most common tasks.


# Usage examples

## The "Hello world"

**What this does:** Get first ten findings from the database

```python
import unicatdb
from typing import List
from pprint import pprint

# %% Paste your API key and Personal access token from https://account.unicatdb.org/

configuration = unicatdb.Configuration(
    access_token='<PASTE YOUR API KEY TOKEN HERE>'
)

# %% Query some data
from unicatdb.openapi_client import UserScopedTenant, FindingArrayResponse
with unicatdb.Client(configuration) as client:

    # list my available workspaces (a.k.a tenants) ...
    my_workspaces: List[UserScopedTenant] = client.tenants.api_tenants_available_get()
    pprint(my_workspaces)

    # ... and if I have one, list some of it's finding
    if my_workspaces:
        selected_workspace = my_workspaces[0]

        findings: FindingArrayResponse = client.findings.api_findings_get(selected_workspace.id)
        pprint(findings)
```

## Advanced query example

**What this does:** Get only the *name*, *amount* and *dynamic data* of the top 10 findings sorted by *amount* greatest-first,
of which taxonomy's genus contains 'vulgare':


```python
import unicatdb
from typing import List
from pprint import pprint

# %% Paste your API key and Personal access token from https://app.unicatdb.org/

configuration = unicatdb.Configuration(
    access_token='<PASTE YOUR API KEY TOKEN HERE>'
)

# %% Query some data - e.g. apply filtering, sorting and paging during the API call to leave the heavy-lifting to the server

from unicatdb.openapi_client import UserScopedTenant, FindingArrayResponse, FindingFieldsQuery, PageQuery

with unicatdb.Client(configuration) as client:

    # list my available workspaces (a.k.a tenants) ...
    my_workspaces: List[UserScopedTenant] = client.tenants.api_tenants_available_get()
    pprint(my_workspaces)

    # ... and if I have one, list some of it's finding
    if my_workspaces:
        selected_workspace = my_workspaces[0]

        filter_expressions = {
            "taxonomyName.species": "like:vulgare"
        }
    
        fetch_only_fields = FindingFieldsQuery(findings="documentName,amount,dynamicData")
    
        findings: FindingArrayResponse = client.findings.api_findings_get(
            selected_workspace.id,
            sort="-amount",
            filter=filter_expressions,
            fields=fetch_only_fields,
            page=PageQuery(number=1,size=10)
        )
    
        pprint(findings)
```

## Uploading attachments with TUS protocol

Preferable method of uploading (large) files is to use UniCatDB [TUS protocol](https://tus.io/) endpoint.
The TUS protocol uses chunking and allows for resumable uploads.

This library includes wrapper for official Python TUS client [tuspy](https://pypi.org/project/tuspy/).
For advanced usage, please refer to [their documentation]().

### Simple TUS upload example

**What this does:** Upload a JPEG image named `my_image_attachment.jpg` to specified Finding.

```python
import unicatdb

# %% Paste your API key and Personal access token from https://account.unicatdb.org/

configuration = unicatdb.Configuration(
    access_token='<PASTE YOUR API KEY TOKEN HERE>'
)

# %% Upload a single file to a Finding

with unicatdb.Client(configuration) as client:

    # suppose we already have some Finding in a workspace
    finding_id = "<PASTE TARGET FINDING ID HERE>"
    workspace_id = "<PASTE TARGET WORKSPACE ID OF THE FINDING HERE>"

    # get prepared TUS protocol for uplading files
    tus_client = client.get_tus_client_for_finding(workspace_id, finding_id)

    # create uploader for our file, don't forget to provide required metadata
    uploader = tus_client.uploader(
        'path/to/my_image_attachment.jpg',
        metadata={
            "fileName": "my_image_attachment.jpg",
            "contentType": "image/jpeg"
        },
        chunk_size=unicatdb.Constants.DEFAULT_CHUNK_SIZE,   # set chunk size in Bytes (1MB is the default)
        log_func=lambda msg: print(msg)                     # optional - print the progress to console
    )

    # Uploads the entire file.
    # This uploads chunk by chunk.
    uploader.upload()
```

### Resumable TUS upload example
 
**What this does:** Upload a video file `very_large_video_file.mp4` to specified Finding with 
ability to resume uploading if it was interrupted.

```python
import unicatdb
from tusclient.storage import filestorage
from tusclient.fingerprint import fingerprint


# %% Paste your API key and Personal access token from https://account.unicatdb.org/

configuration = unicatdb.Configuration(
    access_token='<PASTE YOUR API KEY TOKEN HERE>'
)

# %% Upload a single file to a Finding, with resume capability

# To make upload resumable, first create file-based cache storage
tus_storage = filestorage.FileStorage('tus_resumable_temp.json')
tus_fingerprinter = fingerprint.Fingerprint()

with unicatdb.Client(configuration) as client:

    # suppose we already have some Finding in a workspace
    finding_id = "<PASTE TARGET FINDING ID HERE>"
    workspace_id = "<PASTE TARGET WORKSPACE ID OF THE FINDING HERE>"

    # get prepared TUS protocol for uplading files
    tus_client = client.get_tus_client_for_finding(workspace_id, finding_id)

    # create uploader for our file, don't forget to provide required metadata
    uploader = tus_client.uploader(
        'path/to/very_large_video_file.mp4',
        metadata={
            "fileName": "very_large_video_file.mp4",
            "contentType": "video/mp4"
        },
        chunk_size=unicatdb.Constants.DEFAULT_CHUNK_SIZE,   # set chunk size in Bytes (1MB is the default)
        log_func=lambda msg: print(msg),                     # optional - print the progress to console
        # enable resumability:
        store_url=True,
        url_storage=tus_storage,
        fingerprinter=tus_fingerprinter
    )

    # Uploads the entire file.
    # This uploads chunk by chunk.
    uploader.upload()

    # (Now try force-stopping the script during upload, then restart it. The upload should continue where it left off)

    # clear uploaded file from cache on success
    file_key = tus_fingerprinter.get_fingerprint(uploader.get_file_stream())
    tus_storage.remove_item(file_key)
    # (or simply remove the 'tus_resumable_temp.json' file)
```