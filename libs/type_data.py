_INTEGER = [
    'int',
    'int64',
    'integer',
    'bigint',
    'mediumint',
    'smallint',
    'tinyint',
]

_BOOL = [
    'bool',
    'boolean',
]

_STRING = [
    'varchar',
    'nvarchar',
    'char',
    'bit',
    'varbinary',
    'binary',
    'tinyblob',
    'tinytext',
    'text',
    'blob',
    'mediumtext',
    'mediumblob',
    'longtext',
    'longblob',
    'enum',
]

_DATE_DATETIME = [
    'smalldatetime',
    'datetime',
    'datetime2',
]

_DATE_DATE = [
    'date',
]

_DATE_TIMESTAMP = [
    'timestamp',
]
_DATE_CUSTOM = [
    'time',
    'year',
]

_DATE = _DATE_DATETIME + _DATE_DATE + _DATE_TIMESTAMP + _DATE_CUSTOM

_NUMERIC = [
    'numeric',
    'dec',
    'decimal',
    'double precision',
    'double',
    'float',
]

_JSON = [
    'json',
]