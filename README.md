**Cache service**
The main purpose of a cache is to achieve the following
1) Fast lookup
2) Fast insertion
But this performance comes with a cost of memory because, most cache
such as this uses in-memory mechanism.
To solve this i used an eviction mechanism such as LRU, which is based
on time or memory eviction, this is been selected as an argument during the
runtime, currently the default is time and it updating the cache every 60 sec's

To run the program you will need to run the command
python cache_service.py --strategy time --threshold 60

--strategy defines what eviction strategy you would like to select
from either time or memory, currently this service support LRU eviction, with strategy
such as memory or time, threshold means at what threshold should the
cache service begin to evicts some of the data's for memory, the threshold
is measured in bytes and for time the threshold is measured in seconds

example python cache_service.py --strategy memory --threshold 2048

**Rest service**
Currently the service support two operation such as 
/cache_service (post) sample data is 
{"key":"yahoo.com","value":23}
/cache_service/<key> (get) sample data is localhost:5000/cache_servic/yahoo.com
response {"yahoo.com":"23"}

**Unit Test**
The unit test test_LRUCache basically shows how the cache works with
different mechanism such as memory or time

**Third Party tool**
Basically the only third party tool used was flask
