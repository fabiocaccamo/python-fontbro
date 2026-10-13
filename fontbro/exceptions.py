from __future__ import annotations


class ArgumentError(ValueError):
    pass


class DataError(ValueError):
    pass


class OperationError(TypeError):
    pass


class ClosedFontError(OperationError):
    """
    The operation was called on a closed font.
    """


class MissingTableError(OperationError, KeyError):
    """
    The operation requires a table the font doesn't have.
    It's also a KeyError, raised before when accessing the missing table.
    """

    def __init__(
        self,
        table_tag: str,
        message: str | None = None,
    ) -> None:
        self.table_tag = table_tag
        super().__init__(message or f"Invalid {table_tag} table (doesn't exist).")

    def __reduce__(self) -> tuple[type[MissingTableError], tuple[str, str]]:
        # pickle and copy recreate the exception passing its args (the message
        # only) to __init__, the table tag must be passed too
        return (self.__class__, (self.table_tag, str(self)))

    def __str__(self) -> str:
        # KeyError wraps the message in quotes
        return str(self.args[0])


class VariableFontRequiredError(OperationError):
    """
    The operation requires a variable font.
    """


class SanitizationError(Exception):
    pass
