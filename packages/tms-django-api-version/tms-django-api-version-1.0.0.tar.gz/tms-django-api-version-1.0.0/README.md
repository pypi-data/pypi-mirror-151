# Django API Version

Simple api endpoint to display version from config

Create a `version.py` file containing the `VERSION` variable besides your `settings.py`

```python
VERSION='0.0.1'
#You can also use an environment variable with the following
import os
VERSION=os.getenv('MY_VERSION', 'unknown')
```

Then import the version in your `settings.py`

```python
from <project>.version import VERSION
```

And finally add the views in your urls

```python
path(
    "version/",
    version_views.VersionView.as_view(),
    name="version",
)
```

Then the version will be return on the corresponding endpoint.

