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


import dir_iter
import os

def date_helper(fname):
    return (os.stat(fname).st_mtime, fname)

def sort_by_date(seq):
    timed = map(date_helper, seq)
    timed.sort()
    return timed

# this function seems convoluted
def get_files(image_dir):
  files = []
  for ii in range(len(image_dir.list_repr())):
    if os.path.isdir(image_dir.entry(ii)):
      image_dir.add(ii)
      for jj in range(len(image_dir.list_repr())):
        files.append(image_dir.entry(jj))
      image_dir.pop()
  return files

def get_newest_image_name():
    image_dir = dir_iter.Directory_iter([u'e:\\Images'])
    image_dir.add(0)
    files = get_files(image_dir)
    files_sorted = sort_by_date(files)
    if len(files_sorted) > 0:
        return files_sorted[-1][1]
    else:
        return u''


