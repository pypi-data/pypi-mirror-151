from contextlib import ExitStack
from os import environ, PathLike
from typing import Optional, Union, Callable, Tuple, Mapping, Any

from pandakeeper.dataloader.sql import SqlLoader
from pandas import DataFrame
from pandas import read_sql
from pandera import DataFrameSchema
from pyspark import SparkConf, SparkContext
from typing_extensions import Final, final
from varutils.plugs.constants import empty_mapping_proxy
from varutils.types import NoneType
from varutils.typing import check_type_compatibility, get_fully_qualified_name

from sber_ld_dbtools.credentials import PasswordKeeper, set_default_kerberos_principal

__all__ = (
    'SparkBaseLoader',
    'GlobalSparkConfig',
    'DEFAULT_SPARK_CONF'
)


def _spark_context_creator(stack: ExitStack,
                           credentials: PasswordKeeper,
                           conf: Optional[SparkConf] = None) -> SparkContext:
    set_default_kerberos_principal(credentials)
    return stack.enter_context(SparkContext.getOrCreate(conf))


class SparkBaseLoader(SqlLoader):
    __slots__ = ()

    def __init__(self,
                 sql_query: str,
                 *,
                 credentials: PasswordKeeper,
                 conf: Optional[SparkConf] = None,
                 read_sql_fn: Callable[..., DataFrame] = read_sql,
                 read_sql_args: Tuple[Any, ...] = (),
                 read_sql_kwargs: Mapping[str, Any] = empty_mapping_proxy,
                 output_validator: DataFrameSchema) -> None:
        check_type_compatibility(credentials, PasswordKeeper)
        check_type_compatibility(conf, (SparkConf, NoneType), f'{get_fully_qualified_name(SparkConf)} or None')

        super().__init__(
            _spark_context_creator,
            sql_query,
            context_creator_args=(credentials, conf),
            read_sql_fn=read_sql_fn,
            read_sql_args=read_sql_args,
            read_sql_kwargs=read_sql_kwargs,
            output_validator=output_validator
        )

    @final
    @property
    def credentials(self) -> PasswordKeeper:
        return self._context_creator_args[0]

    @final
    @property
    def conf(self) -> Optional[SparkConf]:
        return self._context_creator_args[1]


DEFAULT_SPARK_CONF: Final = (
    SparkConf()
        .setAppName('DownloadRawData')
        .setMaster("yarn-client")
        .set('spark.dynamicAllocation.enabled', 'false')
        .set('spark.local.dir', '.sparktmp')
        .set('spark.executor.memory', '6g')
        .set('spark.executor.cores', '2')
        .set('spark.executor.instances', '50')
        .set('spark.sql.parquet.mergeScheme', 'false')
        .set('parquet.enable.summary-metadata', 'false')
        .set('spark.yarn.executor.memoryOverhead', '6048mb')
        .set('spark.driver.memory', '90g')
        .set('spark.driver.maxResultSize', '90g')
        .set('spark.yarn.driver.memoryOverhead', '6048mb')
        .set('spark.port.maxRetries', '150')
        .set('spark.dynamicAllocation.enabled', 'false')
        .set('spark.kryoserializer.buffer.max', '1g')
        .set('spark.core.connection.ack.wait.timeout', '800s')
        .set('spark.akka.timeout', '800s')
        .set('spark.storage.blockManagerSlaveTimeoutMs', '800s')
        .set('spark.shuffle.io.connectionTimeout', '800s')
        .set('spark.rpc.askTimeout', '800s')
        .set('spark.network.timeout', '800s')
        .set('spark.rpc.lookupTimeout', '800s')
        .set('spark.sql.crossJoin.enabled', 'True')
        .set('spark.sql.autoBroadcastJoinThreshold', -1)
)


class _GlobalSparkConfigType:
    __slots__ = ()
    __instance: Optional['_GlobalSparkConfigType'] = None

    def __new__(cls) -> '_GlobalSparkConfigType':
        instance = _GlobalSparkConfigType.__instance
        if instance is None:
            instance = super().__new__(cls)
            _GlobalSparkConfigType.__instance = instance
        return instance

    @property
    def SPARK_HOME(self) -> Optional[str]:
        return environ.get('SPARK_HOME')

    @SPARK_HOME.setter
    def SPARK_HOME(self, value: Union[str, bytes, PathLike]) -> None:
        check_type_compatibility(value, (str, bytes, PathLike))
        environ['SPARK_HOME'] = str(value)

    @property
    def PYSPARK_DRIVER_PYTHON(self) -> Optional[str]:
        return environ.get('PYSPARK_DRIVER_PYTHON')

    @PYSPARK_DRIVER_PYTHON.setter
    def PYSPARK_DRIVER_PYTHON(self, value: str) -> None:
        check_type_compatibility(value, str)
        environ['PYSPARK_DRIVER_PYTHON'] = value

    @property
    def PYSPARK_PYTHON(self) -> Optional[str]:
        return environ.get('PYSPARK_PYTHON')

    @PYSPARK_PYTHON.setter
    def PYSPARK_PYTHON(self, value: Union[str, bytes, PathLike]) -> None:
        check_type_compatibility(value, (str, bytes, PathLike))
        environ['PYSPARK_PYTHON'] = str(value)


GlobalSparkConfig = _GlobalSparkConfigType()
