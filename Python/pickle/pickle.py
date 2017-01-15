import pickle

d = [1,2,3]
pickle.dump(d, open("history.txt", 'w'))
pickle.load(d, open("history.txt", 'r'))


