import random

"""
-> "list" object extension/helper functions
"""

""" Master Search """
def get(index, items, default=False):
    """ Safely get index """
    if type(index) in [bool, list, tuple, dict]:
        return default
    _index = int(index)
    try:
        count = _index + 1
        l = len(items)
        if count > l:
            return default
        return items[_index]
    except Exception as e:
        print(f"Failed to get index. error=[ {e} ]")
        return default

def remove_index(index: int, items: []):
    count = 0
    new_list = []
    for item in items:
        if count == index:
            count += 1
            continue
        count += 1
        new_list.append(item)
    return new_list

""" Manipulation """
def scramble(orig):
    """ Randomize List """
    try:
        dest = orig[:]
        random.shuffle(dest)
        return dest
    except Exception as e:
        print(f"Failed to Scramble List. error=[ {e} ]")
        return orig

def flatten(*args):
    """ Flatten lists into one single list.
            (1, 2, ['b', 'a' , ['c', 'd']], 3)
            [1, 2, 'b', 'a', 'c', 'd', 3]
        :param args: items and lists to be combined into a single list
        :rtype: list
    """
    x = []
    list(args)
    for l in args:
        if not isinstance(l, (list, tuple)):
            l = [l]
        for item in l:
            if isinstance(item, (list, tuple)):
                x.extend(flatten(item))
            else:
                x.append(item)
    return x

def flatten_v2(args):
    """ Flatten lists into one single list.
            (1, 2, ['b', 'a' , ['c', 'd']], 3)
            [1, 2, 'b', 'a', 'c', 'd', 3]
        :param args: items and lists to be combined into a single list
        :rtype: list
    """
    x = []

    for item in args:
        if type(item) in [list, tuple]:
            temp = flatten_v2(item)
            x.extend(temp)
        else:
            x.append(item)
    return x

def merge_lists(list_one, list_two) -> []:
    if not list_one:
        return list_two
    if not list_two:
        return list_one
    result = []
    list_one.extend(list_two)
    for myDict in list_one:
        if myDict not in result:
            result.append(myDict)
    return result

def to_str(data) -> str:
    if type(data) is str:
        return data
    temp_str = ""
    for item in data:
        temp_str += "\n" + str(item)
    return temp_str

def remove_duplicates(list_in: list) -> list:
    try:
        return list(set(list_in))
    except Exception as e:
        print(f"Failed to removed Dups. error=[ {e} ]")
        return list_in

