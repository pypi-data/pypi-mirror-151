from typing import Dict, Iterable, List, Type

from django.contrib.postgres.fields import ArrayField
from django.db import models

from xlsx_import_tools.definitions import EXCEPTION_HANDLING

from . import definitions, workbook_validator

"""
This module provides a convenient "wrapper" to
create / alter an excel import schema using Django.
The models here map to the definitions used for Column, Sheet and Workbook validator
and create classes dynamically to provide a django -> 'standard'
python bridge which makes no alterations to existing API.
"""


class ColumnDefinition(models.Model):
    col_name = models.SlugField(
        help_text="A nicely formatted handle to refer to this column",
        unique=True,
    )  # type: str
    required = models.BooleanField(default=True)  # type: ignore
    aliases = ArrayField(
        models.CharField(max_length=128),
        help_text="Alternative wordings/spellings for this column header",
    )  # type: Iterable[str]

    def as_defn(self):
        """
        Create a new `definitions.ColumnDefinition` class and return an instance of that class
        """
        return type(
            f"{self.col_name.title()}ColumnDefinition",
            (definitions.ColumnDefinition,),
            dict(
                aliases=self.aliases,
                required=self.required,
            ),
        )()

    def __str__(self):
        return "{} {} - {}".format(
            self.col_name,
            {True: "(req)", False: ""}[self.required],
            " / ".join(self.aliases),
        )


class SheetDefinition(models.Model):
    sheet_name = models.TextField(
        help_text="A nicely formatted handle to refer to this sheet"
    )
    columns = models.ManyToManyField(
        ColumnDefinition, help_text="Columns to import data from"
    )
    required = models.BooleanField(
        default=True,
        help_text="Declare whether this workbook required to be in the excel file",
    )  # type: bool
    # aliases is a list of names the worksheet may take
    aliases = ArrayField(
        models.CharField(max_length=128),
        help_text="The names which can be used for the workbook sheet to import",
    )  # type: List[str]
    header_definition = models.ForeignKey(
        ColumnDefinition,
        related_name="+",
        on_delete=models.PROTECT,
        help_text="Aliases of this column are used to search for the header row(s)",
    )

    def as_sheet_defn_class(self) -> Type[definitions.SheetDefinition]:

        # A nasty hack because our beloved ArrayField does not save trailing spaces, aaargh
        aliases = self.aliases
        if "Admin" in self.aliases:
            self.aliases.append("Admin ")

        return type(
            f"{self.sheet_name.title()}SheetDefinition",
            (definitions.SheetDefinition,),
            dict(
                aliases=aliases,
                required=self.required,
                column_definitions={
                    col.col_name: col.as_defn() for col in self.columns.all()
                },
            ),
        )

    def as_defn(self, workbook) -> definitions.SheetDefinition:
        """
        Create a new `definitions.SheetDefinition` class and return an instance of that class
        """
        return self.as_sheet_defn_class()(
            workbook, header_definition=self.header_definition
        )

    def __str__(self):
        return "{} {} - {}".format(
            self.sheet_name,
            {True: "(req)", False: ""}[self.required],
            " / ".join(self.aliases),
        )


class WorkbookDefinition(models.Model):

    on_column_alias = (
        EXCEPTION_HANDLING.Warn
    )  # Note: We might change this to a user editable IntegerField in the future

    workbook_name = models.SlugField(
        help_text="A nicely formatted handle to refer to this type of workbook"
    )
    sheets = models.ManyToManyField(
        SheetDefinition, help_text="Sheets to import data from"
    )

    def as_validator(self, workbook):
        """
        Returns a WorkbookValidator instance tied to the workbook
        """
        # Dynamically generated sheet definitions
        # Note: these are clsses, not instances of classes
        sheet_definition_classes = {
            sheet.sheet_name: sheet.as_sheet_defn_class() for sheet in self.sheets.all()
        }  # type: Dict[str, Type[definitions.SheetDefinition]]

        return type(
            f"{self.workbook_name.title()}WorkbookValidator",
            (workbook_validator.WorkbookValidator,),
            dict(sheet_definition_classes=sheet_definition_classes),
        )(workbook=workbook)

    def __str__(self):
        return self.workbook_name
