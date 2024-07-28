array = [1, 2, 3]


def test(cur_array):
    cur_array[0] = 10


test(array)
print(array)
