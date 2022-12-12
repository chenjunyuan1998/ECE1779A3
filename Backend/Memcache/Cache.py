import sys
from collections import defaultdict
from collections import OrderedDict

# key: username, value: set of persistent keys
class Cache:
    def __init__(self):
        self.persistent_key = defaultdict(set)
        self.persistent_store = defaultdict(dict)
        self.lru_dict = defaultdict(OrderedDict)
        self.capacity_dict = defaultdict(int)
        self.space_dict = defaultdict(int)
        self.count_dict = defaultdict(dict)

    def set_cap(self, username, capacity):
        self.capacity_dict[username] = capacity * 1024 * 1024

    def findFirst(self,ordDict):
        return next(iter(ordDict))

    def put_key(self,username, key, value):
        if username not in self.capacity_dict:
            return -1

        if key not in self.count_dict[username]:
            self.count_dict[username][key] = 0
        self.count_dict[username][key] += 1

        if key not in self.persistent_key[username]:
            if key in self.lru_dict[username]:
                self.lru_dict[username].move_to_end(key)
                self.space_dict[username] -= sys.getsizeof(self.lru_dict[username][key])

            self.lru_dict[username][key] = value
            self.space_dict[username] += sys.getsizeof(value)

            while self.space_dict[username] > self.capacity_dict[username]:
                if not self.lru_dict[username]:
                    return 0
                    # all space is allocated for presistent data, ask user to delete mannually
                popped = self.lru_dict[username].popitem(last=False)
                self.space_dict[username] -= sys.getsizeof(popped[1])
        else:
            cur = sys.getsizeof(self.persistent_store[username][key])
            self.space_dict[username] -= cur
            if self.space_dict[username] + value > self.capacity_dict[username]:
                while self.space_dict[username] > self.capacity_dict[username]:
                    if not self.lru_dict[username]:
                        self.space_dict[username] += cur
                        return 0
                        # all space is allocated for presistent data, ask user to delete mannually
                    popped = self.lru_dict[username].popitem(last=False)
                    self.space_dict[username] -= sys.getsizeof(popped[1])

            self.persistent_store[username][key] = value
            self.space_dict[username] += sys.getsizeof(value)

        self.addToPersistent(username,key)

        return 1

    def collectCount(self, username, key):
        return self.count_dict[username][key]

    def addToPersistent(self, username, key):
        if self.collectCount(username,key) > 10:
            popped = self.lru_dict[username][key]
            del self.lru_dict[username][key]
            self.persistent_key[username].add(key)
            self.persistent_store[username][key] = popped

    def deleteFromPersistent(self, username, key):
        self.space_dict -= sys.getsizeof(self.persistent_store[username][key])
        del self.persistent_store[username][key]
        self.persistent_key[username].remove(key)

    def deleteValue(self, username, key):
        if key not in self.lru_dict[username] and key not in self.persistent_key[username]:
            return False

        if key in self.lru_dict[username]:
            popped = self.lru_dict[username][key]
            self.space_dict -= sys.getsizeof(popped)
            del self.lru_dict[username][key]
        else:
            self.deleteFromPersistent(username, key)
        return True

    def delete_user(self, username):
        del self.persistent_key[username]
        del self.lru_dict[username]
        del self.space_dict[username]
        del self.persistent_store[username]
        del self.count_dict[username]
        del self.capacity_dict[username]

    def get_key(self,username, key):
        if key not in self.lru_dict[username]:
            if key not in self.persistent_key[username]:
                return - 1

        if key in self.persistent_key[username]:
            return self.persistent_store[username][key]

        if key in self.lru_dict[username]:
            self.lru_dict[username].move_to_end(key)
            self.count_dict[username][key] += 1
            self.addToPersistent(username, key)
            return self.lru_dict[username][key]