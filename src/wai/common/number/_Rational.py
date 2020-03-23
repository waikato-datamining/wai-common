from math import gcd
from numbers import Rational as RationalABC, Integral


class Rational(RationalABC):
    """
    An implementation of rational numbers.
    """
    def __init__(self, numerator: int, denominator: int = 1):
        # Denominator can't be 0
        if denominator == 0:
            raise ValueError("Rational denominator can't be zero")

        # If numerator is 0, denominator is always 1
        if numerator == 0:
            denominator = 1

        # Denominator should always be positive
        if denominator < 0:
            numerator, denominator = -numerator, -denominator

        # Calculate the redundant factor of the numerator and denominator
        redundant_factor = gcd(numerator, denominator)

        self._numerator = numerator // redundant_factor
        self._denominator = denominator // redundant_factor

    @property
    def numerator(self):
        return self._numerator

    @property
    def denominator(self):
        return self._denominator

    def __trunc__(self):
        result = self._numerator // self._denominator
        if self._numerator < 0:
            result += 1
        return result

    def __floor__(self):
        return self._numerator // self._denominator

    def __ceil__(self):
        if self._denominator == 1:
            return self._numerator

        return self.__floor__() + 1

    def __round__(self, ndigits=None):
        raise NotImplementedError(Rational.__round__.__qualname__)

    def __floordiv__(self, other):
        raise NotImplementedError(Rational.__floordiv__.__qualname__)

    def __rfloordiv__(self, other):
        raise NotImplementedError(Rational.__rfloordiv__.__qualname__)

    def __mod__(self, other):
        raise NotImplementedError(Rational.__mod__.__qualname__)

    def __rmod__(self, other):
        raise NotImplementedError(Rational.__rmod__.__qualname__)

    def __lt__(self, other):
        if isinstance(other, RationalABC):
            return (self._numerator * other.denominator) < (self._denominator * other.numerator)

        if isinstance(other, Integral):
            return self._numerator < (other * self._denominator)

        raise NotImplementedError(f"Comparisons between Rational and {type(other).__qualname__}")

    def __le__(self, other):
        return self == other or self < other

    def __add__(self, other):
        if isinstance(other, RationalABC):
            return Rational(self._numerator * other.denominator + self._denominator * other.numerator,
                            self._denominator * other.denominator)

        if isinstance(other, Integral):
            return Rational(self._numerator + self._denominator * other,
                            self._denominator)

        raise NotImplementedError(f"Comparisons between Rational and {type(other).__qualname__}")

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return Rational(-self._numerator, self._denominator)

    def __pos__(self):
        return self

    def __mul__(self, other):
        if isinstance(other, RationalABC):
            return Rational(self._numerator * other.numerator, self._denominator * other.denominator)

        if isinstance(other, Integral):
            return Rational(self._numerator * other, self._denominator)

        raise NotImplementedError(f"Multiplication between Rational and {type(other).__qualname__}")

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        raise NotImplementedError(Rational.__truediv__.__qualname__)

    def __rtruediv__(self, other):
        raise NotImplementedError(Rational.__rtruediv__.__qualname__)

    def __pow__(self, exponent):
        raise NotImplementedError(Rational.__pow__.__qualname__)

    def __rpow__(self, base):
        raise NotImplementedError(Rational.__rpow__.__qualname__)

    def __abs__(self):
        return Rational(abs(self._numerator), self._denominator)

    def __eq__(self, other):
        if isinstance(other, RationalABC):
            return (
                other.numerator == self._numerator
                and (
                    self._numerator == 0
                    or other.denominator == self._denominator
                )
            )

        if isinstance(other, Integral):
            return (
                other == self._numerator
                and self._denominator == 1
            )

        raise NotImplementedError(f"Comparisons between Rational and {type(other).__qualname__}")

    def __hash__(self):
        if self._denominator == 1:
            return hash(self._numerator)

        return hash((self._numerator, self._denominator))

    def __str__(self):
        return f"{self._numerator} / {self._denominator}"
