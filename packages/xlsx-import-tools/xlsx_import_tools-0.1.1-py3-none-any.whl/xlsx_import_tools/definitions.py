from __future__ import annotations

import enum
import itertools
import logging
from collections import defaultdict
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union

from openpyxl.cell.cell import Cell
from openpyxl.cell.read_only import EmptyCell  # type: ignore
from openpyxl.workbook.workbook import Workbook

from .validators import NotNullCellValidator

logger = logging.getLogger(__name__)

# Several class methods use a common format for output messages
Messages = Dict[str, List[str]]  # A type alias for list of 'messages'
ErrorMessages = Messages
WarningMessages = Messages
InfoMessages = Messages

WorksheetRange = Tuple[Tuple[Cell]]
StringCellMap = Dict[
    str, Optional[Cell]
]  # A type alias for 'this string matched this cell' mapping eg column headers


class CellNotFoundError(Exception):
    """
    Raised when a cell of value "something" is not found
    """

    pass


class SheetNotFoundError(Exception):
    pass


class HeaderCollisionError(Exception):
    """
    A header collision occurs when two headers "match"
    i.e. "Cheque Value" and "Cheque" (for number)
    """

    pass


class HeaderNotFoundError(CellNotFoundError):
    """
    Raised when a header is not present in the workbook
    """

    pass


class SheetNotFound(Exception):
    """
    Raised when a sheet is not present in the workbook
    """

    pass


def worksheetrange_asdict(r: WorksheetRange) -> Dict[str, str]:
    """
    Return the
    """
    cells = {}
    for row in r:
        for cell in row:
            try:
                if cell.value:
                    cells[cell.coordinate] = cell.value
            except AttributeError:
                pass
    return cells


class Compar:
    """
    A namespace for some simple functions to
    match different values
    """

    @staticmethod
    def clean_value(value):
        """
        Strip whitespace and lower
        """
        if not value:
            return False
        return f"{value}".strip().lower()

    @staticmethod
    def exact(value, try_content) -> bool:
        if not value and try_content:
            return False
        try:
            return Compar.clean_value(value) == Compar.clean_value(try_content)
        except AttributeError as E:
            logger.debug(f"{E}")
            return False

    @staticmethod
    def startswith(value, try_content) -> bool:
        if not value and try_content:
            return False
        try:
            a, b = Compar.clean_value(value), Compar.clean_value(try_content)
            return (
                hasattr(a, "startswith")
                and hasattr(b, "startswith")
                and (a.startswith(b) or b.startswith(a))
            )
        except (AttributeError, TypeError) as E:
            logger.debug(f"{E}")
            return False


class EXCEPTION_HANDLING(enum.Enum):
    """
    Handling values for particular cases
    to determinw how "strict" to be when handling errors
    """

    DoNothing = 1
    # Info = 2
    Warn = 3
    Err = 4


class ColumnDefinition:
    """
    Define a Column with whether it is required or not
    and the name(s) it may take
    """

    required = False
    aliases = tuple()  # type: Tuple[str, ...]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators = []


class RequiredColumnDefinition(ColumnDefinition):
    required = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(NotNullCellValidator())


class ValueColumnDef(RequiredColumnDefinition):
    """
    Not strictly a part of "Generic", this DIRD flavoured definition
    is used in a default locator for set of headers
    """

    aliases = ("Cheque Value", "Project Value")


class SheetDefinition:
    """
    Validate that a given worksheet has columns as
    specified
    """

    required = True
    # aliases is a list of names the worksheet may take
    aliases = []  # type: Iterable[str]
    column_definitions = {}  # type: Dict[str, ColumnDefinition]

    def __init__(self, workbook, *args, **kwargs):
        self.workbook = workbook  # type: Workbook

        # By default the column headers will be detected
        # from a cell in the 'header_search' range containing a match to one
        # of the aliases of a column definition

        self.header_search = kwargs.get(
            "header_search", "A1:P20"
        )  # The cells to search for the header value
        self.header_definition = kwargs.get(
            "header_definition", ValueColumnDef()
        )  # type: ColumnDefinition

        # The limits of where we expect to find headers
        self.header_coordinates_start_row = (
            "A"  # Assuming that we start at the first column
        )
        self.header_coordinates_end_row = (
            "AA"  # Assuming that we have max ~25 columns of data
        )
        self.header_coordinates_nrows = 1  # Tweak to search for "merged" cells etc

        self.on_column_alias = kwargs.get(
            "on_column_alias", None
        )  # Declare action to take when a column uses an unexepected 'alias'
        # Track the errors / warnings encountered along the way
        self.errors = defaultdict(list)  # type: ErrorMessages
        self.warnings_ = defaultdict(list)  # type: WarningMessages
        self.info = defaultdict(list)  # type: InfoMessages

        # Header columns is an expensive property
        # cached here
        self._sheet = None  # Cached version of property "sheet"
        self._headers_range = None
        self._header_columns = None  # type: Optional[StringCellMap]
        self._header_row = None
        self._sheet_range = None

        self._first_value_row = None
        self._last_value_row = None

    @property
    def header_coordinates(self) -> str:
        return f"{self.header_coordinates_start_row}{self.header_row.row}:{self.header_coordinates_end_row}{self.header_row.row + self.header_coordinates_nrows}"

    @property
    def data_header_coordinates(
        self,
    ) -> Tuple[Union[str, Exception], Union[str, Exception]]:
        """
        Finds the coordinates which will be used to extract
        data from.
        """
        hcols = self.header_columns.values()
        min_col = min([n.column_letter for n in hcols])
        max_col = max([n.column_letter for n in hcols])
        try:
            min_hrow = min([n.row for n in hcols])
            max_hrow = max([n.row for n in hcols])
            header = (
                f"{min_col}{min_hrow}:{max_col}{max_hrow}"
            )  # type: Union[str, Exception]
        except CellNotFoundError as E:
            header = E

        try:
            min_row = self.find_first_value_row().row
            max_row = self.find_last_value_row().row
            data = (
                f"{min_col}{min_row}:{max_col}{max_row}"
            )  # type: Union[str, Exception]
        except CellNotFoundError as E:
            data = E

        return header, data

    @property
    def sheet(self):
        """
        Return the first sheet matching 'aliases' from the workbook
        """
        if self._sheet:
            return self._sheet
        present = set(self.workbook.sheetnames)
        matched_sheets = list(present.intersection(self.aliases))

        # Use the first alias to refer to this
        # particular sheet for error reporting
        required_sheet = self.aliases[0]
        logger.debug("WorkbookValidator.validate searching: %s", required_sheet)
        if len(matched_sheets) == 0 and self.required:
            raise SheetNotFoundError(
                "No sheet for %s in workbook. Permitted names are %s"
                % (required_sheet, ", ".join(self.aliases))
            )
        elif len(matched_sheets) > 1:
            self.errors[required_sheet].append(
                f"Multiple sheets for {required_sheet} in workbook. Permitted names are {self.aliases}"
            )
        else:
            assert len(matched_sheets) == 1
            self.info[required_sheet].append(
                f"Successfully located a header for {required_sheet}"
            )
        self._sheet = self.workbook[matched_sheets[0]]
        return self._sheet

    @property
    def header_row(self):
        if not self._header_row:
            if not self.sheet:
                raise TypeError
            self._header_row = find_value(
                cells=self.sheet[self.header_search],
                try_content=self.header_definition.aliases,
            )
            if not self._header_row:
                raise HeaderNotFoundError(
                    "No header from %s found in range %s",
                    self.header_definition.aliases,
                    self.header_search,
                )
        return self._header_row

    def find_first_value_row(self) -> Cell:
        """
        The first row containing values
        From the "header row", start searching downwards until we find a cell with a value
        value_column is a historical throwback, it's more like a "Primary key" which must
        exist to identify and import a valid row
        """

        if self._first_value_row:
            return self._first_value_row

        if not self.sheet and self.header_row:
            raise CellNotFoundError("This sheet appears to have no rows to import")

        assert hasattr(self.header_row, "row")  # Expect the header to be a cell
        value_column = self.header_row
        assert value_column
        for r in range(1, 5):
            # Try the row directly below header row, and
            # a few more rows in case of "Kundiawa Gembogl 2013" bug: merged A11 & A12
            cell_ref = "{}{}".format(value_column.column_letter, value_column.row + r)
            cell = self.sheet[cell_ref]  # type: Any
            if cell.value:
                self._first_value_row = cell
                return cell
        raise CellNotFoundError("This sheet appears to have no rows to import")

    def find_last_value_row(
        self,
        start_search: int = 1,
        search_depth: int = 100,
        allow_empty_rows: int = 2,
    ) -> Optional[Cell]:
        """
        The last row before you hit the expanse of dead space
        """

        def last_populated_cell(
            cells, last_cell: Optional[Cell] = None
        ) -> Tuple[Optional[Cell], bool]:
            if not cells:
                return None, True
            empty_cells_seen = 0
            for row in cells:
                for cell in row:
                    if (
                        isinstance(cell, EmptyCell)
                        or cell.value is None
                        or (hasattr(cell.value, "strip") and not cell.value.strip())
                    ):
                        # Covers the case where the cell is a special empty XML value
                        # missing entirely is different to being blank
                        empty_cells_seen += 1
                    else:
                        empty_cells_seen = 0
                        # Break if we hit a formula
                        if hasattr(cell.value, "startswith") and cell.value.startswith(
                            "="
                        ):
                            return last_cell, True
                        last_cell = cell

                    if empty_cells_seen > allow_empty_rows:
                        return last_cell, True
            if not last_cell:
                raise CellNotFoundError(
                    "Could not identify the last row to import from this sheet"
                )
            return last_cell, False

        if self._last_value_row:
            return self._last_value_row

        if not self.sheet:
            raise AttributeError(
                "No sheet in the workbook with one of the following names: %s",
                ", ".join(self.aliases),
            )

        first_value_row = self.find_first_value_row()
        value_column = self.header_row
        last_cell = first_value_row
        search_complete = False
        while not search_complete:
            search_cells = f"{value_column.column_letter}{first_value_row.row + start_search}:{value_column.column_letter}{first_value_row.row + start_search + search_depth}"  # type: ignore
            sheet_search_cells = self.sheet[search_cells]
            if not sheet_search_cells:
                # When all search_cells are empty you will get a
                # truncated list of cells
                return last_cell
            last_cell, search_complete = last_populated_cell(
                sheet_search_cells, last_cell
            )
            start_search += 100
        self._last_value_row = last_cell
        return last_cell

    @property
    def header_columns(self):
        """
        Get the header definitions for the columns
        """

        def header_column_handler(header_cell, column_defn):
            if header_cell is None and column_defn.required:
                msg = f"No header column identified in sheet for {column_ref}. Allowed values are {column_defn.aliases}"
                self.errors[column_ref].append(msg)
                return

            elif header_cell is None:
                msg = f"An optional header was not identified in sheet for {column_ref}"
                self.info[column_ref].append(msg)
                return

            else:
                msg = f'Header identified in sheet for {column_ref}, "{header_cell.value}" at {header_cell.row}{header_cell.column_letter}'
                self.info[column_ref].append(msg)

            if header_cell.value != column_defn.aliases[0]:
                # Take some action if cell column is not the first
                # option for an alias
                alias_msg = f"Column uses a different name. Consider renaming: '{header_cell.value}' to: '{column_defn.aliases[0]}'"
                if self.on_column_alias == EXCEPTION_HANDLING.Err:
                    self.errors[column_ref].append(alias_msg)
                elif self.on_column_alias == EXCEPTION_HANDLING.Warn:
                    self.warnings_[column_ref].append(alias_msg)
                elif self.on_column_alias == EXCEPTION_HANDLING.DoNothing:
                    self.info[column_ref].append(alias_msg)

        if not self._header_columns:
            found_headers = {}  # type: StringCellMap
            for column_ref, column_defn in self.column_definitions.items():

                try:
                    header_cell = find_value(self.headers_range, column_defn.aliases)
                    if column_ref in found_headers:
                        # TODO: More info for the user on header collision: Which headers have errors?
                        raise HeaderCollisionError(
                            "There was a collision between two header definitions"
                        )
                    found_headers[column_ref] = header_cell
                    header_column_handler(header_cell, column_defn)

                except CellNotFoundError:
                    if column_defn.required:
                        raise HeaderNotFoundError(
                            "A required header was not found. \nRequired, one of:\n\t%s\nHeaders found were: \n\t%s"
                            % (
                                "\n\t".join(column_defn.aliases),
                                "\n\t".join(
                                    worksheetrange_asdict(self.headers_range).values()
                                ),
                            )
                        )
                    logger.debug(
                        "No header for column set starting with %s",
                        column_defn.aliases[0],
                    )
                    # To find out which headers were included in the search,
                    # logger.debug(worksheetrange_asdict(self.headers_range))
                    pass

                # Write log messages, debugging  info
            self._header_columns = found_headers
        return self._header_columns

    @property
    def headers_range(self) -> WorksheetRange:
        """
        Returns rows of cells to search for header values
        """
        if not self._headers_range:
            header_range = self.header_coordinates
            logger.debug("Headers range %s", header_range)
            headers = self.sheet[header_range]
            self._headers_range = headers

        return self._headers_range

    @property
    def sheet_range(self) -> WorksheetRange:

        if not self._sheet_range:
            header_columns_rows = {
                k: v.column_letter
                for k, v in self.header_columns.items()
                if hasattr(v, "row")
            }  # type: Dict[str, str]

            first_col = min(header_columns_rows.values())
            last_col = max(header_columns_rows.values())
            try:
                first_row = self.find_first_value_row()
                last_row = self.find_last_value_row()
            except CellNotFoundError:
                raise

            self._sheet_range = self.sheet[
                f"{first_col}{first_row.row}:{last_col}{last_row.row}"
            ]

        return self._sheet_range

    @property
    def header_column_set(self):
        """
        Shorthand to generate a set
        of coordinate, value, key
        This can be used to compare different
        sets of headers from sheets or import iterations
        """
        return {
            (col.coordinate, col.value, col_key)
            for col_key, col in self.header_columns.items()
        }

    def validate(self) -> Tuple[SheetDefinition, Optional[Exception]]:
        try:
            self.sheet
            self.sheet_range
            self.headers_range
            self.header_columns
        except Exception as E:
            logger.debug(f"{E}")
            return self, E
        return self, None

    def extract(self) -> Iterator[Tuple[int, Dict[Any, Any], Dict[str, List[str]]]]:
        """
        Returns the data which was able to be extracted from
        the sheet and any errors encountered on the way
        """
        header_columns_rows = {
            k: v.column_letter
            for k, v in self.header_columns.items()
            if hasattr(v, "row")
        }  # type: Dict[str, str]
        included_columns = {v: k for k, v in header_columns_rows.items()}

        for row in self.sheet_range:
            row_idx = -1  # type: int
            row_json = {}
            row_errors = defaultdict(list)  # type: Dict[str, List[str]]

            for cell in row:

                if not hasattr(
                    cell, "column_letter"
                ):  # This occurs when an EmptyCell is encountered. Special "missing" value
                    continue

                if cell.column_letter not in included_columns:
                    # A column not included in the JSON definitions
                    continue

                if row_idx == -1 and isinstance(cell.row, int):
                    row_idx = cell.row

                if cell.column_letter in included_columns:
                    column_def = self.column_definitions[
                        included_columns[cell.column_letter]
                    ]
                    cell_value = cell.value

                    # Perform any cleaning up of the
                    # cell value here
                    if hasattr(cell_value, "strip"):
                        cell_value = cell_value.strip()  # type: ignore

                    for v in column_def.validators:
                        if cell_value is None and not column_def.required:
                            continue
                        cell_value, is_valid, message = v.validate(cell, cell_value)
                        if message:
                            row_errors[
                                f"{included_columns[cell.column_letter]} ({cell.column_letter})"
                            ].append(message)
                    row_json[included_columns[cell.column_letter]] = cell_value

            yield row_idx, row_json, row_errors


def find_value(
    cells: WorksheetRange,
    try_content: Tuple[str],
    inexact: bool = True,
    len_limit: int = 2,
) -> Cell:
    """
    Within the given range of cells, search for the first
    match to a given value

    Args:
        cells (WorksheetRange): The range of cells to search
        try_content (Iterable[str]): Loop over these strings to search for values
        inexact (bool, optional): Whether to try "less exact" (strip, lower, startswith) matches
        len_limit (int, optional): Restrict startswith to this length to prevent empty or short cell content matching everything

    Raises:
        CellNotFoundError: When the given phrases are not found in the search range

    Returns:
        Cell: The cell reference which contains the given content
    """
    cell_iter = itertools.chain.from_iterable(cells)
    for cell, header_content in itertools.product(cell_iter, try_content):
        if not hasattr(cell, "value"):
            continue
        cv = cell.value
        if Compar.exact(cv, header_content):
            logger.debug("Exact match for %s in %s", header_content, cell.coordinate)
            return cell
        elif (
            inexact
            and Compar.startswith(cv, header_content)
            and len(cv.strip()) > len_limit
        ):
            logger.debug(
                "Startswith match for %s in %s", header_content, cell.coordinate
            )
            return cell
    raise CellNotFoundError(
        "%s not in range %s:%s"
        % (
            try_content[0],
            list(filter(lambda x: hasattr(x, "coordinate"), cells[0]))[0].coordinate,
            list(filter(lambda x: hasattr(x, "coordinate"), cells[-1]))[-1].coordinate,
        )
    )
