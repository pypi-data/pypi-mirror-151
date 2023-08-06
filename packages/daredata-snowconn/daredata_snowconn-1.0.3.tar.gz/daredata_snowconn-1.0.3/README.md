# SnowConn

This repository is a wrapper around the [snowflake SQLAlchemy](https://docs.snowflake.net/manuals/user-guide/sqlalchemy.html)
library. It manages the creation of connections and provides a few convenience functions that should be good enough
to cover most use cases yet be flexible enough to allow additional wrappers to be written around to serve more specific
use cases for different teams. 

## Installation

To install latest version released to pypi with pip:

```bash
pip install daredata_snowconn
```

To install the latest version directly from the repo:

```bash
pip install 'git+ssh://git@github.com/DareData/snowconn.git@master#egg=snowconn'
```

## Connection

Everything is implemented in a single `SnowConn` class. To import it is always the same:

```py
from snowconn import SnowConn
```

### (1) Connection using your own personal creds

Set the environment variables:

* SF_USERNAME - SnowFlake username.
* SF_PASSWORD - SnowFlake password.
* SF_ROLE - the role you want to use.
* SF_ACCOUNT - SnowFlake [account identifier](https://docs.snowflake.com/en/user-guide/admin-account-identifier.html), has the format `<organization_name>-<account_name>`.

Then simply do:

```py
conn = SnowConn.connect()
```
That's it you are connected! You can connect to a specific schema/database using another role or particular computing warehouse with the following:

```py
conn = SnowConn.connect('db_prod', 'public', role=my_role, warehouse=my_warehouse)
```

## API

Now that you're connected, there are a few low-level functions that you can use to programatically interact with
the snowflake tables that you have access to.

### execute_simple

The exc_simple function is used for when you have a single statement to execute and the result set can fit into memory. It
takes a single argument which a string of the SQL statement that you with to execute.

### execute_string

If you have multiple sql statements in a single string that you want to execute or the resultset is larger than
will fit into memory, this is the function that you want to use. It returns a list of cursors that are a result
of each of the statements that are contained in the string. See [here](https://docs.snowflake.net/manuals/user-guide/python-connector-api.html#execute_string) for the full documentation.

### execute_file

If you have the contents of an sql file that you want to execute, you can use this function. For example:
This also returns a list of cursors the same as `execute_string` does. In fact, this function is nothing more than a very
simple wrapper around `execute_string`.

### read_df

Use this function to read the results of a query into a dataframe. Note that pandas is NOT a dependency of this repo so
if you want to use it you must satisfy this dependency yourself.

It takes one sql string as an argument and returns a dataframe.

### write_df

Use this to write a dataframe to Snowflake. This is a very thin wrapper around the pandas [DataFrame.to_sql()](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html) function.

Unfortunately, it doesn't play nice with dictionaries and arrays so the use cases are quite limited. Hopefully
we will improve upon this in the future.

### get_current_role

Returns the current role.

### close

Use this to cleanly close all connections that have ever been associated with this instance of SnowConn. If you don't
use this your process will hang for a while without saying anything before it actually exits.

## Accessing the connection objects directly

These functions are mostly wrappers around 2 connection libraries:

- [The snowflake python connector](https://docs.snowflake.net/manuals/user-guide/python-connector-api.html)
- [The snowflake SQLAlchemy library](https://docs.snowflake.net/manuals/user-guide/sqlalchemy.html)

Should you need to use either of these yourself, you can ask for the connections yourself with the following
functions:

### get_raw_connection

This will return the instance of a snowflake connector which is documented [here](https://docs.snowflake.net/manuals/user-guide/python-connector-api.html#connect). It is a good choice if you have very simple needs and for some reason none
of the functions in the rest of this repo are serving your needs.

### get_alchemy_engine

This is the result of [create_engine()](https://docs.snowflake.net/manuals/user-guide/sqlalchemy.html#connection-parameters)
which was called during `connect()` or `credsman_connect()`. It does not represent an active connection to the database
but rather acts as a factory for connections.

This is useful for using the most commonly abstracted things in other libraries such as dashboards, pandas, etc. 
However, like SQLAlchemy in general, despite being very widely supported and feature-complete, it is not the simplest 
API so it should probably not be your first choice unless you know exactly that you need it.

### get_connection

This returns the result of the creating the sqlalchemy engine and then calling `connect()` on it. Unlike the result
of `get_alchemy_engine` this represents an active connection to Snowflake and this has a session associated with it.

You can see the object documentation [here](https://docs.snowflake.net/manuals/user-guide/sqlalchemy.html#parameters-and-behavior)
