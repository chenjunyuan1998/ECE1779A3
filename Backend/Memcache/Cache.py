import sys
from collections import defaultdict
from collections import OrderedDict

GET_COUNT_THRESHOLD = 10

# key: username, value: set of persistent keys
persistent_dict = defaultdict(set)
lru_dict = defaultdict(OrderedDict)
capacity_dict = dict()
space_dict = dict()


# TODO: record the number of get on a specific key, put it into persistent_dict if it surpasses GET_COUNT_THRESHOLD
# TODO: update capacity for a user
def add_user(username, capacity):
    persistent_dict[username] = set()
    lru_dict[username] = OrderedDict()
    capacity_dict[username] = capacity * 1024 * 1024
    space_dict[username] = 0


def delete_user(username):
    del persistent_dict[username]
    del lru_dict[username]


def update_capacity(username, capacity):
    pass


def get_key(username, key):
    if key not in lru_dict[username]:
        return - 1

    lru_dict[username].move_to_end(key)
    return lru_dict[username][key]


def put_key(username, key, value):
    if key in lru_dict[username]:
        lru_dict[username].move_to_end(key)
        space_dict[username] -= sys.getsizeof(lru_dict[username][key])

    lru_dict[username][key] = value
    space_dict[username] += sys.getsizeof(value)

    if space_dict[username] > capacity_dict[username]:
        while space_dict[username] > capacity_dict[username]:
            item = lru_dict[username].popitem(last=False)
            space_dict[username] -= sys.getsizeof(item[1])
        return "OK"
    else:
        return True

