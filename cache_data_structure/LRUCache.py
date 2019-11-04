__author__ ="ayomideayodele"
from datetime import datetime, timedelta
from time import sleep

from cache_data_structure.eviction_strategy import *

import sys
import threading

class DataNotFoundException(Exception):
    pass


class CacheClientNotFoundException(Exception):
    pass

class CacheNode:
    '''
    This class represent the data the user inserted into the cache and it also keeps the structure of the cache(which could be used with either eviction strategy LRU or LFU),
    which is pointing to the previous Node and Next Node in the data-structure, this structure helps us to achieve the eviction strategy,
    we would use for cache, the class also maintains the expiration_time which maybe used depending on what eviction strategy the user picked.
    '''
    def __init__(self,key,value,ttl=0):
        self.key   = key
        self.value = value
        self.next  = None
        self.prev  = None
        self.ttl   = ttl #Which means time to live
        self.expiration_time = datetime.now()+timedelta(seconds=ttl)

    def reset_expiration_time(self):
        self.expiration_time = datetime.now()+timedelta(seconds=self.ttl)

    def parse_data(self):
        return {self.key:self.value}


class LRUCache:
    def __init__(self,**kwargs):
        self.cache_strategy = kwargs.get('cache_strategy')
        self.threshold      = kwargs.get("threshold")
        self.__table        = dict()# This is the representation of the cache underhood
        self.__head         = None
        self.__tail         = None
        self.__curr_size    = 0
    def get_data(self,key):
        if not key in self.__table:
            raise DataNotFoundException("This key was not found in the table ")
        data = self.__table.get(key)
        self.__remove(data)
        self.__set_head(data)
        return  data.parse_data()

    def add_data(self,key,value):
        if key in self.__table:
            data        = self.__table.get(key)
            data.value  = value
            data.reset_expiration_time()
            self.__remove(data)
            self.__set_head(data)
        else:
            self.update_cache()
            if self.cache_strategy == EvictionStrategy.TIME_STRATEGY:
                new_data          = CacheNode(key,value,self.threshold)
            elif self.cache_strategy == EvictionStrategy.MEMORY_STRATEGY:
                new_data          = CacheNode(key, value)
            self.__table[key] = new_data
            self.__set_head(new_data)

    def remove_data(self,key):
        if key in self.__table:
            data = self.__table.get(key)
            self.__remove(data)
            return data
        raise DataNotFoundException

    def remove_header(self):
        if self.__head:
            data = self.__head
            self.__remove(data)
            return data
        else:
            raise DataNotFoundException

    def __len__(self):
        return len(self.__table)

    def update_cache(self):
        if self.__exceed_capacity():
            print(f"Removing the key {self.__tail.key}")
            del self.__table[self.__tail.key]
            self.__remove(self.__tail)

    def __exceed_capacity(self):
        if self.cache_strategy == EvictionStrategy.TIME_STRATEGY:
            '''
            This strategy checks the tail time and see if the time as expired then it will remove the tail
            '''
            if self.__tail:
                current_time = datetime.now()
                return current_time>self.__tail.expiration_time
            else:
                return False
        elif self.cache_strategy == EvictionStrategy.MEMORY_STRATEGY:
            '''
            This strategy checks the LRU cache size and compares it against the threshold set for it
            '''
            if self.__tail:
                return self.__curr_size>self.threshold
            else:
                return False
        return True
    def __remove(self,data):
        self.__curr_size -= sys.getsizeof(data) # in reducing the size of the cache
        if data.prev:
            data.prev.next = data.next
        else:
            self.__head    = data.next

        if data.next:
            data.next.prev = data.next
        else:
            self.__tail    = data.prev

    def __set_head(self,data):
        self.__curr_size += sys.getsizeof(data) # This is used in calculating the size of the cache
        if self.__head:
            self.__head.prev = data
        data.next = self.__head
        data.prev = None
        self.__head = data
        if not self.__tail:
            self.__tail = data

class CacheClient:
    _cache_client=None

    @classmethod
    def create_client(cls,strategy,threshold):
        kwargs = dict()
        if strategy == "memory":
            kwargs["cache_strategy"] = EvictionStrategy.MEMORY_STRATEGY
            kwargs["threshold"]      = threshold
        elif strategy == "time":
            kwargs["cache_strategy"] = EvictionStrategy.TIME_STRATEGY
            kwargs["threshold"] = threshold
        cls._cache_client = LRUCache(**kwargs)

    @classmethod
    def updater_thread(cls):
        cache_update = threading.Thread(target=cls.updater)
        return cache_update

    @classmethod
    def updater(cls):
        while True:
            print("Checking the cache")
            sleep(5)  # 5 sec's delay in the cache
            cls._cache_client.update_cache()

    @classmethod
    def get_data(cls,key):
        if cls._cache_client is None:
            raise CacheClientNotFoundException
        return cls._cache_client.get_data(key)

    @classmethod
    def set_data(cls,key,value):
        if cls._cache_client is None:
            raise CacheClientNotFoundException
        cls._cache_client.add_data(key,value)

    @classmethod
    def remove_data(cls,key):
        if cls._cache_client is None:
            raise CacheClientNotFoundException
        return cls._cache_client.remove_data(key)

    @classmethod
    def remove_header(cls):
        if cls._cache_client is None:
            raise CacheClientNotFoundException
        return cls._cache_client.remove_header()