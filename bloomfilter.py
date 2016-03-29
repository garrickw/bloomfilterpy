from math import *
import hashlib
import bitarray
import struct

class BloomFilter(object):

    def __init__(self, capacity = 1000, error_rate = 0.001):
        '''self.num_hash :       optimal number of hash functions
           self.num_bit :          the approprate bits of bloom filter
        '''
        self.capacity = capacity
        self.error_rate = error_rate
        self.num_hash = int(ceil(-capacity*log(error_rate) / pow(log(2), 2)))
        self.num_bit = int(ceil(log(1/error_rate, 2)))

        print self.num_hash
        print self.num_bit

        self.filter_bitarray = bitarray.bitarray(self.num_bit)
        self.filter_bitarray.setall(False)
        salts = [hashlib.md5(str(i)) for i in range(self.num_hash)]
        self.hashfns = [hashlib.md5(salt.digest()) for salt in salts]


    def add(self, item):
        """add new item into the filter_bitarray"""
        indexs = self.__get_indexs(item)
        for  index in indexs:
            self.filter_bitarray[index] = True

    def __get_indexs(self,item):
        indexs = []
        for hashfn in self.hashfns:
            h = hashfn.copy()
            h.update(item)
            hlen = h.digest_size/8
            index = struct.unpack("q"*hlen, h.digest())[0] % self.num_bit
            indexs.append(index)
        return indexs

    def __contains__(self, item):
        indexs = self.__get_indexs(item)
        for index in indexs:
            if not self.filter_bitarray[index]:
                return False
        return True

if __name__ == "__main__":
    test = BloomFilter(10000, 0.01)
    url = "www.baidu.com"
    if url in test:
        print "exsits"
    else:
        print "add"
        test.add(url)

    if url in test:
        print "exsits"
    else:
        print "add"
        test.add(url)