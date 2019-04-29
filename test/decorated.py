from functools import wraps
class aba():
    def __init__(self,ss=11):
        self.ss = ss
    def jaon(self,func):
        @wraps(func)
        def decorated(x):
            if x == 1:
                return func(x)
            else:
                return 0
        return decorated
bb = aba()
def a(self):
    print(self)
    return 123

def b(c):
    def w():
        c()
        return c.x

@b
def d(x):
    print(x)
    return 15
print(d)

@bb.jaon
def obj(x):
    print(x)
    return x
print(obj(1))