from queue import *

class Country:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return "The %s country is %s years old." % (self.name, self.age)
