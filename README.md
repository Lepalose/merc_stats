

REQUIREMENTS:

Need to have Python installed
Python Libs used: MySQLdb, urllib, json, ast, datetime, pytz, glob, sys, os
I think these are all standard and may not require specific downloading.

A server to test on (see below for XAMPP guidance)


##########################################################
1. Set up XAMPP
https://www.apachefriends.org/download.html

Setup walkthrough: https://www.ionos.ca/digitalguide/server/tools/xampp-tutorial-create-your-own-local-test-server/
Better: https://premium.wpmudev.org/blog/setting-up-xampp/



##########################################################

2. XAMPP uses MariaDB instead of MySQL, recomment changing this to MySQL otherwise may be difficulty in implmenting changes

https://stackoverflow.com/questions/39654428/how-can-i-change-mariadb-to-mysql-in-xampp

https://ourcodeworld.com/articles/read/1215/how-to-use-mysql-5-7-instead-of-mariadb-in-xampp-for-windows



##########################################################

3. Create MySQL Database for stats

Start Apache / MySQL
Via XAMPP - MySQL - Admin
Create Database
--Database MERCDemo 



##########################################################

4. Create new Database user (phpMyAdmin)
(to match calls in Python & PHP code)
..
$username = "testadm";
$password = "test_all_the_things";   



##########################################################

5. Initialize Tables
Run "MERCDemo_createtabs.py" to generate tables



##########################################################

6. Example - parse data provided
Adjust dates dstart and dend in "MERCDemo_DB_auto_open.py"
Run "MERCDemo_DB_auto_open.py"
Note; this will take a significant amount of time currently, suggest sticking to a single day at a time.













