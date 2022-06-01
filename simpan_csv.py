import time

def kini():
  now = [str(t) for t in time.localtime()]
  now[1:6] = [t if len(t) > 1 else '0' +  t for t in now[1:6]]
  # now[7] = '0' * (3 - len(now[7])) + now[7]
  return ''.join(now[:6]) #+ '_' + ''.join(now[6:])

class simpan:

  def __init__(self, name: str, auto_time_name = True):
    '''Automatically generates file [name][time].csv.'''
    if '.csv' in name: name = name.replace('.csv', '')
    if auto_time_name:
      self.name = name + kini() + '.csv'
    else:
      self.name = name + '.csv'
    try:
      with open(self.name, 'x') as f:
        f.write('time,volt,freq\n')
    except FileExistsError:
      with open(self.name, 'w') as f:
        f.write('time,volt,freq\n')

  def insert(self, volt, freq):
    with open(self.name, 'a') as f:
      line = [str(time.time()), str(volt), str(freq)]
      f.write(','.join(line) + '\n')

  def fetch(self):
    return None
