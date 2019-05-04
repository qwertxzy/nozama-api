import mysql.connector

user=''
passwd=''
database=''
host=''

connector = mysql.connector.connect(
    user=user,
    database=database,
    passwd=passwd,
    host=host)