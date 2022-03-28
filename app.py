import indera
import simpan
import time
import os
from dotenv import load_dotenv

os.nice(19)
load_dotenv()

refs = [3028, 3110] # [volt, freq], see reference table
opr_time = 30 # detik, boleh 24 * 3600
interval = 5 # detik, disarankan >= 2 detik

host = os.getenv('HOSTURL')
port = os.getenv('PORT')
user = os.getenv('USER')
db_name = os.getenv('DBNAME')
table = os.getenv('TABLENAME')

pm5350 = indera.indera(host, port)
monitor = simpan.simpan(user, db_name, table)

# Main app
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
  for trial in [1, 2, 3]:
    try:
      data = pm5350.mbpoll(refs)
      break
    except:
      if trial == 3:
        print('Read sensor data failed')
        jump = True
  if jump: continue
  volt = data[3028]
  freq = data[3110]
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

