"""
At Ormuco, we want to optimize every bits of software we write. 
Your goal is to write a new library that can be integrated to the Ormuco stack. 
Dealing with network issues everyday, latency is our biggest problem. 
Thus, your challenge is to write a new Geo Distributed LRU (Least Recently Used) cache with time expiration. 
This library will be used extensively by many of our services so it needs to meet the following criteria:
 
    1 - Simplicity. Integration needs to be dead simple.
    2 - Resilient to network failures or crashes.
    3 - Near real time replication of data across Geolocation. Writes need to be in real time.
    4 - Data consistency across regions
    5 - Locality of reference, data should almost always be available from the closest region
    6 - Flexible Schema
    7 - Cache can expire 
"""


# EXPLAINING THE DISTRIBUTED NATURE OF LRU CAHCHE: In order to make this distributed we would design a central server that facilitates queries between worker machines.
# Each machine would have a geo location and the central server would maintain this ensuring that reads are always from the closest machine
# Each machine would have a copy of the cache and the central server would execute the LRU eviction policies and read/write/remove data from machines.
# When we write to LRU cache we would update it an all machines -- in the case of a failiure we would have a correct copy in another machine


#NOTE: Python used for simplicity sake but other languages may be better suited for this task since speed,concurrency, and security are important

import time

class LRUCache:

    def __init__(self,cap):
        self.cap = cap
        self.size = 0
       
        self.cache = {}
        self.head = None
        self.tail = None

    def put(self,key,value,expiration_time=0):
        is_node_new = False
        node = self.cache.get(key)
        if node == None: #if true its a new item otherwise replacing
            node = list_node(key,value,expiration_time) #create our new node
            is_node_new = True
            if self.size>=self.cap:
                self.remove_node(self.tail,False)
            else: 
                if self.size==0:
                    self.tail = node
                    self.head = node
                self.size+=1
        elif expiration_time >0:
            node.expiration_time = expiration_time 
        
        #item is most recently used item so should be set to head
        self.set_as_head(node,is_node_new)
        #updating the cache
        self.cache[key] = node

    def get(self,key):
        query = self.cache.get(key)
        if query != None:
            if query.is_expired():
                self.remove_node(query,False)
                self.size-=1 
            else:
                self.set_as_head(query,False)
                return query.value
        return None

    def remove_node(self,node,temp_removal):
        if self.size == 1:
            self.head = None
            self.tail = None
        elif node == self.head:
            self.head = node.prev
            self.head.next = None
        elif node == self.tail:
            self.tail = self.tail.next
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        
        if not temp_removal:
            del self.cache[node.key]
        
    def set_as_head(self,node,is_new):
        if not is_new:
            self.remove_node(node,True)
        temp = self.head
        node.prev = self.head
        self.head = node
        temp.next = self.head
        node.last_use_time = (time.time() * 1000) #update the time

    def print_cache(self): # for testing
        if self.size == 0: print(l.cache)
        else:
            for key in self.cache.keys():
                print(str(key)+" : "+ str(self.cache[key].value))
        print("")
        

class list_node: #implment my own linked_list class tp minimize overhead of unknown library
    def __init__(self,key,value,expiration_time):
        self.key = key
        self.value = value
        self.expiration_time = expiration_time
        self.last_use_time = (time.time() * 1000)

        self.next = None
        self.prev = None

    def is_expired(self):
        
        if self.expiration_time>0 and abs((time.time() * 1000) - self.last_use_time) >= self.expiration_time :
            return True
        return False


if __name__ == "__main__":
    
    #intro
    print("Showing lru cache works with simple demo! \nStart by instanstiating a cache of capacity 3")
    print("Note: all reads and writes from cache are optimzed to 0(1) for high speed. I implemented by own version of doubly linked list (that maintains the lru info) to show my understanding")
    l = LRUCache(3)
    print(l)
    print("")

    #test 1
    print("Testing 'put': \nStart by adding 6 items to the cache by looping from 1-6 and updating the key and value to value i from iteration i")
    print("In this experiment the size of cache should never exceed 3 and the final cahche should have values 3,4, and 5 as values 0,1,and 2 would be evicted as they were the least recently used")
    print("Note: Expiration times are set to zero by default for this expiriment \n ")

    print("Empty cache shown below \nStarting test 1 now... \n")
    print(l.cache)
    
    for i in range(6):
        l.put(i,i)
        print("Cache at Iteration "+ str(i))
        l.print_cache()


    #test 2
    print("Testing 'get': \n Here we will simply attemp to get values 3-6. For 3,4,& 5 it should return 3,4,& 5 repectivley and will 'None' for 6 as 6 isnt in cache")
    print("Starting test 2 now...\n")
    for i in range(3,7): 
        val = l.get(i)
        print("For key value "+ str(i)+" we get "+str(val))
    print("")


    #test 3
    print("Testing LRU eviction policy \n")

    print("Here we will 'put' 3 new value (1-3) then look at the cache to see that 5 then 4 and then 3 are is replaced from the cache as these were the least recently used in order from the last test")
    print("Starting test 3 now...\n")
    for i in range(3):
        l.put(i,i)
        print("Cache at Iteration "+ str(i))
        l.print_cache()


        
