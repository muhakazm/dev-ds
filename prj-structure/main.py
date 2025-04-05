from src import helper as h
from src import dict_helper as dh

# print('Hello, World!')

a = [1,2,3,4,5]
b = [3,4,5,6,7,8]
c = h.get_lists_intersection(a,b)
# print(c)

p = {'a': 12, 'b': 13, 'c': 14}
p2 = dh.dict_key_value_printer(p)

x = ['a', 12, 'b', 13, 'c', 14, 'd', 15, 'e']
x2 = h.list_elements_to_key_value_pair(x)
# print(x2)

h.list_elements_to_key_value_pair_printer(x)