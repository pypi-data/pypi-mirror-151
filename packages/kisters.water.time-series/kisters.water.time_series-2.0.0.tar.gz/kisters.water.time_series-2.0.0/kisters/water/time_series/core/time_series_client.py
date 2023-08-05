from __future__ import annotations

import asyncio
import inspect
import itertools
from abc import abstractmethod
from collections.abc import AsyncIterator, Callable, Coroutine, Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
from typing import Any, Generic, Type, TypeVar

import pandas as pd  # type: ignore
from pydantic import ValidationError

from . import TimeSeriesUserError
from .schema import CommentSupport, EnsembleMember, TimeSeriesComment, TimeSeriesMetadata
from .time_series import TimeSeries, TimeSeriesMetadataT, TimeSeriesT


def make_iterable(value: Any) -> Iterable[Any]:
    """Make an infinite iterable if it's not iterable or it's string."""
    if not isinstance(value, Iterable) or isinstance(value, str):
        return itertools.repeat(value)
    return value


T = TypeVar("T")


class TimeSeriesClient(Generic[TimeSeriesT, TimeSeriesMetadataT]):
    comment_support: CommentSupport = CommentSupport.UNSUPPORTED
    time_series_schema: Type[TimeSeriesMetadataT] = TimeSeriesMetadata  # type: ignore

    @classmethod
    def sanitize_metadata(
        cls,
        *,
        path: str | None = None,
        metadata: dict[str, Any] | TimeSeriesMetadata | None = None,
    ) -> TimeSeriesMetadataT:
        if not metadata and not path:
            raise TimeSeriesUserError("Invalid arguments: path and metadata cannot be both None", str(path))
        elif not metadata:
            metadata = cls.time_series_schema(path=path)
        else:
            try:
                metadata = cls.time_series_schema.parse_obj(metadata)
                if path:
                    metadata.path = path  # type: ignore
            except ValidationError as e:
                raise TimeSeriesUserError(
                    f"Invalid metadata {metadata} for time series {path}", str(path)
                ) from e
        return metadata  # type: ignore

    @abstractmethod
    async def __aenter__(self) -> TimeSeriesClient[TimeSeriesT, TimeSeriesMetadataT]:
        """Enter the async context"""

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the async context"""

    def run_sync(
        self,
        coroutine: Callable[..., Coroutine[Any, Any, T]],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """This method safely calls async methods from a sync context."""
        if not inspect.iscoroutinefunction(coroutine):
            raise ValueError(f"Method: {coroutine}, is not a coroutine")
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            # No event loop is running. Using asyncio.run() is not safe,
            # because it cleans up event loops.
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.__aenter__())
            result = loop.run_until_complete(coroutine(*args, **kwargs))
            loop.run_until_complete(self.__aexit__(None, None, None))
            return result

        # There is an event loop already running, but are in a sync context.
        # Calling the async methods from this method/thread is not possible, so
        # we spawn a new loop in a temporary thread. While not optimal from a
        # performance perspective, it ensures that both sync and async contexts
        # can share the OIDC client. As tokens are cached, sharing the client
        # is still much cheaper than the overhead of spawning a thread once in
        # a while. In performance-critical contexts, the overhead can be avoided
        # completely by using the async API
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(asyncio.run, self.__aenter__())  # type: ignore
            future = executor.submit(asyncio.run, coroutine(*args, **kwargs))
            wait([executor.submit(asyncio.run, self.__aexit__(None, None, None))])  # type: ignore
            return future.result()

    def iter_over_async(
        self, coroutine: Callable[..., AsyncIterator[T]], *args: Any, **kwargs: Any
    ) -> Iterator[T]:
        if not inspect.isasyncgenfunction(coroutine):
            raise ValueError(f"Method: {coroutine}, is not an async generator")
        ait = coroutine(*args, **kwargs)

        async def get_next() -> tuple[bool, T | None]:
            try:
                obj = await ait.__anext__()
                return False, obj
            except StopAsyncIteration:
                return True, None

        executor_context = None
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
            run = loop.run_until_complete
        else:
            executor_context = ThreadPoolExecutor(max_workers=1).__enter__()

            def run(next_coroutine: Coroutine[Any, Any, Any]) -> Any:  # type: ignore
                return executor_context.submit(asyncio.run, next_coroutine).result()  # type: ignore

        run(self.__aenter__())
        done, obj = run(get_next())
        while not done:
            yield obj  # type: ignore
            done, obj = run(get_next())
        run(self.__aexit__(None, None, None))
        if executor_context:
            executor_context.__exit__(None, None, None)

    @abstractmethod
    async def create_time_series(
        self,
        *,
        path: str,
        metadata: dict[str, Any] | TimeSeriesMetadata | None = None,
        **kwargs: Any,
    ) -> TimeSeriesT:
        """
        Create a time series.

        Args:
            path: The time series path.
            metadata: The time series metadata.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            The TimeSeries object.
        """

    @abstractmethod
    async def read_time_series(
        self, *, path: str, metadata_keys: list[str] | None = None, **kwargs: Any
    ) -> TimeSeriesT:
        """
        Get the TimeSeries by path.

        Args:
            *path: The full qualified TimeSeries path.
            metadata_keys: list of metadata keys to read.  Set to None to request all metadata.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            The TimeSeries object.

        Examples:
            .. code-block:: python
                ts = await context.get_by_path("W7AgentTest/20003/S/cmd")
        """

    @abstractmethod
    def filter_time_series(
        self,
        *,
        ts_filter: str | None,
        metadata_keys: list[str] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[TimeSeriesT]:
        """
        Get time series based on filter strings.

        Args:
            ts_filter: An iterable of TimeSeries paths or filters.
            metadata_keys: list of metadata keys to read.  Set to None to request all metadata.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            The list of the found TimeSeries objects.

        Examples:
            .. code-block:: python
                async for ts in context.filter_time_series("W7AgentTest/20004/S/*"):
                    print(ts.metadata)
        """

    @abstractmethod
    async def update_time_series(
        self, *, path: str, metadata: dict[str, Any] | TimeSeriesMetadata, **kwargs: Any
    ) -> None:
        """
        Update the time series metadata.

        Args:
            path: The time series path.
            metadata: The time series metadata.
            **kwargs: Additional backend specific keyword arguments.
        """

    @abstractmethod
    async def delete_time_series(self, *, path: str, **kwargs: Any) -> None:
        """
        Delete the time series.

        Args:
            path: The time series path.
            **kwargs: Additional backend specific keyword arguments.
        """

    @abstractmethod
    async def read_coverage(
        self,
        *,
        path: str,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
    ) -> tuple[datetime, datetime]:
        """
        Get the time series coverage.

        Args:
            path: The time series path.
            t0: The t0 of the ensemble member.
            dispatch_info: The dispatch info of the ensemble member.
            member: The member info of the ensemble member.

        Returns:
            A tuple of datetimes.
        """

    @abstractmethod
    def read_ensemble_members(
        self,
        *,
        path: str,
        t0_start: datetime | None = None,
        t0_end: datetime | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[EnsembleMember]:
        """
        Read the ensemble members of a forecast time series.

        Args:
            path: The time series path.
            t0_start: The starting date from which to look for ensembles.
            t0_end: The ending date until which to look for ensembles.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            An AsyncIterator of EnsembleMember objects.
        """

    @abstractmethod
    async def read_data_frame(
        self,
        *,
        path: str,
        start: datetime | None = None,
        end: datetime | None = None,
        columns: list[str] | None = None,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        This method returns the TimeSeries data between the start and end dates (both dates included)
        structured as a pandas DataFrame, the DataFrame index is localized in the TimeSeries timezone.

        Args:
            path: The time series path.
            start: The starting date from which the data will be returned.
            end: The ending date until which the data will be covered (end date included).
            columns: The list of column keys to read.
            t0: The t0 timestamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            The DataFrame containing the TimeSeries data
        """

    @abstractmethod
    async def write_data_frame(
        self,
        *,
        path: str,
        data_frame: pd.DataFrame,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        This method writes the TimeSeries data from the data_frame into this TimeSeries.

        Args:
            path: The time series path.
            data_frame: The TimeSeries data to be written in the form of a pandas DataFrame.
            t0: The t0 time stamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier
            **kwargs: Additional backend specific keyword arguments.
        """

    @abstractmethod
    async def delete_data_range(
        self,
        *,
        path: str,
        start: datetime | None = None,
        end: datetime | None = None,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        This method deletes a range of data and/or an ensemble member from a time series.

        Args:
            path: The time series path.
            start: The starting date from which the data will be returned.
            end: The ending date until which the data will be covered.
            t0: The t0 time stamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier
            **kwargs: Additional backend specific keyword arguments.
        """

    async def read_data_frames(
        self,
        *,
        paths: Iterable[str],
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        t0: datetime | Iterable[datetime | None] | None = None,
        dispatch_info: str | Iterable[str | None] | None = None,
        member: str | Iterable[str | None] | None = None,
        **kwargs: Any,
    ) -> dict[str, pd.DataFrame]:
        """
        Read multiple TimeSeries as data frames.

        Notes:
            This method can be overwritten on backends which support bulk operations.

        Args:
            paths: An iterable of time series paths.
            start: An optional iterable of datetimes representing the date from which data will be written,
                if a single datetime is passed it is used for all the TimeSeries.
            end: An optional iterable of datetimes representing the date until (included) which data will be
                written, if a single datetime is passed it is used for all the TimeSeries.
            t0: An optional iterable of datetimes used to select the t0 in an ensemble TimeSeries, if a
                single datetime is passed it is used for all the TimeSeries.
            dispatch_info: An optional iterable of str used to select the dispatch info in an ensemble
                TimeSeries, if a single str is passed it is used for all the TimeSeries.
            member: An optional iterable of str used to select the member in an ensemble TimeSeries,
                if a single str is passed it is used for all the TimeSeries.
            **kwargs: Additional backend specific keyword arguments.
        """
        data_frames = await asyncio.gather(
            *(
                self.read_data_frame(
                    path=path,
                    start=start_i,
                    end=end_i,
                    t0=t0_i,
                    dispatch_info=dispatch_info_i,
                    member=member_i,
                    **kwargs,
                )
                for path, start_i, end_i, t0_i, dispatch_info_i, member_i in zip(
                    paths,
                    make_iterable(start),
                    make_iterable(end),
                    make_iterable(t0),
                    make_iterable(dispatch_info),
                    make_iterable(member),
                )
            )
        )
        return {path: df for path, df in zip(paths, data_frames)}

    async def write_data_frames(
        self,
        *,
        paths: Iterable[str],
        data_frames: Iterable[pd.DataFrame],
        t0: datetime | Iterable[datetime | None] | None = None,
        dispatch_info: str | Iterable[str | None] | None = None,
        member: str | Iterable[str | None] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Write multiple data frames to TimeSeries

        Notes:
            This method can be overwritten on backends which support bulk operations.

        Args:
            paths: An iterable of time series paths.
            data_frames: An iterable of DataFrames
            t0: An optional iterable of datetimes used to select the t0 in an ensemble TimeSeries,
                if a single datetime is passed it is used for all the TimeSeries.
            dispatch_info: An optional iterable of str used to select the dispatch info in an ensemble
                TimeSeries, if a single str is passed it is used for all the TimeSeries.
            member: An optional iterable of str used to select the member in an ensemble TimeSeries,
                if a single str is passed it is used for all the TimeSeries.
            **kwargs: Additional backend specific keyword arguments.
        """
        await asyncio.gather(
            *(
                self.write_data_frame(
                    path=path,
                    data_frame=df_i,
                    t0=t0_i,
                    dispatch_info=dispatch_info_i,
                    member=member_i,
                    **kwargs,
                )
                for path, df_i, t0_i, dispatch_info_i, member_i in zip(
                    paths,
                    data_frames,
                    make_iterable(t0),
                    make_iterable(dispatch_info),
                    make_iterable(member),
                )
            )
        )

    def read_comments(
        self,
        *,
        path: str,
        start: datetime | None = None,
        end: datetime | None = None,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[TimeSeriesComment]:
        """
        Read the time series comments.

        Args:
            path: The time series path.
            start: The datetime from which to retrieve comments.
            end: The datetime until which to retrieve comments.
            t0: The t0 timestamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            An iterable of TimeSeriesComment objects.
        """
        raise NotImplementedError

    async def write_comments(
        self,
        *,
        path: str,
        comments: list[TimeSeriesComment],
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Write a list of time series comments.

        Args:
            path: The time series path.
            comments: The time series comments.
            t0: The t0 timestamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier
            **kwargs: Additional backend specific keyword arguments.
        """
        raise NotImplementedError

    async def delete_comments(
        self,
        path: str,
        comment_ids: list[str] | None = None,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Delete time series comments.

        Args:
            path: The time series path.
            comment_ids: The time series comment ids to delete.
            t0: The t0 timestamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier
            **kwargs: Additional backend specific keyword arguments.
        """
        raise NotImplementedError


TimeSeriesClientT = TypeVar("TimeSeriesClientT", bound=TimeSeriesClient[TimeSeries, TimeSeriesMetadata])
