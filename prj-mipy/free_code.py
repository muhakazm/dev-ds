import mipy

ori_dict = {
    'aaa': 'aaa'
    ,'bbb': 'bbb'
    ,'ccc': 'ccc'
    ,'ddd': 'ddd'
}
d = mipy.InsensitiveKeysDict(ori_dict)
print(f'{d} \t {d['AAA']}')
d['AaA'] = 'AaA'
print(f'{d} \t {d['AAA']}')


