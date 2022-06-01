Usage:
  - Create a .env file. Adjust the values based on your setup.
```HOSTURL=10.0.0.1
PORT=26
DBNAME=tes
TABLENAME=power
```
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

