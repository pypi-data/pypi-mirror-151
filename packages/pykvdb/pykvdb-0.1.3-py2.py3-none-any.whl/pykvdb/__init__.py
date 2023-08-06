#!/usr/bin/python
# encoding: utf-8

__version__ = '0.1.1'
__author__ = 'Bingal'

import lmdb

class KVDB:
    def __init__(self, path=None, size=10*1024*1024):
        # 10MB
        self.env = lmdb.open('pykvdb' if not path else path,
                             map_size=size)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def set(self, sid, name):
        txn = self.env.begin(write=True)
        txn.put(str(sid).encode(), name.encode())
        txn.commit()

    def delete(self, sid):
        txn = self.env.begin(write=True)
        txn.delete(str(sid).encode())
        txn.commit()

    def get(self, sid):
        txn = self.env.begin()
        name = txn.get(str(sid).encode())
        return name.decode() if name else ''

    def cursor(self):
        txn = self.env.begin()
        cur = txn.cursor()
        return cur
      
    def close(self):
        self.env.close()
 

if __name__ == '__main__':
    
    with KVDB() as kv:
        kv.set('a', 'test')

    with KVDB() as kv:
        print(kv.get('a'))
    
    with KVDB() as kv:
        cur = kv.cursor()
        for k, v in cur:
            print(k.decode(), v.decode())

