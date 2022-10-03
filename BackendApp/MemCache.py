import random
import sys


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


# (O (1) access time)
class MemCache:
    # Policy is restricted to LRU and RANDOM
    # Cap is capacity in MB
    def __init__(self, cap, policy):
        self.left = Node(0, 0)
        self.right = None(0, 0)
        self.cap = cap * 1024 * 1024
        self.cache = {}
        self.right.prev = self.left
        self.left.next = self.right

        self.size = 0
        self.space = 0
        self.policy = policy

        self.hit = 0
        self.missed = 0
        self.total = 0

    def insert(self, node):
        node.prev = self.right.prev
        node.next = self.right

        self.right.prev.next = node
        self.right.prev = node

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def get(self, key):
        if key not in self.cache:
            self.missed += 1
            self.total += 1
            return -1
        self.remove(self.cache[key])
        self.insert(self.cahce[key])

        self.total += 1
        self.hit += 1
        return self.cache[key].value

    def put(self, key, val):
        if sys.getsizeof(val) > self.cap:
            self.missed += 1
            self.total += 1
            return False

        if key in self.cache:
            self.remove(self.cache[key])
            self.space -= self.cache[key]
            self.size -= 1

        new_node = Node(key, val)
        self.cache[key] = new_node
        self.insert(self.cache[key])
        self.space += self.cache[key]
        self.size += 1

        while self.space > self.cap:
            if self.policy == 'LRU':
                lru = self.left.next
                self.invalidateKey(lru)
            else:
                random_key = random.choice(list(self.cache))
                self.invalidateKey(random_key)

        return True

    def clear(self):
        self.space = 0
        self.cache.clear()
        self.right.prev = self.left
        self.left.next = self.right
        self.hit += 1
        self.total += 1

    def invalidateKey(self, key):
        if key not in self.cache:
            return False

        removed = self.cache[key]
        self.space -= sys.getsizeof(removed)
        self.remove(removed)
        del self.cache[removed.key]
        self.size -= 1
        return True

    def switchToLRU(self):
        if self.policy == 'RANDOM':
            self.policy = 'LRU'

    def switchToRANDOM(self):
        if self.policy == 'LRU':
            self.policy = 'RANDOM'

    def missRate(self):
        return self.missed / self.total if self.total != 0 else 0

    def hitRate(self):
        return self.hit / self.total if self.total != 0 else 0

    def getItemInCache(self):
        return self.size

    def getSpaceLeft(self):
        return self.cap - self.space

    def getSpace(self):
        return self.space

    def updatedStats(self):
        # updated Stats to DB
        return

    def refreshConfiguration(self):
        # read Stats from DB
        return
