from src import dict_helper as dh

def get_lists_intersection(list1, list2):
    return list(set(list1) & set(list2))

def list_elements_to_key_value_pair(my_list):
    my_dict = dict()
    for i, element in enumerate(my_list):
        if i%2 == 0:
            key = element
            my_dict[key] = None
        else:
            my_dict[key] = element
    return my_dict

def list_elements_to_key_value_pair_printer(my_list):
    my_dict = list_elements_to_key_value_pair(my_list)
    dh.dict_key_value_printer(my_dict)


x = ['a', 12, 'b', 13, 'c', 14, 'd', 15, 'e']
x2 = list_elements_to_key_value_pair(x)

list_elements_to_key_value_pair_printer(x)