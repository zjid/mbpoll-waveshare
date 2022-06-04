Usage:
  - Create a .env file. Adjust the values based on your setup.
```
MBHOSTURL=10.0.0.1
MBPORT=26
DBHOST=localhost
DBPORT=1234
DBUSER=user
DBPASS=mypassword
DBNAME=mydatabase
TABLENAME=table1
```
    MB = modbus
    DB = database
  - Run the app.py.
---

The app runs under this setup:
  - Schneider PM5350
  - Waveshare RS232/485 to eth
  - Ethernet connection to computer
  
Requirements:
  - linux
  - mbpoll
Python packages:
  - dotenv
  - os
  - psycopg
  - subprocess
  - time

Still no success with this setup:
  - King Pigeon M100T
  - ADAM-6017

