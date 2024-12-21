
def test():
    print(1111)
    yield
    print(222)

if __name__ == "__main__":
    a = test()
    # next(a)
    # next(a)