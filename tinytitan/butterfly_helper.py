# Returns -1 if no match, otherwise returns index of
# first matching item.
def find_index_of_matching(thelist, target_item):
    index = 0
    for item in thelist:
        if item == target_item:
            return index
        ++index
    return -1

def default_combo_index(thelist, target_item, default_index=0):
    result = find_index_of_matching(thelist, target_item)
    if result == -1:
        result = default_index
    return result

