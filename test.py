"""A comparation about """


from bloomfilter import BloomFilter
import sys
import functools
import time
import cPickle
import  hashlib
import uuid


def timeit(func):
    @functools.wraps(func)
    def wrapper(*arg, **kw):
        start = time.time()
        func()
        end = time.time()
        print "costs {time}s.".format(time = end - start)
    return wrapper



@timeit
def test_bloom():
    data = (str(uuid.uuid1()) for i in range(100000))
    filter = BloomFilter(100000, 0.0001)
    for item in data:
        if not item in filter:
            filter.add(item)
    print "{name} costs {bytes} bytes.".format(name=sys._getframe().f_code.co_name, bytes=filter.container_size())


@timeit
def test_set():
    s = set()
    data = (str(uuid.uuid1()) for i in range(100000))
    for i in data:
        s.add(i)
    t = cPickle.dumps(s)
    print "{name} costs {bytes} bytes.".format(name=sys._getframe().f_code.co_name, bytes=sys.getsizeof(t))

@timeit
def test_list():
    l = list()
    data = (str(uuid.uuid1()) for i in range(100000))
    for i in data:
        if i not in l:
            l.append(i)
    t = cPickle.dumps(l)
    print "{name} costs {bytes} bytes.".format(name=sys._getframe().f_code.co_name, bytes=sys.getsizeof(t))


if __name__ == "__main__":
    test_set()
    print 
    test_bloom()
    print 
    test_list()

#output:
#
#test_set costs 4788979 bytes.
#costs 2.68518805504s.
#
#test_bloom costs 692464 bytes.
#costs 8.05900907516s.
#
#test_list costs 4788943 bytes.
#costs 67.8493359089s
#
#Aparently bloomfilter is considerable solution when data become so big, because it save a lot of space.

