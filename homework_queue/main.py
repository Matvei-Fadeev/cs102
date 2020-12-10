from queue import *
from country import *

def print_queue_list(queue_list, name=""):
    print("Print the %s queue" % (name))
    for elem in queue_list:
        print(elem)
    print()

def test_queue():
    numbers = MyQueue()
    numbers.add(5)
    numbers.add(3)
    numbers.add(6)
    numbers_list = numbers.get_list()
    print_queue_list(numbers_list, "numbers")

    countries = MyQueue()
    countries.add(Country("New-Landia", 4321))
    countries.add(Country("Old-Fanthya", 219))
    countries.add(Country("Magiska", 12321))
    countries.add(Country("LuLu", 61))
    countries_list = countries.get_list()
    print_queue_list(countries_list, "countries")

if "__main__" == __name__:
    test_queue()


    #
