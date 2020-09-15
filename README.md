# Python-Windscribe

## Usage

### Login

Login by explicitly providing your username & password or export environment
variables `WINDSCRIBE_USER` and `WINDSCRIBE_PW`.

```python
import windscribe

windscribe.login('<user>', '<password>')
```

### Get locations

Returns a list of `WindscribeLocation` instances; each of which have the
following attributes: `name`, `abbrev`, `city`, and `label`.

```python
location_list = windscribe.locations()
```

### Connect

Connects to the best server by default:

```python
windscribe.connect()
```

Connect to a random location:

```python
windscribe.connect(rand=True)
```

Connect to a specific location using a string:

**NOTE:** *You can use a given location's `name`, `abbrev`, `city`, or `label`.*

```python
windscribe.connect('BBQ')
```

Connect by passing in a `WindscribeLocation` instance:

```python
def get_barbecue():

    for location in windscribe.locations():

        if location.label == 'BBQ': return location

bbq = get_barbecue()

windscribe.connect(bbq)
```

### Account Details

```python
windscribe.account()
```

### Logout

```python
windscribe.logout()
```