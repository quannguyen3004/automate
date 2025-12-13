import pytest
from PDA import PDA


@pytest.fixture()
def pda():
    return PDA()


def test_infix_to_postfix_basic(pda):
    assert pda.infix_to_postfix('(a+b)*c') == 'a b + c *'


def test_infix_with_negative_number(pda):
    assert pda.infix_to_postfix('-3+4') == '-3 4 +'


def test_unary_minus_and_recognition(pda):
    assert pda.recognize_infix('-3+4') is True


def test_postfix_recognition_binary(pda):
    # (3+4)*2 -> 3 4 + 2 *
    assert pda.recognize_postfix('3 4 + 2 *') is True


def test_postfix_recognition_reject(pda):
    assert pda.recognize_postfix('3 +') is False


def test_function_support(pda):
    # sin(x) -> x sin
    postfix = pda.infix_to_postfix('sin(x)')
    assert postfix == 'x sin'
    assert pda.recognize_postfix(postfix) is True


def test_complex_expression_with_power(pda):
    # (a+b)^2 -> a b + 2 ^
    postfix = pda.infix_to_postfix('(a+b)^2')
    assert postfix == 'a b + 2 ^'
    assert pda.recognize_postfix(postfix) is True


def test_decimal_numbers(pda):
    # 3.14 * 2 -> 3.14 2 *
    postfix = pda.infix_to_postfix('3.14*2')
    assert postfix == '3.14 2 *'
    assert pda.recognize_postfix(postfix) is True


def test_multiple_functions(pda):
    # sin(x) + cos(y) -> x sin y cos +
    postfix = pda.infix_to_postfix('sin(x)+cos(y)')
    assert postfix == 'x sin y cos +'
    assert pda.recognize_postfix(postfix) is True


def test_invalid_infix_mismatched_parens(pda):
    # ((a+b)*c -> mismatched parentheses
    try:
        pda.infix_to_postfix('((a+b)*c')
        assert False, "Should raise ValueError"
    except ValueError:
        assert True


def test_postfix_insufficient_operands(pda):
    # a + b + (not enough operands before last +)
    assert pda.recognize_postfix('a +') is False


def test_postfix_extra_operands(pda):
    # a b (extra operand at end)
    assert pda.recognize_postfix('a b') is False


def test_negative_in_expression(pda):
    # -5 * (3+2) -> -5 3 2 + *
    postfix = pda.infix_to_postfix('-5*(3+2)')
    assert postfix == '-5 3 2 + *'
    assert pda.recognize_postfix(postfix) is True
