# Sky Api Client

This is the sky api python client library.

## Installation

```
pip install sky_api_client
```

## Examples

1. Initialize the client

```python
from sky_api_client import SkyApi

sky_api = SkyApi('subscription_key', 'access_token')
```

2. Get list of all constituent

```python
list = sky_api.constituent.list()
```

## Available methods

1. List all constituents

```
list = sky_api.constituent.list()
```

2. Get a specific constituent

```python
constituent = sky_api.constituent.get('constituent_id')
```

3. Create a new constituent

```python
new_constituent = sky_api.constituent.create({'first': '', 'last': ''})
```

4. Update an existing constituent

```python
updated_constituent = sky_api.constituent.update('constituent_id' ,{'first': '', 'last': ''})
```

5. Delete a constituent

```python
sky_api.constituent.delete('constituent_id')
```
