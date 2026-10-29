monday = {"ana", "ben", "cara", "dan"}
tuesday = {"cara", "dan", "eli"}

print(monday | tuesday)    # union: everyone
print(monday & tuesday)    # intersection: both days
print(monday - tuesday)    # only Monday
print(monday ^ tuesday)    # exactly one day

unique_ips = set(["1.1.1.1", "8.8.8.8", "1.1.1.1"])
print(len(unique_ips))     # 2
