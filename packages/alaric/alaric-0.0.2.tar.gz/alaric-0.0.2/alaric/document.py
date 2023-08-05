import functools
from copy import deepcopy
from typing import List, Dict, Optional, Union, Any, TypeVar, Type

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.results import DeleteResult

from alaric.abc import BuildAble

T = TypeVar("T")


def return_converted(func):
    """
    If we have a registered converter,
    this deco will attempt to parse
    the given data into our provided
    class through the use of dictionary unpacking.
    """

    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        data: Union[Dict, List[Dict]] = await func(*args, **kwargs)

        self: Document = args[0]
        if not data or not self.converter:
            return data

        if not isinstance(data, list):
            return self.converter(**data)

        new_data = []
        for d in data:
            new_data.append(self.converter(**d))

        return new_data

    return wrapped


class Document:
    _version = 10

    def __init__(
        self,
        database: AsyncIOMotorDatabase,
        document_name: str,
        converter: Optional[Type[T]] = None,
    ):
        """
        Parameters
        ----------
        database: AsyncIOMotorDatabase
            The database we are connected to
        document_name: str
            What this _document should be called
        converter: Optional[Type[T]]
            An optional converter to try
            to convert all data-types which
            return either Dict or List into
        """
        self._document_name: str = document_name
        self._database: AsyncIOMotorDatabase = database
        self._document: AsyncIOMotorCollection = database[document_name]

        self.converter: Type[T] = converter

    def __repr__(self):
        return f"<Document(document_name={self.document_name})>"

    @return_converted
    async def find(
        self, filter_dict: Union[Dict, BuildAble]
    ) -> Optional[Union[Dict[str, Any], Type[T]]]:
        """
        Find and return one item.

        Parameters
        ----------
        filter_dict: Union[Dict, BuildAble]
            A dictionary to use as a filter or
            :py:class:`AQ` object.

        Returns
        -------
        Optional[Union[Dict[str, Any], Type[T]]]
            The result of the query
        """
        if isinstance(filter_dict, BuildAble):
            filter_dict = filter_dict.build()

        filter_dict = self.__convert_filter(filter_dict)
        self.__ensure_dict(filter_dict)

        return await self._document.find_one(filter_dict)

    @return_converted
    async def find_many(
        self, filter_dict: Union[Dict[str, Any], BuildAble]
    ) -> List[Union[Dict[str, Any], Type[T]]]:
        """
        Find and return all items
        matching the given filter.

        Parameters
        ----------
        filter_dict: Dict[str, Any]
            A dictionary to use as a filter or
            :py:class:`AQ` object.

        Returns
        -------
        List[Union[Dict[str, Any], Type[T]]]
            The result of the query
        """
        if isinstance(filter_dict, BuildAble):
            filter_dict = filter_dict.build()

        self.__ensure_dict(filter_dict)

        return await self._document.find(filter_dict).to_list(None)

    async def delete(
        self, filter_dict: Union[Dict, BuildAble]
    ) -> Optional[DeleteResult]:
        """
        Delete an item from the Document
        if an item with the provided filter exists.

        Parameters
        ----------
        filter_dict: Union[Dict, BuildAble]
            A dictionary to use as a filter or
            :py:class:`AQ` object.

        Returns
        -------
        Optional[DeleteResult]
            The result of deletion if it occurred.
        """
        filter_dict = self.__convert_filter(filter_dict)
        self.__ensure_dict(filter_dict)

        result: DeleteResult = await self._document.delete_many(filter_dict)
        result: Optional[DeleteResult] = result if result.deleted_count != 0 else None
        return result

    async def update(
        self,
        filter_dict: Union[Dict, Any],
        data: Dict[str, Any] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Update an existing _document within the database
        Parameters
        ----------
        filter_dict: Union[Dict, Any]
            The _id of the item to update by,
            if a Dict is passed that is
            used as the filter.
        data: Dict[str, Any]
            The data we want to update with
        """
        filter_dict = self.__convert_filter(filter_dict)

        if data is None:
            # Backwards compat so you can just pass something like
            # await doc.upsert({"_id": 1, "data": False})
            data = deepcopy(filter_dict)
            filter_dict = self.__convert_filter(data.pop("_id"))

        await self.update_by_custom(filter_dict, data, *args, **kwargs)

    # <-- Actual Methods -->
    @return_converted
    async def get_all(
        self,
        filter_dict: Optional[Union[Dict[str, Any], BuildAble]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> List[Optional[Union[Dict[str, Any], Type[T]]]]:
        """
        Fetches and returns all items
        which match the given filter.

        Example usages

        .. code-block:: python
            results = await document.get_all()

            ...

            # Get all documents with a given field
            results = await document.get_all(AQ(EXISTS("field")))

        Parameters
        ----------
        filter_dict: Optional[Dict[str, Any]]
            A dictionary to use as a filter or
            :py:class:`AQ` object.

        Returns
        -------
        List[Optional[Union[Dict[str, Any], Type[T]]]]
            The items matching the filter
        """
        filter_dict = filter_dict or {}
        if isinstance(filter_dict, BuildAble):
            filter_dict = filter_dict.build()

        return await self._document.find(filter_dict, *args, **kwargs).to_list(None)

    async def insert(self, data: Dict[str, Any]) -> None:
        """
        Insert the given data into the _document
        Parameters
        ----------
        data: Dict[str, Any]
            The data to insert
        """
        self.__ensure_dict(data)

        await self._document.insert_one(data)

    async def upsert(
        self,
        filter_dict: Union[Dict, Any],
        data: Dict[str, Any] = None,
        option: str = "set",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Performs an UPSERT operation,
        so data is either INSERTED or UPDATED
        based on the current state of the _document.
        Parameters
        ----------
        filter_dict: Union[Dict, Any]
            The _id of the item to update by,
            if a Dict is passed that is
            used as the filter.
        data: Dict[str, Any]
            The data to upsert (filter is _id)
        option: str
            The optional option to pass to mongo,
            default is set
        """
        # Fairly sure this is no longer needed
        # if await self.find_by_id(data["_id"]) is None:
        #     return await self.insert(data)
        filter_dict = self.__convert_filter(filter_dict)

        if data is None:
            # Backwards compat so you can just pass something like
            # await doc.upsert({"_id": 1, "data": False})
            data = deepcopy(filter_dict)
            filter_dict = self.__convert_filter(data.pop("_id"))

        await self.upsert_custom(filter_dict, data, option, *args, **kwargs)

    async def update_by_id(
        self, data: Dict[str, Any], option: str = "set", *args: Any, **kwargs: Any
    ) -> None:
        """
        Performs an update operation.
        Parameters
        ----------
        data: Dict[str, Any]
            The data to upsert (filter is _id)
        option: str
            The optional option to pass to mongo,
            default is set
        Notes
        -----
        If the data doesn't already
        exist, this makes no changes
        to the actual database.
        """
        self.__ensure_dict(data)
        self.__ensure_id(data)

        data_id = data.pop("_id")
        await self._document.update_one(
            {"_id": data_id}, {f"${option}": data}, *args, **kwargs
        )

    async def upsert_custom(
        self,
        filter_dict: Dict[str, Any],
        update_data: Dict[str, Any],
        option: str = "set",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Performs an UPSERT operation,
        so data is either INSERTED or UPDATED
        based on the current state of the _document.
        Uses filter_dict rather then _id
        Parameters
        ----------
        filter_dict: Dict[str, Any]
            The data to filter on
        update_data: Dict[str, Any]
            The data to upsert
        option: str
            The optional option to pass to mongo,
            default is set
        """
        await self.update_by_custom(
            filter_dict, update_data, option, upsert=True, *args, **kwargs
        )

    async def update_by_custom(
        self,
        filter_dict: Dict[str, Any],
        update_data: Dict[str, Any],
        option: str = "set",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Performs an update operation.
        Parameters
        ----------
        filter_dict: Dict[str, Any]
            The data to filter on
        update_data: Dict[str, Any]
            The data to upsert
        option: str
            The optional option to pass to mongo,
            default is set
        """
        self.__ensure_dict(filter_dict)
        self.__ensure_dict(update_data)

        # Update
        await self._document.update_one(
            filter_dict, {f"${option}": update_data}, *args, **kwargs
        )

    async def unset(self, _id: Union[Dict, Any], field: Any) -> None:
        """
        Remove a given param, basically dict.pop on the db.
        Works based off _id
        Parameters
        ----------
        _id: Any
            The field's _document id or
            dict as a filter
        field: Any
            The field to remove
        """
        filter_dict = self.__convert_filter(_id)
        await self.unset_by_custom(filter_dict, field)

    async def unset_by_custom(self, filter_dict: Dict[str, Any], field: Any) -> None:
        """
        Remove a given param, basically dict.pop on the db.
        Works based off _id
        Parameters
        ----------
        filter_dict: Dict[str, Any]
            The fields to match on (Think _id)
        field: Any
            The field to remove
        """
        self.__ensure_dict(filter_dict)
        await self._document.update_one(filter_dict, {"$unset": {field: True}})

    async def increment(
        self, data_id: Union[Dict, Any], amount: Union[int, float], field: str
    ) -> None:
        """
        Increment a field somewhere.
        Parameters
        ----------
        data_id: Any
            The fields to match on (Think _id)
        amount: Union[int, float]
            How much to increment (or decrement) by
        field: str
            The key for the field to increment
        """
        filter_dict = self.__convert_filter(data_id)

        await self.increment_by_custom(filter_dict, amount, field)

    async def increment_by_custom(
        self, filter_dict: Dict[Any, Any], amount: Union[int, float], field: str
    ) -> None:
        """
        Increment a field somewhere.
        Parameters
        ----------
        filter_dict: Dict[Any, Any]
            The 'thing' we want to increment
        amount: Union[int, float]
            How much to increment (or decrement) by
        field: str
            The key for the field to increment
        """
        self.__ensure_dict(filter_dict)
        await self._document.update_one(filter_dict, {"$inc": {field: amount}})

    async def update_field_to(
        self, filter_dict: Union[Dict[Any, Any], BuildAble], field: str, new_value: Any
    ) -> None:
        """
        Modify a single field and change the value.

        Parameters
        ----------
        filter_dict: Union[Dict[Any, Any], BuildAble]
            A dictionary to use as a filter or
            :py:class:`AQ` object.
        field: str
            The key for the field to increment
        new_value: Any
            What the field should get changed to
        """
        if isinstance(filter_dict, BuildAble):
            filter_dict = filter_dict.build()

        self.__ensure_dict(filter_dict)
        await self._document.update_one(filter_dict, {"$set": {field: new_value}})

    async def bulk_insert(self, data: List[Dict]) -> None:
        """
        Given a List of Dictionaries, bulk insert all
        the given dictionaries in a single call.

        Parameters
        ----------
        data: List[Dict]
            The data to bulk insert
        """
        self.__ensure_list_of_dicts(data)
        await self._document.insert_many(data)

    # <-- Private methods -->
    @staticmethod
    def __ensure_list_of_dicts(data: List[Dict]):
        assert isinstance(data, list)
        assert all(isinstance(entry, dict) for entry in data)

    @staticmethod
    def __ensure_dict(data: Dict[str, Any]) -> None:
        assert isinstance(data, dict)

    # <-- Some basic internals -->
    @property
    def document_name(self) -> str:
        return self._document_name

    @property
    def raw_database(self) -> AsyncIOMotorDatabase:
        return self._database

    @property
    def raw_collection(self) -> AsyncIOMotorCollection:
        return self._document
