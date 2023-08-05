import asyncio
from abc import ABC
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence

from pydantic import validate_arguments

from ..cache import cache
from ..core import BaseClient
from ..encoders import encode_query_params
from .errors import ServerError
from .retry import retry_policy

PATH = "/users/{user_uuid}/institutions/{institution_id}/transactions"

TransactionRecord = Dict[str, Any]
TransactionsMeta = Dict[str, Any]
TransactionsAccount = Dict[str, Any]
TransactionsResponse = Dict[str, Any]


class BaseTransactionsResource(ABC):
    def __init__(self, client: BaseClient):
        self._client = client

    @retry_policy(
        max_retry_count=4,
        max_retry_interval_seconds=10,
        retryable_exceptions=[ServerError],
    )
    async def _get_page(
        self,
        user_uuid: str,
        institution_id: str,
        utc_starttime: Optional[datetime] = None,
        utc_endtime: Optional[datetime] = None,
        labels: Optional[Sequence[str]] = None,
        account_types: Optional[Sequence[str]] = None,
        page: int = 1,
    ) -> TransactionsResponse:
        async with self._client.session() as session:
            response = await session.get(
                PATH.format(user_uuid=user_uuid, institution_id=institution_id),
                params=encode_query_params(
                    utc_starttime=utc_starttime,
                    utc_endtime=utc_endtime,
                    labels=labels,
                    account_types=account_types,
                    page=page,
                ),
            )

        if response.status_code == 500:
            raise ServerError(response.text)

        assert response.status_code == 200, response.text
        return response.json()  # type: ignore

    @validate_arguments
    @cache
    async def _get(
        self,
        user_uuid: str,
        institution_id: str,
        utc_starttime: Optional[datetime] = None,
        utc_endtime: Optional[datetime] = None,
        labels: Optional[Sequence[str]] = None,
        account_types: Optional[Sequence[str]] = None,
        page: Optional[int] = None,
    ) -> List[TransactionRecord]:
        response = await self._get_page(
            user_uuid=user_uuid,
            institution_id=institution_id,
            utc_starttime=utc_starttime,
            utc_endtime=utc_endtime,
            labels=labels,
            account_types=account_types,
            page=page or 1,
        )
        max_pages = response["_meta"]["max_pages"]
        if not page and max_pages > 1:
            coroutines = [
                self._get_page(
                    user_uuid=user_uuid,
                    institution_id=institution_id,
                    utc_starttime=utc_starttime,
                    utc_endtime=utc_endtime,
                    labels=labels,
                    account_types=account_types,
                    page=page + 2,
                )
                for page in range(max_pages - 1)
            ]
            response_pages = await asyncio.gather(*coroutines)
            responses = (response, *response_pages)
        else:
            responses = (response,)

        return [
            record
            for response in responses
            for transaction_account in response["transactions"]
            for record in transaction_account["records"]
        ]


class AsyncTransactionsResource(BaseTransactionsResource):
    async def get(
        self,
        user_uuid: str,
        institution_id: str,
        *,
        utc_starttime: Optional[datetime] = None,
        utc_endtime: Optional[datetime] = None,
        labels: Optional[Sequence[str]] = None,
        account_types: Optional[Sequence[str]] = None,
        page: Optional[int] = None,
    ) -> List[TransactionRecord]:
        return await self._get(
            user_uuid=user_uuid,
            institution_id=institution_id,
            utc_starttime=utc_starttime,
            utc_endtime=utc_endtime,
            labels=labels,
            account_types=account_types,
            page=page,
        )


class SyncTransactionsResource(BaseTransactionsResource):
    def get(
        self,
        user_uuid: str,
        institution_id: str,
        *,
        utc_starttime: Optional[datetime] = None,
        utc_endtime: Optional[datetime] = None,
        labels: Optional[Sequence[str]] = None,
        account_types: Optional[Sequence[str]] = None,
        page: Optional[int] = None,
    ) -> List[TransactionRecord]:
        return self._client.run(
            self._get(
                user_uuid=user_uuid,
                institution_id=institution_id,
                utc_starttime=utc_starttime,
                utc_endtime=utc_endtime,
                labels=labels,
                account_types=account_types,
                page=page,
            )
        )
