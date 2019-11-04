from time import sleep

from cache_data_structure.LRUCache import *
from cache_data_structure.eviction_strategy import *
import unittest

class LruCacheTest(unittest.TestCase):
    '''
    This test basically test two cases such as the Memory eviction process and Time eviction process
    '''
    def setUp(self):
        memory_kwargs = dict()
        memory_kwargs['cache_strategy'] = EvictionStrategy.MEMORY_STRATEGY
        memory_kwargs['threshold']      = 360 # maximum threshold is 360 bytes
        self.memory_lru = LRUCache(**memory_kwargs)
        self.memory_lru.add_data("google.com",3)
        self.memory_lru.add_data("facebook.com", 73)
        self.memory_lru.add_data("amazon.com", 53)
        self.memory_lru.add_data("yahoo.com", 45)
        self.memory_lru.add_data("bing.com", 63)
        self.memory_lru.add_data("youtube.com", 53)
        self.memory_lru.add_data("snapchat.com", 23)
        self.memory_lru.add_data("instagram.com", 33)
        self.memory_lru.add_data("netflix.com", 13)
        self.memory_lru.add_data("alibaba.com", 32)
        self.memory_lru.add_data("groupon.com", 1)
        time_kwargs   = dict()
        time_kwargs['cache_strategy'] = EvictionStrategy.TIME_STRATEGY
        time_kwargs['threshold']      = 30 # maximum threshold is 84 sec's from when it was inserted
        self.time_lru   = LRUCache(**time_kwargs)

    def set_create_time_lru(self):
        self.time_lru.add_data("google.com",3)
        sleep(3)
        self.time_lru.add_data("facebook.com", 73)
        sleep(3)
        self.time_lru.add_data("amazon.com", 53)
        sleep(3)
        self.time_lru.add_data("yahoo.com", 45)
        sleep(3)
        self.time_lru.add_data("bing.com", 63)
        sleep(3)
        self.time_lru.add_data("youtube.com", 53)
        sleep(3)
        self.time_lru.add_data("snapchat.com", 23)
        sleep(3)
        self.time_lru.add_data("instagram.com", 33)
        sleep(3)
        self.time_lru.add_data("netflix.com", 13)
        sleep(3)
        self.time_lru.add_data("alibaba.com", 32)
        sleep(3)
        self.time_lru.add_data("groupon.com", 1)

    def testMemory(self):
        '''
        We expect each entry will consist of about 56 byte each, that is for 360 bytes we expect 7 element at max
        present in the cache
        '''
        self.assertEqual(len(self.memory_lru),7)

    def testMemoryFindData(self):
        result = False
        try:
            self.memory_lru.get_data("google.com")
        except DataNotFoundException:
            result = True
        self.assertTrue(result)
        self.assertEqual(self.memory_lru.get_data("alibaba.com"),{'alibaba.com':32})

    def testTimeoutStrategy(self):
        self.set_create_time_lru()
        result=False
        try:
            self.time_lru.get_data("google.com")
        except DataNotFoundException:
            result=True
        self.assertTrue(result)
        self.assertEqual(self.time_lru.get_data("alibaba.com"),{'alibaba.com':32})