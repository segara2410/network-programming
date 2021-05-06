import random

random.seed(923982341)
with open('newinput.txt', 'w') as f:
    for ii in range(10000):
        nn = random.randint(1, 1000)
        if nn % 2 == 0:
            print("ADD ", nn, file=f)
        else:
            print("DEC ", nn, file=f)
