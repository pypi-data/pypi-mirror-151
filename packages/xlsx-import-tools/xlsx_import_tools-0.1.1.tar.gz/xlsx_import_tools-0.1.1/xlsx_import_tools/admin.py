from django.contrib import admin

from . import models


@admin.register(models.ColumnDefinition)
class ColumnDefinitionAdmin(admin.ModelAdmin):
    list_display = (
        "col_name",
        "aliases",
        "required",
    )


@admin.register(models.SheetDefinition)
class SheetDefinitionAdmin(admin.ModelAdmin):
    list_display = (
        "sheet_name",
        "aliases",
    )


@admin.register(models.WorkbookDefinition)
class WorkbookDefinitionAdmin(admin.ModelAdmin):
    list_display = ("workbook_name",)
