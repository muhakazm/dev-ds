import mipy

message = mipy.greeting()
print(message)


# Example Usage
d = mipy.InsensitiveKeysDict({"Hello": "World", "TEST": 123})
print(d)
print(d["hello"])  # Output: World
print(d["test"])  # Output: 123

# # Original key casing is preserved
# print(d)  # Output: {'Hello': 'World', 'TEST': 123}

# # Even if we update with a different case, the key remains in its original form
# d["hElLo"] = "New Value"
# print(d)  # Output: {'Hello': 'New Value', 'TEST': 123}

# # Convert to a normal dictionary
# standard_dict = d.to_dict()
# print(standard_dict)  # Output: {'Hello': 'New Value', 'TEST': 123}