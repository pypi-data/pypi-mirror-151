from math import sqrt, atan2, hypot, cos, sin
from random import uniform
from typing import Tuple


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def random(min: float=-1, max: float=1):
        '''
        Create an Vector2 object with random values between min and max
        '''
        return Vector2(uniform(min, max), uniform(min, max))

    @staticmethod
    def fromTuple(tuple: Tuple):
        '''
        Create an Vector2 object with a tuple
        '''
        return Vector2(tuple[0], tuple[1])

    def copy(self):
        '''
        Copys the vector
        '''
        return Vector2(self.x, self.y)

    def normalize(self):
        mag = self.getMag()
        if mag > 0:
            self.x /= mag
            self.y /= mag

    def rotate(self, deg):
        h = atan2(self.y, self.x) + deg
        mag = self.getMag()
        self.x = cos(h) * mag
        self.y = sin(h) * mag

    def getMag(self):
        return sqrt(self.x**2 + self.y**2)

    def setMag(self, magnitude):
        newX = self.x * magnitude / self.getMag()
        newY = self.y * magnitude / self.getMag()
        self.x = newX
        self.y = newY

    def getAngle(self, other):
        return atan2((other.y - self.y), (other.x - self.x))

    def getDist(self, other):
        '''
        Get distance between two vectors
        '''
        return hypot((other.x - self.x), (other.y - self.y))

    def toTuple(self):
        return self.x, self.y

    def toInt(self):
        return Vector2(int(self.x), int(self.y))

    def toFloat(self):
        return Vector2(float(self.x), float(self.y))

    def compineToList(self, *args):
        '''
        Pass as many vectors as you want as arguments.
        '''
        vectors = [self.x, self.y]
        for vec in args:
            if type(vec) == Vector2:
                vectors.append(vec.x)
                vectors.append(vec.y)
        return vectors

    def __repr__(self):
        return f'Vector2({self.x}, {self.y})'

    def __add__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x + other.x, self.y + other.y)
        elif type(other) == int or float:
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x - other.x, self.y - other.y)
        elif type(other) == int or float:
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x * other.x, self.y * other.y)
        elif type(other) == int or float:
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x / other.x, self.y / other.y)
        elif type(other) == int or float:
            return Vector2(self.x / other, self.y / other)
