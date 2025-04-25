
from enum import Enum

class Color(Enum):
    RED = 1
    BLUE = 2





class A:
    def __init__(self, my_id):
        self.my_id = my_id
        self.color = Color.RED


if __name__ == "__main__":
    a = A(1)
    b = A(2)
    print(a.color)
