import psycopg

# Requires:
# - postgresql supported by psycopg,
# - database name
# - user name
# - table name
# - column 'volt' and 'freq'

class simpan:

  def __init__(self, params, tablename):
    '''Params is a dictionary. In local database, keys: user, password, dbname.
    For remote database, add keys: host, port. More params depend on your db.
    Different version may use key "database" instead of "dbname".'''
    text = ''
    for (k,v) in params.items():
      text += k + '=' + str(v) + ' '
    self.params = text
    self.table = tablename

  def insert(self, volt, freq):
    '''Records voltage and frequency in a database'''
    with psycopg.connect(self.params) as conn:
      with conn.cursor() as cur:
        cur.execute(
          # 'INSERT INTO %s (volt, freq) VALUES (%s, %s)', 
          # (self.table, volt, freq)
          'INSERT INTO powerlog (volt, freq) VALUES (%s, %s)', 
          (volt, freq)
        )
        conn.commit()

  def fetch(self, size = 10):
    '''Buggy'''
    with psycopg.connect(self.params) as conn:
      with conn.cursor() as cur:
        cur.execute('SELECT * FROM %s', (self.table))
        out = cur.fetchmany(size)
    return out

