# Setting up An Local Development Environment

## Requirements

### Software

- Python

### Python Libs

- MySQLdb (Not Default)
- pytz (Not Default)
- urllib
- json
- ast
- datetime
- glob
- sys
- os

### MySQL Server to test on (see below for XAMPP guidance)

## Installation Steps

1. Set up XAMPP
[Download the installer here](https://www.apachefriends.org/download.html)

[Setup walkthrough](https://www.ionos.ca/digitalguide/server/tools/xampp-tutorial-create-your-own-local-test-server/)

[Another better example](https://premium.wpmudev.org/blog/setting-up-xampp/)

1. XAMPP uses MariaDB instead of MySQL, recommend changing this to MySQL otherwise there may be difficulty in implmenting changes

[Changing MariaDB to MySql in XAMPP](https://stackoverflow.com/questions/39654428/how-can-i-change-mariadb-to-mysql-in-xampp)

[MySQL 5.7 in XAMPP for Windows](https://ourcodeworld.com/articles/read/1215/how-to-use-mysql-5-7-instead-of-mariadb-in-xampp-for-windows)

3. Create MySQL Database for stats

Start Apache / MySQL
Via XAMPP - MySQL - Admin
Create Database
--Database MERCDemo

4. Create new Database user (phpMyAdmin)
(to match calls in Python & PHP code)

```python
..
$username = "testadm";
$password = "test_all_the_things";
```

5. Initialize Tables

Run `MERCDemo_createtabs.py` to generate tables

6. Example - parse data provided

Adjust dates dstart and dend in `MERCDemo_DB_auto_open.py`
Run `MERCDemo_DB_auto_open.py`

>Note: this will take a significant amount of time currently, suggest sticking to a single day at a time.













