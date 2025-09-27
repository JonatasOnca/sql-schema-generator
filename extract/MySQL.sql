--  Copyright 2025 TecOnca Data Solutions.

use {{ database_name }};

select  
    info.TABLE_NAME
    , info.COLUMN_NAME
    , info.DATA_TYPE
    , const.CONSTRAINT_TYPE
from INFORMATION_SCHEMA.COLUMNS info 
left join INFORMATION_SCHEMA.KEY_COLUMN_USAGE use_name
ON 
    use_name.TABLE_NAME = info.TABLE_NAME 
    and use_name.COLUMN_NAME = info.COLUMN_NAME
left join INFORMATION_SCHEMA.TABLE_CONSTRAINTS const
ON    
    info.TABLE_NAME = const.TABLE_NAME
    and use_name.COLUMN_NAME = info.COLUMN_NAME
    and use_name.CONSTRAINT_NAME = const.CONSTRAINT_NAME
where info.TABLE_NAME in (
    ${tables}
);
