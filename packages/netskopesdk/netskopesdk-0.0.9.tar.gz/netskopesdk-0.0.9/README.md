# Netskope SDK

Neskope SDK is Python library for dealing with API's to download the Netskope events. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install NetskopeSDK.

```bash
pip install netskopesdk
```

## Usage

```python
from netskope.api.iterator.netskope_iterator import NetskopeIterator
from netskope.api.iterator.const import Const
from requests.exceptions import RequestException
import time

# Construct the params dict to pass the authentication details 
params = {
        Const.NSKP_TOKEN : "<REST-API-TOKEN",
        Const.NSKP_TENANT_HOSTNAME : "<HOSTNAME>",
        Const.NSKP_EVENT_TYPE : "<EVENT-TYPE>",
        Const.NSKP_ITERATOR_NAME : "<ITERATOR-NAME>"
    }

# Create an Iterator
iterator = NetskopeIterator(params)

# To consume the data form the beginning , start the iterator with head()
response = iterator.head()

# To consume the data form the latest timestamp , start the iterator with tail()
response = iterator.tail()

# To consume the data form a specific timestamp , start the iterator with timestmap()
response = iterator.download(<epoc-timestamp>)


# To stream the data use the next() iterator 
# Consume the message indefinitely in a loop and ingest the data to SIEM
    while True:
        response = (iterator.next())
        try:
            if response:
                data = response.json()
                if "result" in data and len(data["result"]) != 0:
                    
                    # Ingest the response data to SIEM .
                    # if( ingestion-fail ):
                       # User resend 
                       #response = iterator.resend()
                else:
                    print("No response received from the iterator")
                    # Sleep for desired time and recommended 5 sec 
                    # time.sleep(5)
        except Exception as e:
            raise RequestException(e)

```