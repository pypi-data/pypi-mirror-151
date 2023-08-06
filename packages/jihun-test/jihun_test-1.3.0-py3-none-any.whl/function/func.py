import numpy as np


def testAdd(a, b):
    result = a + b
    return result


def testHello(a):
    result = "hello " + a
    return result


def testRandomArray(a):
    result = np.random.rand(a)
    return result


if __name__ == "__main__":
    result = testAdd(2, 3)
    result2 = testHello("jihun")
    result3 = testRandomArray(4)
    print(result)
    print(result2)
    print(result3)
