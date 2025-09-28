--  Copyright 2025 TecOnca Data Solutions.

SELECT 
    ${fields}
    , CAST(CURRENT_TIMESTAMP AS VARCHAR) as insertionDateTime
FROM ${{ database_name }}.${table_name}