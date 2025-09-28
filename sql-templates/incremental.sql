--  Copyright 2025 TecOnca Data Solutions.

SELECT 
    ${fields}
    , CAST(CURRENT_TIMESTAMP AS VARCHAR) as insertionDateTime
FROM ${{ database_name }}.${table_name}
WHERE  CAST(${update} AS DATE) BETWEEN 'start_date' AND 'end_date'
    OR CAST(${create} AS DATE) BETWEEN 'start_date' AND 'end_date'
