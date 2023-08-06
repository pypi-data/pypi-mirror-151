from typing import Any, Tuple, Union

from openpyxl.cell.read_only import EmptyCell  # type: ignore


class CellContentValidator:
    """
    Check the content of a given cell in the worksheet.
    Returns cell value after validation, validation state and
    optionally reason for validation fail
    """

    def validate(self, cell, value) -> Tuple[Any, bool, Union[str, None]]:
        """
        The "validate" function of subclasses ought to take
        a cell and a value (usually this will be equal to 'cell.value' but
        chained validators may alter this)
        """
        if True:
            message = None
            validated = True
            return value, validated, message


class NotNullCellValidator(CellContentValidator):
    """
    Return False if a cell is an EmptyCell object
    or if it's an empty string, or None value
    """

    def validate(self, cell, value) -> Tuple[Any, bool, Union[str, None]]:
        message = "This cell requires a value"
        if (
            isinstance(cell, EmptyCell)
            or not value
            or value == ""
            or (hasattr(value, "strip") and value.strip() == "")
        ):
            return value, False, message
        return value, True, None


class IsIntegerValidator(CellContentValidator):
    def validate(self, cell, value) -> Tuple[Any, bool, Union[str, None]]:
        if isinstance(value, int):
            return value, True, None
        else:
            return value, False, "This value should be an integer"


class IsNumericValidator(CellContentValidator):
    """
    Value is a float or int
    """

    def validate(self, cell, value) -> Tuple[Any, bool, Union[str, None]]:
        if isinstance(value, int) or isinstance(value, float):
            return value, True, None
        else:
            return value, False, "This value should be a number"


class MaxNumberValidator(CellContentValidator):
    def __init__(self, val: int):
        self.val = val  # type: int

    def validate(self, cell, value) -> Tuple[Any, bool, Union[str, None]]:
        if isinstance(value, int) and value <= self.val:
            return value, True, None
        else:
            return value, False, f"This value should be less than {self.val}"


class MinNumberValidator(CellContentValidator):
    def __init__(self, val: int):
        self.val = val  # type: int

    def validate(self, cell, value):
        if isinstance(value, int) and cell.value >= self.val:
            return value, True, None
        else:
            return value, False, f"This value should be more than {self.val}"
