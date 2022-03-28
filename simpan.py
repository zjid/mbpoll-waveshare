import psycopg

# Requires:
# - postgresql supported by psycopg,
# - database name, default 'monitor'
# - user name, default 'ks'
# - table name, default 'testhome'
# - column 'volt' and 'freq'

class simpan:

  def __init__(self, user, db_name, table_name):
    self.name = db_name
    self.user = user
    self.tabel = table_name

  def insert(self, volt, freq):
    '''Records voltage and frequency in a database'''
    with psycopg.connect('dbname=' + self.name + ' user=' + self.user) as conn:
      with conn.cursor() as cur:
        cur.execute(
          'INSERT INTO %s (volt, freq) VALUES (%s, %s)', 
          (self.tabel, volt, freq) )
        conn.commit()

  def fetch(self, size = 10):
    '''Buggy'''
    with psycopg.connect('dbname=' + self.name + ' user=' + self.user) as conn:
      with conn.cursor() as cur:
        cur.execute('SELECT * FROM %s', (self.tabel))
        out = cur.fetchmany(size)
    return out

