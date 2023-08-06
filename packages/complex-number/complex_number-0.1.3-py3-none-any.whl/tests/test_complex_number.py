"""Test Complex Number."""

import unittest
from math import atan
from math import pi

from complex_number import ComplexNumber


class ComplexNumberTests(unittest.TestCase):
    def setUp(self) -> None:
        self.z1 = ComplexNumber(0, 0)
        self.z2 = ComplexNumber(1, 1)
        self.z3 = ComplexNumber(-1, -1)
        self.z4 = ComplexNumber(2, 3)
        self.z5 = ComplexNumber(0, -3)
        self.z6 = ComplexNumber(0, 2)
        self.z7 = ComplexNumber(2, -2)
        self.z8 = ComplexNumber()

    def test_init(self) -> None:
        """Test the __init__ method."""
        self.assertEqual(self.z1._real, 0)
        self.assertEqual(self.z1._imag, 0)
        self.assertEqual(self.z8._real, 0)
        self.assertEqual(self.z8._imag, 0)
        self.assertEqual(self.z2._real, 1)
        self.assertEqual(self.z2._imag, 1)
        with self.assertRaises(TypeError):
            ComplexNumber("a", "b")

    # from_polar

    def test_real_getter(self) -> None:
        """Test the real property getter."""
        self.assertEqual(self.z1.real, 0)
        self.assertEqual(self.z2.real, 1)
        self.assertEqual(self.z3.real, -1)

    def test_real_setter(self) -> None:
        """Test the real property setter."""
        self.z1.real = 2
        expected_result = ComplexNumber(2, 0)
        self.assertEqual(self.z1, expected_result)

    def test_imag_getter(self) -> None:
        """Test the imag property getter."""
        self.assertEqual(self.z1.imag, 0)
        self.assertEqual(self.z2.imag, 1)
        self.assertEqual(self.z3.imag, -1)

    def test_imag_setter(self) -> None:
        """Test the imag property setter."""
        self.z1.imag = 2
        expected_result = ComplexNumber(0, 2)
        self.assertEqual(self.z1, expected_result)

    def test_modulus_getter(self) -> None:
        """Test the modulus property getter."""
        self.assertEqual(self.z1.modulus, 0)
        self.assertEqual(self.z2.modulus, 2**0.5)
        self.assertEqual(self.z3.modulus, 2**0.5)
        self.assertEqual(self.z4.modulus, 13**0.5)

    def test_modulus_setter(self) -> None:
        """Test the modulus property setter."""
        self.z2.modulus = 5
        expected_result = 5
        self.assertEqual(self.z2.modulus, expected_result)
        with self.assertRaises(ValueError):
            self.z3.modulus = -2

    def test_argument_getter(self) -> None:
        """Test the argument property getter."""
        with self.assertRaises(ValueError):
            self.z1.argument
        self.assertAlmostEqual(self.z2.argument, pi / 4)
        self.assertAlmostEqual(self.z3.argument, 1.25 * pi)
        self.assertAlmostEqual(self.z4.argument, atan(3 / 2))
        self.assertAlmostEqual(self.z5.argument, 1.5 * pi)
        self.assertAlmostEqual(self.z7.argument, 1.75 * pi)

    def test_argument_setter(self) -> None:
        """Test the argument property setter."""
        self.z2.argument = pi
        expected_result = pi
        self.assertEqual(self.z2.argument, expected_result)
        self.z3.argument = pi
        expected_result_2 = ComplexNumber.from_polar(2**0.5, pi)
        self.assertAlmostEqual(self.z3, expected_result_2)

    def test_print(self) -> None:
        """Test the print method."""
        self.assertEqual(self.z2.print(), self.z2.print())

    def test_add(self) -> None:
        """Test the __add__ method."""
        result = self.z1 + self.z2
        expected_result = ComplexNumber(1, 1)
        self.assertAlmostEqual(result, expected_result)

    def test_iadd(self) -> None:
        """Test the __iadd__ method."""
        self.z1 += self.z2
        expected_result = ComplexNumber(1, 1)
        self.assertAlmostEqual(self.z1, expected_result)

    def test_sub(self) -> None:
        """Test the __sub__ method."""
        result = self.z1 - self.z2
        expected_result = ComplexNumber(-1, -1)
        self.assertAlmostEqual(result, expected_result)

    def test_isub(self) -> None:
        """Test the __isub__ method."""
        self.z1 -= self.z2
        expected_result = ComplexNumber(-1, -1)
        self.assertAlmostEqual(self.z1, expected_result)

    def test_mul(self) -> None:
        """Test the __mul__ method."""
        result = self.z2 * self.z3
        expected_result = ComplexNumber(0, -2)
        self.assertAlmostEqual(result.real, expected_result.real)
        self.assertAlmostEqual(result.imag, expected_result.imag)

    def test_imul(self) -> None:
        """Test the __imul__ method."""
        self.z2 *= self.z3
        expected_result = ComplexNumber(0, -2)
        self.assertAlmostEqual(self.z2.real, expected_result.real)
        self.assertAlmostEqual(self.z2.imag, expected_result.imag)

    def test_truediv(self) -> None:
        """Test the __truediv__ method."""
        result = self.z2 / self.z3
        expected_result = ComplexNumber(-1, 0)
        self.assertAlmostEqual(result.real, expected_result.real)
        self.assertAlmostEqual(result.imag, expected_result.imag)
        result2 = self.z2 / 2
        expected_result2 = ComplexNumber(0.5, 0.5)
        self.assertAlmostEqual(result2.real, expected_result2.real)
        self.assertAlmostEqual(result2.imag, expected_result2.imag)
        with self.assertRaises(ZeroDivisionError):
            self.z2 / 0
        with self.assertRaises(ZeroDivisionError):
            self.z2 / ComplexNumber(0, 0)

    def test_itruediv(self) -> None:
        """Test the __itruediv__ method."""
        self.z2 /= self.z3
        expected_result = ComplexNumber(-1, 0)
        self.assertAlmostEqual(self.z2.real, expected_result.real)
        self.assertAlmostEqual(self.z2.imag, expected_result.imag)

    def test_pow(self) -> None:
        """Test the __pow__ method."""
        result = self.z2 ** 2
        expected_result = ComplexNumber(0, 2)
        self.assertAlmostEqual(result.real, expected_result.real)
        self.assertAlmostEqual(result.imag, expected_result.imag)

        result2 = self.z2 ** -2
        expected_result2 = ComplexNumber(0, -0.5)
        self.assertAlmostEqual(result2.real, expected_result2.real)
        self.assertAlmostEqual(result2.imag, expected_result2.imag)

    def test_ipow(self) -> None:
        """Test the __ipow__ method."""
        self.z2 **= 2
        expected_result = ComplexNumber(0, 2)
        self.assertAlmostEqual(self.z2.real, expected_result.real)
        self.assertAlmostEqual(self.z2.imag, expected_result.imag)

    def test_root(self) -> None:
        """Test the root method."""
        result1, result2 = self.z6.root()
        expected_result1, expected_result2 = (ComplexNumber(1, 1), ComplexNumber(-1, -1))
        self.assertAlmostEqual(result1.real, expected_result1.real)
        self.assertAlmostEqual(result1.imag, expected_result1.imag)
        self.assertAlmostEqual(result2.real, expected_result2.real)
        self.assertAlmostEqual(result2.imag, expected_result2.imag)

    def test_eq(self) -> None:
        """Test the __eq__ method."""
        self.assertTrue(self.z1, self.z1)
        self.assertTrue(self.z2, self.z2)
        with self.assertRaises(NotImplementedError):
            self.z1 == 3

    def test_pos(self) -> None:
        """Test the __pos__ method."""
        self.assertEqual(+self.z1, self.z1)
        self.assertEqual(+self.z2, self.z2)

    def test_neg(self) -> None:
        """Test the __neg__ method."""
        self.assertEqual(-self.z1, ComplexNumber(0, 0))
        self.assertEqual(-self.z2, ComplexNumber(-1, -1))

    def test_conjugate(self) -> None:
        """Test the conjugate method."""
        self.assertEqual(self.z2.conjugate(), ComplexNumber(1, -1))

    def test_polar(self) -> None:
        """Test the polar method."""
        result = self.z2.polar()
        expected_result = {"modulus": 2 ** 0.5, "argument": pi / 4}
        self.assertEqual(result["modulus"], expected_result["modulus"])
        self.assertAlmostEqual(result["argument"], expected_result["argument"])

    def test_to_cartesian(self) -> None:
        """Test the to_cartesian staticmethod."""
        result_real, result_imag = ComplexNumber.to_cartesian(2 ** 0.5, pi / 4)
        expected_real, expected_imag = 1.0, 1.0
        self.assertAlmostEqual(result_real, expected_real)
        self.assertAlmostEqual(result_imag, expected_imag)

    def test_check_isinstance(self) -> None:
        """Test the check_isinstance staticmethod"""
        self.assertTrue(ComplexNumber.check_isinstance(
            instance_type=ComplexNumber, value=self.z2, name="self.z2"))

        with self.assertRaises(TypeError):
            ComplexNumber.check_isinstance(
                instance_type=int, value=self.z2, name="self.z2")

    def test_is_number(self) -> None:
        """Test the is_number staticmethod"""
        self.assertTrue(ComplexNumber.is_number(5))
        self.assertTrue(ComplexNumber.is_number(-5))
        self.assertTrue(ComplexNumber.is_number(5.0))
        self.assertTrue(ComplexNumber.is_number(-5.0))

        self.assertFalse(ComplexNumber.is_number("5"))

    def test_check_geq(self) -> None:
        """Test the check_geq staticmethod"""
        self.assertTrue(ComplexNumber.check_geq(value=0, name="0"))
        self.assertTrue(ComplexNumber.check_geq(value=2, name="2"))

        with self.assertRaises(ValueError):
            ComplexNumber.check_geq(value=-2, name="-2")

    def test_check_gt(self) -> None:
        """Test the check_geq staticmethod"""
        self.assertTrue(ComplexNumber.check_gt(value=0.1, name="0"))
        self.assertTrue(ComplexNumber.check_gt(value=2, name="2"))

        with self.assertRaises(ValueError):
            ComplexNumber.check_gt(value=0, name="0")
