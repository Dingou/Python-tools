from collections import namedtuple

Student = namedtuple('Student', ['name', 'age', 'sex', 'email'])
student1 = Student('leo', '30', 'male', 'regardfs@gmail.com')
student2 = Student(name='tom', age=10, sex='male', email='gumdamfs@163.com')
print student2.age
print student2.name
isinstance(student1, tuple)
