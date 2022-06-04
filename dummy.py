# run the app with dummy data

# import indera
import random

import time
import os
from dotenv import load_dotenv

os.nice(19)
load_dotenv()

refs = [3028, 3110] # [volt, freq], see reference table
opr_time = 30 # seconds, i.e. 24 * 3600
latency = 2 # between plant and database
interval = 5 # seconds, must be lot higher than latency
save_in = 'pg' # csv, pg

mb_host = os.getenv('MBHOSTURL')
mb_port = os.getenv('MBPORT')
db_params = {
  'host': os.getenv('DBHOST'),
  'port': os.getenv('DBPORT'),
  'user': os.getenv('DBUSER'),
  'password': os.getenv('DBPASS'),
  'dbname': os.getenv('DBNAME')
}
table = os.getenv('TABLENAME')

# pm5350 = indera.indera(mb_host, mb_port)
if save_in == 'csv':
  import simpan_csv
  monitor = simpan_csv.simpan(table, auto_time_name=True)
elif save_in == 'pg':
  import simpan_pg
  monitor = simpan_pg.simpan(db_params, table)

# Main app
interval -= latency
sleep_time = 0.8 * interval
expected_count = int(opr_time / interval)
i = 0
tstart = time.time()
tend = tstart + opr_time + 0.1
tnext = tstart + interval
print('Recording started')
while True:
  if time.time() >= tend: break
  jump = False
  # for trial in [1, 2, 3]:
  #   try:
  #     data = pm5350.mbpoll(refs)
  #     break
  #   except:
  #     if trial == 3:
  #       print('Read sensor data failed')
  #       jump = True
  if jump: continue
  # volt = data[3028]
  # freq = data[3110]
  volt = 220 + random.randint(-10, 10) + random.random()
  freq = 50 + random.randint(-5, 5) + random.random()
  for trial in [1, 2, 3]:
    try:
      monitor.insert(volt, freq)
      break
    except:
      if trial == 3:
        print('Store sensor data failed')
        jump = True
  if jump: continue
  progress = 100 * i / expected_count
  progress = str(int(progress)) + '%'
  print(progress, 'volt:', volt, 'freq:', freq)
  i += 1
  time.sleep(sleep_time)
  while True:
    if time.time() >= tnext: break
  tnext += interval
  
print('Recording finished! Count:', i, '/', expected_count)
