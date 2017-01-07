class Student(object):

    def __init__(self, name, score):
        self.name = name
        self._score = score

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self._score = score

    @property
    def grade(self):
        if(self._score >= 80):
            return "A"
        elif(self._score < 60):
            return "C"
        else:
            return "B"

    @grade.setter
    def grade(self, grade):
        self.grade = grade

s = Student('Bob', 59)
print s.grade

s.score = 60
print s.grade

s.score = 99
print s.grade