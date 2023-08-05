# tmp_connection_psql

Its a little package to create a temporary psql database and qet a connection on it.

## Install

Available as a package on pypi.
```shell
pip install tmp-connection-psql
```

First install all dependencies
```bash
$ poetry install
Installing dependencies from lock file

No dependencies to install or update

Installing the current project: tmp_connection_psql (1.0.1)
```

## Usage

tmp_connection is a function who yield a connection, to use it you need to make your code in a with
statement.

```python
with tmp_connection("dummypassword") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    record = cursor.fetchall()
print(record)
```
Give you an error because the database is empty.
It doesn't known the table 'people'.

You can create your table and fill it after creating the database with `tmp_connection("password")`
```python
with tmp_connection("dummypassword") as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE people (id serial NOT NULL PRIMARY KEY, first_name TEXT NOT NULL, age int NOT NULL, zipcode int NOT NULL, city TEXT NOT NULL)")
    cursor.execute("""INSERT INTO people VALUES
("Ulysse", 25, 75019, "Paris"), ("Jacques", 84, 42820, "Ambierle")""")
    conn.commit()
```
and launch request on it
```python
cursor.execute("SELECT * FROM people")
    record = cursor.fetchall()
print(record)
```
it will give you.
```python
[
    ("id": 1, "first_name": "Ulysse", "age": 25, "zipcode": 75019, "city": "Paris"),
    ("id": 2, "first_name": "Jacques", "age": 84, "zipcode": 42820, "city": "Ambierle"),
]
```

Or You can give an sql file to the function `tmp_connection("password", "./sql_file.sql")`
and it will create the table and fill it before giving you access to the connection.

Example:
```python
with tmp_connection("dummypassword", "./sql_file.sql") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    record = cursor.fetchall()
print(record)
```
it will give you
```python
[
    ("id": 1, "first_name": "Ulysse", "age": 25, "zipcode": 75019, "city": "Paris"),
    ("id": 2, "first_name": "Jacques", "age": 84, "zipcode": 42820, "city": "Ambierle"),
]
```
with the file './sql_file.sql' .
```SQL
-- Create table
CREATE TABLE people (id serial NOT NULL PRIMARY KEY, first_name TEXT NOT NULL, age int NOT NULL, zipcode int NOT NULL, city TEXT NOT NULL);
-- Insert into people
INSERT INTO people VALUES
("Ulysse", 25, 75019, "Paris"); -- id = 1
("Jacques", 84, 42820, "Ambierle"); -- id = 2
```

## Changelog, License

- [Changelog](CHANGELOG.md)
- [EUPL European Union Public License v. 1.2](LICENSE.md)

## Credits

- Author : CHOSSON Ulysse
- Maintainer : CHOSSON Ulysse
- Email : <ulysse.chosson@obspm.fr>
- Contributors :
    - MARTIN Pierre-Yves <pierre-yves.martin@obspm.fr>
