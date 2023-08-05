from collections.abc import Mapping as _Mapping
from contextlib import ExitStack
from copy import copy
from os import PathLike
from typing import Any, Optional, Union, Mapping, Dict
from warnings import warn

import jaydebeapi
from jpype import JVMNotFoundException, isJVMStarted, startJVM, getDefaultJVMPath
from pandakeeper.dataloader.sql import SqlLoader
from pandakeeper.validators import AnyDataFrame
from pandera import DataFrameSchema
from typing_extensions import final
from varutils.plugs.constants import empty_mapping_proxy
from varutils.typing import check_type_compatibility

from sber_ld_dbtools.credentials import PasswordKeeper

__all__ = (
    'OracleContextManager',
    'OracleLoader',
    'GlobalOracleConfig'
)


class OracleContextManager:
    __slots__ = ('host', 'user', '__password', 'port', 'sid', 'connection')

    def __init__(self, host: str, *, user: str, password: str, port: Union[str, int], sid: str) -> None:

        check_type_compatibility(host, str)
        check_type_compatibility(user, str)
        check_type_compatibility(password, str)
        check_type_compatibility(port, (str, int))
        check_type_compatibility(sid, str)

        self.host = host
        self.user = user
        self.__password = password
        self.port = port
        self.sid = sid
        self.connection: Optional[jaydebeapi.Connection] = None

    def __enter__(self) -> jaydebeapi.Connection:
        if not isJVMStarted():
            startJVM(
                GlobalOracleConfig.JVMPath,
                f'-Djava.class.path={GlobalOracleConfig.OJDBC8_PATH}',
                convertStrings=True
            )
        self.connection = jaydebeapi.connect(
            'oracle.jdbc.driver.OracleDriver',
            f'jdbc:oracle:thin:{self.user}/{self.__password}@{self.host}:{self.port}:{self.sid}'
        )
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        if exc_type is not None:
            raise


def _oracle_context_creator(stack: ExitStack,
                            credentials: PasswordKeeper,
                            **oracle_parameters: Any) -> jaydebeapi.Connection:
    user = oracle_parameters.get('user')
    password = oracle_parameters.get('password')
    if user is None:
        user = credentials.get_username()
    if password is None:
        password = credentials.get_password()
    host = oracle_parameters['host']
    port = oracle_parameters['port']
    sid = oracle_parameters['sid']

    conn = stack.enter_context(
        OracleContextManager(
            host,
            user=user,
            password=password,
            port=port,
            sid=sid
        )
    )
    return conn


class OracleLoader(SqlLoader):
    __slots__ = ()

    def __init__(self,
                 sql_query: str,
                 *,
                 credentials: PasswordKeeper,
                 oracle_parameters: Mapping[str, Any] = empty_mapping_proxy,
                 output_validator: DataFrameSchema = AnyDataFrame,
                 **read_sql_kwargs: Any) -> None:

        check_type_compatibility(credentials, PasswordKeeper)
        check_type_compatibility(oracle_parameters, _Mapping, 'Mapping')

        for keyword in ('host', 'port', 'sid'):
            if keyword not in oracle_parameters:
                raise KeyError(f"Parameter 'oracle_parameters' should contain '{keyword}' key")

        super().__init__(
            _oracle_context_creator,
            sql_query,
            context_creator_args=(credentials,),
            context_creator_kwargs=copy(oracle_parameters),
            read_sql_kwargs=read_sql_kwargs,
            output_validator=output_validator
        )

    @final
    @property
    def credentials(self) -> PasswordKeeper:
        return self._context_creator_args[0]

    @final
    @property
    def oracle_parameters(self) -> Dict[str, Any]:
        res = dict(self._context_creator_kwargs)
        if 'password' in res:
            res['password'] = '*****'
        return res


class _GlobalOracleConfigType:
    __slots__ = ()
    __instance: Optional['_GlobalOracleConfigType'] = None
    __OJDBC8_PATH = ''
    try:
        __JVMPath: str = getDefaultJVMPath()
    except JVMNotFoundException:
        warn(
            "No JVM shared library file (libjli.dylib) found. "
            "Try setting up the JAVA_HOME environment variable properly "
            "or setting up the GlobalOracleConfig.JVMPath property manually.",
            RuntimeWarning
        )
        __JVMPath = ''

    def __new__(cls) -> '_GlobalOracleConfigType':
        instance = _GlobalOracleConfigType.__instance
        if instance is None:
            instance = super().__new__(cls)
            _GlobalOracleConfigType.__instance = instance
        return instance

    @property
    def OJDBC8_PATH(self) -> str:
        res = _GlobalOracleConfigType.__OJDBC8_PATH
        if not res:
            raise ValueError('OJDBC8_PATH is not set')
        return res

    @OJDBC8_PATH.setter
    def OJDBC8_PATH(self, value: Union[str, bytes, PathLike]) -> None:
        check_type_compatibility(value, (str, bytes, PathLike))
        _GlobalOracleConfigType.__OJDBC8_PATH = str(value)

    @property
    def JVMPath(self) -> str:
        return _GlobalOracleConfigType.__JVMPath

    @JVMPath.setter
    def JVMPath(self, value: Union[str, bytes, PathLike]) -> None:
        check_type_compatibility(value, (str, bytes, PathLike))
        _GlobalOracleConfigType.__JVMPath = str(value)


GlobalOracleConfig = _GlobalOracleConfigType()
