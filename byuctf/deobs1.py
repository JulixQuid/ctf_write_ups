numbers = [12838, 1089, 16029, 13761, 1276, 14790, 2091, 17199, 2223, 2925, 17901, 3159, 18135, 18837, 3135, 19071, 4095, 19773, 4797, 4085, 20007, 5733, 20709, 17005, 2601, 9620, 3192, 9724, 3127, 8125]
u = 3
U = 256

# Compute some_list as [pow(3, i, 256) for i in range(3, 33)]
some_list = [pow(3, i, 256) for i in range(3, 33)]

# Compute the flag characters
flag = []
for i in range(30):
    flag.append(chr(some_list[i]))
print(some_list)
print(''.join(flag))