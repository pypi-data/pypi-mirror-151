"""Complex Numbers class implementation
"""


from copy import deepcopy
from math import acos
from math import cos
from math import pi
from math import sin
from typing import Any
from typing import Union


Number = int | float
Complex_or_Number = Union['ComplexNumber', Number]


class ComplexNumber:
    """ComplexNumber class to perform complex operations.
    """

    def __init__(self, real: Number = 0.0, imag: Number = 0.0) -> None:
        """Initialize a complex number instance with the given real and imag values.

        Args:
            real (Number, optional): The real part. Defaults to 0.0.
            imag (Number, optional): The imaginary part. Defaults to 0.0.
        """
        ComplexNumber.check_isinstance(instance_type=Number, value=real, name="real")
        ComplexNumber.check_isinstance(instance_type=Number, value=imag, name="imag")

        self._real: float = float(real)
        self._imag: float = float(imag)

    @classmethod
    def from_polar(cls, modulus: Number, argument: Number) -> 'ComplexNumber':
        """Initialize a complex number from the polar form.

        Args:
            modulus (Number): The modulus of the complex number in polar form.
            argument (Number): The argument of the complex number in polar form.

        Returns:
            ComplexNumber: ComplexNumber instance.
        """
        cls.check_isinstance(instance_type=Number, value=modulus, name="modulus")
        cls.check_isinstance(instance_type=Number, value=argument, name="argument")
        cls.check_geq(value=modulus, name="modulus")

        real, imag = cls.to_cartesian(modulus, argument)

        return cls(real, imag)

    @property
    def real(self) -> float:
        """Getter for the real part.

        Returns:
            float: Real part.
        """
        return self._real

    @real.setter
    def real(self, real: Number) -> None:
        """Setter for the real part.

        Args:
            real (Number): New real part.
        """
        ComplexNumber.check_isinstance(instance_type=Number, value=real, name="real")
        self._real = float(real)

    @property
    def imag(self) -> float:
        """Getter for the imaginary part.

        Returns:
            float: Imaginary part.
        """
        return self._imag

    @imag.setter
    def imag(self, imag: Number) -> None:
        """Setter for the imaginary part.

        Args:
            imag (Number): New imaginary part.
        """
        ComplexNumber.check_isinstance(instance_type=Number, value=imag, name="imag")
        self._imag = float(imag)

    @property
    def modulus(self) -> float:
        """Getter for the modulus (calculated property).

        Returns:
            float: Modulus.
        """
        modulus = (self.real**2 + self.imag**2) ** 0.5
        return modulus

    @modulus.setter
    def modulus(self, modulus: Number) -> None:
        """Setter for the modulus.

        Args:
            modulus (Number): New modulus.
        """
        ComplexNumber.check_isinstance(instance_type=Number, value=modulus, name="modulus")
        ComplexNumber.check_gt(value=modulus, name="modulus")
        argument = self.argument
        real, imag = ComplexNumber.to_cartesian(modulus, argument)
        self.real = real
        self.imag = imag

    @property
    def argument(self) -> float:
        """Getter for the argument (calculated property).

        Returns:
            float: The argument.
        """
        modulus = self.modulus
        ComplexNumber.check_gt(value=modulus, name="modulus")
        argument = acos(self.real / modulus)

        if self.real < 0 and self.imag < 0:
            argument += pi / 2
        elif self.real == 0 and self.imag < 0:
            argument += pi
        elif self.real > 0 and self.imag < 0:
            argument += 1.5 * pi
        else:
            pass

        return argument

    @argument.setter
    def argument(self, argument: Number) -> None:
        """Setter for the argument.

        Args:
            argument (Number): The new argument.
        """
        ComplexNumber.check_isinstance(instance_type=Number, value=argument, name="argument")
        modulus = self.modulus
        real, imag = ComplexNumber.to_cartesian(modulus, argument)
        self.real = real
        self.imag = imag

    def __repr__(self) -> str:
        """Return the complex number instance representation.

        Returns:
            str: The representation of the complex number instance.
        """
        return f"{self._real:.4f}{self._imag:+.4f}i"  # 4 decimal places

    def __str__(self, precision: int = 2) -> str:
        """The complex number instance as a string.

        Args:
            precision (int, optional): Set number of decimal places. Defaults to 2.

        Returns:
            str: The complex number instance as a string.
        """
        ComplexNumber.check_isinstance(instance_type=int, value=precision, name="precision")
        return f"{self.real:.{precision}f}{self.imag:+.{precision}f}i"

    def print(self, precision: int = 2) -> str:
        """A more user friendly alternative to set the number of decimal places instead of using
        __str__(...)

        Args:
            precision (int, optional): Set number of decimal places. Defaults to 2.
        """

        print(self.__str__(precision))

    def __add__(self, other: Complex_or_Number) -> 'ComplexNumber':
        """Adds to a complex number another number or complex number.

        Args:
            other (Complex_or_Number): Number or complex number.

        Returns:
            ComplexNumber: The addition result as complex number instance.
        """
        ComplexNumber.check_isinstance(instance_type=(
            ComplexNumber, Number), value=other, name="other")
        if ComplexNumber.is_number(other):
            other = ComplexNumber(real=other)
        real = self.real + other.real
        imag = self.imag + other.imag
        return ComplexNumber(real, imag)

    def __iadd__(self, other: Complex_or_Number) -> 'ComplexNumber':
        return self.__add__(other)

    def __sub__(self, other: Complex_or_Number) -> 'ComplexNumber':
        """Subtracts from a complex number another number or complex number.

        Args:
            other (Complex_or_Number): Number or complex number.

        Returns:
            ComplexNumber: The subtraction result as complex number instance.
        """
        ComplexNumber.check_isinstance(instance_type=(
            ComplexNumber, Number), value=other, name="other")
        if ComplexNumber.is_number(other):
            other = ComplexNumber(real=other)
        real = self.real - other.real
        imag = self.imag - other.imag
        return ComplexNumber(real, imag)

    def __isub__(self, other: Complex_or_Number) -> 'ComplexNumber':
        return self.__sub__(other)

    def __mul__(self, other: Complex_or_Number) -> 'ComplexNumber':
        """Multiplies to a complex number another number or complex number.

        Args:
            other (Complex_or_Number): Number or complex number.

        Returns:
            ComplexNumber: The multiplication result as complex number instance.
        """
        ComplexNumber.check_isinstance(instance_type=(
            ComplexNumber, Number), value=other, name="other")
        if ComplexNumber.is_number(other):
            other = ComplexNumber(real=other)
        modulus1, argument1 = self.modulus, self.argument
        modulus2, argument2 = other.modulus, other.argument

        modulus = modulus1 * modulus2
        argument = argument1 + argument2
        real, imag = ComplexNumber.to_cartesian(modulus, argument)
        return ComplexNumber(real, imag)

    def __imul__(self, other: Complex_or_Number) -> 'ComplexNumber':
        return self.__mul__(other)

    def __truediv__(self, other: Complex_or_Number) -> 'ComplexNumber':
        """Divides a complex number by another number or complex number.

        Args:
            other (Complex_or_Number): Number or complex number.

        Raises:
            ZeroDivisionError: If other is a number and is equal to 0.
            ZeroDivisionError: If other is a complex number and its modulus is equal to 0.
            SystemError: Should never happen. If it does, then some unwanted case is not being
            catched.

        Returns:
            ComplexNumber: The division result as a complex number instance.
        """
        ComplexNumber.check_isinstance(instance_type=(
            ComplexNumber, Number), value=other, name="other")
        if ComplexNumber.is_number(other):
            if other == 0:
                raise ZeroDivisionError("You cannot divide by 0.")
            other = ComplexNumber(real=other)
        elif other.modulus == 0:
            raise ZeroDivisionError("You cannot divide by 0.")
        else:
            pass

        modulus1, argument1 = self.modulus, self.argument
        modulus2, argument2 = other.modulus, other.argument

        modulus = modulus1 / modulus2
        argument = argument1 - argument2
        real, imag = ComplexNumber.to_cartesian(modulus, argument)
        return ComplexNumber(real, imag)

    def __itruediv__(self, other: Complex_or_Number) -> 'ComplexNumber':
        return self.__truediv__(other)

    def __pow__(self, exponent: Number) -> 'ComplexNumber':
        """Raises a complex number to the power of the exponent.

        Args:
            exponent (Number): The exponent.

        Returns:
            ComplexNumber: The result of raising the complex number instance to the power of the
            exponent.
        """
        ComplexNumber.check_isinstance(instance_type=Number, value=exponent, name="exponent")
        modulus, argument = self.modulus, self.argument
        result_modulus, result_argument = modulus**exponent, argument * abs(exponent)
        if exponent < 0:
            result_argument = -result_argument

        real, imag = ComplexNumber.to_cartesian(result_modulus, result_argument)
        return ComplexNumber(real, imag)

    def __ipow__(self, other: Number) -> 'ComplexNumber':
        return self.__pow__(other)

    def root(self, index: int = 2) -> tuple:
        """Calculates all solutions of taking the root with the index (whole number).

        Args:
            index (int, optional): The index of the root. Defaults to 2.

        Returns:
            tuple: Tuple of all solutions as complex number instances.
        """
        ComplexNumber.check_isinstance(instance_type=int, value=index, name="index")
        results = []
        first = self ** (1 / index)
        results.append(first)

        modulus = first.modulus
        argument = first.argument
        k = 2 * pi / index
        for i in range(1, index):
            complex_number = ComplexNumber.from_polar(modulus, argument + i * k)
            results.append(complex_number)

        return tuple(results)

    def __eq__(self, other: 'ComplexNumber') -> bool:
        """Checks whether the real parts and the imaginary parts are equal.

        Args:
            other (ComplexNumber): Other complex number instance.

        Raises:
            NotImplementedError: If other is not a complex number instance.

        Returns:
            bool: True, if real parts and imaginary parts are equal.
        """
        if other.__class__ is self.__class__:
            return (self.real, self.imag) == (other.real, other.imag)
        raise NotImplementedError

    def __pos__(self) -> 'ComplexNumber':
        return self

    def __neg__(self) -> 'ComplexNumber':
        copy = deepcopy(self)
        copy.real = -copy.real
        copy.imag = -copy.imag
        return copy

    def conjugate(self) -> 'ComplexNumber':
        """Returns conjugated complex number instance.

        Returns:
            ComplexNumber: conjugated complex number instance.
        """
        copy = deepcopy(self)
        real = copy.real
        imag = -copy.imag
        return ComplexNumber(real, imag)

    def polar(self) -> dict[str, float]:
        """Return the polar form of the complex number instance in a dictionary.

        Returns:
            dict[str, float]: {"modulus": modulus, "argument": argument}
        """
        return {"modulus": self.modulus, "argument": self.argument}

    def print_polar(self, precision: int = 2) -> None:
        """Print the polar form to the console.

        Args:
            precision (int, optional): Set number of decimal places. Defaults to 2.
        """
        ComplexNumber.check_isinstance(instance_type=int, value=precision, name="precision")
        modulus, argument = self.modulus, self.argument
        print(f"{modulus:.{precision}f} cis({(argument/pi):.{precision}f} π)")

    @staticmethod
    def to_cartesian(modulus: Number, argument: Number) -> tuple[float, float]:
        """Calculates the real part and imaginary part from the polar form.

        Args:
            modulus (Number): Modulus
            argument (Number): Argument

        Returns:
            tuple[float, float]: Tuple of real part and imaginary part
        """
        real = modulus * cos(argument)
        imag = modulus * sin(argument)
        return (real, imag)

    @staticmethod
    def check_isinstance(*, instance_type: Any, value: Any, name: str) -> None | bool:
        """Checks if value is an instance of type instance_type. If not a TypeError is raised.

        Args:
            instance_type (Any): The class(es) to check for.
            value (Any): The value to check.
            name (str): The variable name of the originally passed in argument for the error
            message.

        Raises:
            TypeError: If value is not an instance of instance_type.

        Returns:
            None | bool: True if check successfully passed.
        """
        if not isinstance(value, instance_type):
            raise TypeError(f"{name} must be of type {instance_type}.")
        return True

    @staticmethod
    def is_number(value: Any) -> bool:
        """Checks if value is a number.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if value is a number. False if value is not a number.
        """
        return isinstance(value, Number)

    @staticmethod
    def check_geq(*, compare_value: Number = 0, value: Number, name: str) -> None | bool:
        """Checks if value is greater or equal to compare_value. If not a ValueError is raised.

        Args:
            value (Number): The value to check.
            name (str): The variable name of the originally passed in argument for the error
            message.
            compare_value (Number, optional): The value to compare against. Defaults to 0.

        Raises:
            ValueError: If the check fails.

        Returns:
            None | bool: True if the check passed successfully.
        """
        if not value >= compare_value:
            raise ValueError(f"{name} must be greater than {compare_value}.")
        return True

    @staticmethod
    def check_gt(*, compare_value: Number = 0, value: Number, name: str) -> None | bool:
        """Checks of value is greater than compare_value. If not a ValueError is raised.

        Args:
            value (Number): The value to check.
            name (str): The variable name of the originally passed in argument for the error
            message.
            compare_value (Number, optional): The value to compare against. Defaults to 0.

        Raises:
            ValueError: If the check fails.

        Returns:
            None | bool: True if the check passed successfully.
        """
        if not value > compare_value:
            raise ValueError(f"{name} must be greater than {compare_value}.")
        return True
