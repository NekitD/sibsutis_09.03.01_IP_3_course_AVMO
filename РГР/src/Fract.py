import math

class Fract:
    def __init__(self, upper, lower=1):
        if lower == 0:
            raise ValueError("Знаменатель не может быть 0!")
        if lower < 0:
            upper = -upper
            lower = -lower
        self.upper = upper
        self.lower = lower
        self.reduce()

    def __str__(self):
        if self.upper % self.lower == 0:
            return str(self.upper // self.lower)
        else:
            return f'({self.upper}/{self.lower})'

    def reduce(self):
        gcd = math.gcd(self.upper, self.lower)
        self.upper //= gcd
        self.lower //= gcd

    def __mul__(self, x):
        if isinstance(x, Fract):
            return Fract(self.upper * x.upper, self.lower * x.lower)
        elif isinstance(x, (int, float)):
            return Fract(self.upper * x, self.lower)
        else:
            raise TypeError("Ошибка умножения дроби!")

    def __truediv__(self, x):
        if isinstance(x, Fract):
            return Fract(self.upper * x.lower, self.lower * x.upper)
        elif isinstance(x, (int, float)):
            return Fract(self.upper, self.lower * x)
        else:
            raise TypeError("Ошибка деления дроби!")

    def __add__(self, x):
        if isinstance(x, Fract):
            new_upper = self.upper * x.lower + x.upper * self.lower
            new_lower = self.lower * x.lower
            return Fract(new_upper, new_lower)
        elif isinstance(x, (int, float)):
            return Fract(self.upper + x * self.lower, self.lower)
        else:
            raise TypeError("Ошибка сложения дробей!")

    def __sub__(self, x):
        if isinstance(x, Fract):
            new_upper = self.upper * x.lower - x.upper * self.lower
            new_lower = self.lower * x.lower
            return Fract(new_upper, new_lower)
        elif isinstance(x, (int, float)):
            return Fract(self.upper - x * self.lower, self.lower)
        else:
            raise TypeError("Ошибка вычитания из дроби!")
    
    def __eq__(self, x):
        if isinstance(x, Fract):
            return self.upper * x.lower == x.upper * self.lower
        elif isinstance(x, (int, float)):
            return self.upper == x * self.lower
        return False

    def __ne__(self, x):
        return not self.__eq__(x)

    def __gt__(self, x):
        if isinstance(x, Fract):
            return self.upper * x.lower > x.upper * self.lower
        elif isinstance(x, (int, float)):
            return self.upper > x * self.lower
        raise TypeError("Ошибка сравнения!")

    def __ge__(self, x):
        if isinstance(x, Fract):
            return self.upper * x.lower >= x.upper * self.lower
        elif isinstance(x, (int, float)):
            return self.upper >= x * self.lower
        raise TypeError("Ошибка сравнения!")

    def __lt__(self, x):
        if isinstance(x, Fract):
            return self.upper * x.lower < x.upper * self.lower
        elif isinstance(x, (int, float)):
            return self.upper < x * self.lower
        raise TypeError("Ошибка сравнения!")

    def __le__(self, x):
        if isinstance(x, Fract):
            return self.upper * x.lower <= x.upper * self.lower
        elif isinstance(x, (int, float)):
            return self.upper <= x * self.lower
        raise TypeError("Ошибка сравнения!")

    def __abs__(self):
        return Fract(abs(self.upper), self.lower)
    
    def __radd__(self, x):
        return self.__add__(x)

    def __rsub__(self, x):
        if isinstance(x, (int, float)):
            return Fract(x * self.lower - self.upper, self.lower)
        else:
            raise TypeError("Ошибка вычитания из дроби!")

    def __rmul__(self, x):
        return self.__mul__(x)

    def __rtruediv__(self, x):
        if isinstance(x, (int, float)):
            return Fract(x * self.lower, self.upper)
        else:
            raise TypeError("Ошибка деления на дробь!")
    def __float__(self):
        return self.upper / self.lower
