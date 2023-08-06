import typing as t


class IRecord(t.Protocol):
    def get_id(self) -> str:
        ...


TIRecord = t.TypeVar("TIRecord", bound=IRecord)
T = t.TypeVar("T")


class IRecordStore(t.Protocol[T]):
    """Interface for a Data Access Object (DAO) which can save objects to some back-end persistence solution."""

    def save(self, record: T):
        """Updates ``record`` in the database, or creates it if it's not there."""
        ...

    def get(self, id_: str) -> t.Optional[T]:
        """Retrieves a record from the database, returning ``None`` if it doesn't exist."""
        ...

    def delete(self, id_: str) -> bool:
        """
        Deletes a record from the database, returning ``True`` if the record was deleted, and ``False`` if it didn't
        exist.
        """
        ...

    def get_all(self, **where_equals) -> t.Iterable[T]:
        """Retrieves all records which satisfy the optional ``*where_equals`` equality conditions."""
        ...

    def delete_all(self, **where_equals) -> int:
        """
        Deletes all records which satisfy the optional ``*where_equals`` equality conditions. Returns the number of
        records that were deleted.
        """
        ...
