import logging
from pathlib import Path
from typing import Dict, Iterator, Optional, Tuple, Type, Union

from openpyxl import Workbook, load_workbook

from .definitions import EXCEPTION_HANDLING, SheetDefinition

logger = logging.getLogger(__name__)


class WorkbookValidator:
    sheet_definition_classes = {}  # type: Dict[str, Type[SheetDefinition]]

    on_workbook_alias = EXCEPTION_HANDLING.DoNothing
    on_column_alias = EXCEPTION_HANDLING.DoNothing

    def __init__(self, workbook: Union[Workbook, str, Path]):
        """
        Assign the workbook (or open the workbook if str or Path)
        to the created instance and make the 'sheet definitions'
        instances of the classes included in the definition of
        this subclass of WorkbookValidator

        Args:
            workbook (Union[Workbook, str, Path]): the workbook to use for source data
        """
        self.workbook = (
            workbook
            if isinstance(workbook, Workbook)
            else load_workbook(filename=workbook, read_only=True)
        )
        # Sheet definitions are instances of the classes referenced above
        self.sheet_definitions = {
            label: klass(self.workbook, on_column_alias=EXCEPTION_HANDLING.Warn)
            for label, klass in self.sheet_definition_classes.items()
        }

    def validate(self) -> Iterator[Tuple[str, SheetDefinition, Optional[Exception]]]:
        """
        Yields the sheets in the workbook
        """
        for sheet, defn in self.sheet_definitions.items():
            validated_defn, execption = defn.validate()
            yield sheet, validated_defn, execption
