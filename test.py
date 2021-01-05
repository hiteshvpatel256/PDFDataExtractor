# import re

# regex_voter_id = '[_\|\]})]'
# line = '_S 338) 338} SGU0751982'
# sr_no = ''
# line = re.sub(regex_voter_id, '', line)
# print(line)
a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

delete_indexes = [2, 5, 8]

for index in delete_indexes:
    del a[index]
    print(a)
