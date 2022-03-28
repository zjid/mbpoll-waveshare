import subprocess as sp

class indera:

  limit = 100
  nmin = 2700
  nmax = 3194

  def __init__(self, host, port):
    '''Host ip address and port'''
    self.host = host
    self.port = port

  def _normalize(n):
    '''Limit and make even n'''
    if n < indera.nmin: n = indera.nmin
    elif n > indera.nmax: n = indera.nmax
    if n % 2 == 0: return n
    return n + 1
  def _normalize_refs(refs):
    '''Limit, make even, trim, and sort refs to acceptable arguments'''
    return sorted(list(set(list(map(indera._normalize, refs)))))

  def _check_output(self, startref, count):
    '''Get mbpoll output once'''
    return sp.check_output([
      'mbpoll',
      str(self.host),
      '-p ' + str(self.port),
      '-t 4:float',
      '-B',
      '-1',
      '-c ' + str(count),
      '-r ' + str(startref),
    ])

  def _simplify(out):
    '''Returns trim string from mbpoll output'''
    out = str(out).replace('\\n', '').replace('\\t', '')
    out = out.replace('-nan', '0').replace('"', '').replace(' ', '')
    out = out.split('Polling slave')[1]
    out = out.split('[')[1:]
    semua = []
    for rv in out:
      rv = rv.split(']:')
      semua.append([int(rv[0]), float(rv[1])])
    return semua

  def _split_batch(refs):
    '''Split mbpoll call to few calls due to limitation'''
    l = len(refs)
    batches = []
    newbatch = True
    i = 0
    while True:
      if newbatch:
        point0 = refs[i]
        batch = [point0]
      i += 1
      if i >= l:
        batches.append(batch)
        break
      elif refs[i] - point0 >= indera.limit:
        batches.append(batch)
        newbatch = True
        continue
      else:
        batch.append(refs[i])
        newbatch = False
    return batches

  def _bulk_read(self, batch):
    '''Returns list of pairs of all reference and value'''
    l = len(batch)
    if l < 1:
      return []
    elif l == 1:
      return indera._simplify(self._check_output(batch[0], 1))
    else:
      ref = min(batch)
      maxref = max(batch)
      count = (maxref - ref) // 2 + 1
      return indera._simplify(self._check_output(ref, count))

  def mbpoll(self, refs):
    '''Returns dictionary of selected reference and value'''
    refs = indera._normalize_refs(refs)
    bats = indera._split_batch(refs)
    semua = []
    for bat in bats:
      out = self._bulk_read(bat)
      semua.extend(out)
    kamus = {}
    for pair in semua:
      if pair[0] in refs:
        kamus[ pair[0] ] = pair[1]
    return kamus

# pm5350 = indera('local', 502)
# refs = [2600, 2700, 2800, 3027, 3028, 3110, 3111, 3194, 3200]
# print(refs)
# refs = indera._normalize_refs(refs)
# print(refs)
# bats = indera._split_batch(refs)
# print(bats)
# print(pm5350.mbpoll(refs))
