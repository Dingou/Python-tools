class Fib(object):
    __slot__ = ('num', 'lst')
    def __init__(self):
        self._num = 0
        self._lst = None
    @property
    def num(self):
        return self._num
    @num.setter
    def num(self, number):
        self._num = number
    @property
    def lst(self):
        return self._lst
    @lst.setter
    def lst(self, new_lst):
        self.lst = new_lst
    def __len__(self):
        return len(self._lst)
    def __str__(self):
        return str(self._lst)
    def __call__(self, n):
        self._num = n
        if self._num == 0:
            L = []
        elif self._num == 1:
            L = [0]
        else:
            L = [0, 1]
            for i in range(2, self._num):
                L.append(L[-1]+L[-2])
        return str(L)