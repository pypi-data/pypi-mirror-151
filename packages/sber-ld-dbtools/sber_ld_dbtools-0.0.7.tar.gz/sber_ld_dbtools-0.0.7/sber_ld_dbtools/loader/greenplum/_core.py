from collections.abc import Mapping as _Mapping
from contextlib import ExitStack
from copy import copy
from typing import Any, Mapping, Dict

import psycopg2
from pandakeeper.dataloader.sql import SqlLoader
from pandakeeper.validators import AnyDataFrame
from pandera import DataFrameSchema
from typing_extensions import final
from varutils.plugs.constants import empty_mapping_proxy
from varutils.typing import check_type_compatibility

from sber_ld_dbtools.credentials import PasswordKeeper, set_default_kerberos_principal

__all__ = (
    'GreenplumLoader',
)


def _greenplum_context_creator(stack: ExitStack,
                               credentials: PasswordKeeper,
                               **greenplum_context_kwargs: Any) -> psycopg2.extensions.connection:
    set_default_kerberos_principal(credentials)
    if 'user' not in greenplum_context_kwargs:
        greenplum_context_kwargs['user'] = credentials.get_username()
    conn = stack.enter_context(psycopg2.connect(**greenplum_context_kwargs))
    return conn


class GreenplumLoader(SqlLoader):
    __slots__ = ()

    def __init__(self,
                 sql_query: str,
                 *,
                 credentials: PasswordKeeper,
                 greenplum_parameters: Mapping[str, Any] = empty_mapping_proxy,
                 output_validator: DataFrameSchema = AnyDataFrame,
                 **read_sql_kwargs: Any) -> None:

        check_type_compatibility(credentials, PasswordKeeper)
        check_type_compatibility(greenplum_parameters, _Mapping, 'Mapping')

        for keyword in ('host', 'dbname'):
            if keyword not in greenplum_parameters:
                raise KeyError(f"Parameter 'greenplum_parameters' should contain '{keyword}' key")

        super().__init__(
            _greenplum_context_creator,
            sql_query,
            context_creator_args=(credentials,),
            context_creator_kwargs=copy(greenplum_parameters),
            read_sql_kwargs=read_sql_kwargs,
            output_validator=output_validator
        )

    @final
    @property
    def credentials(self) -> PasswordKeeper:
        return self._context_creator_args[0]

    @final
    @property
    def greenplum_parameters(self) -> Dict[str, Any]:
        res = dict(self._context_creator_kwargs)
        if 'password' in res:
            res['password'] = '*****'
        return res
