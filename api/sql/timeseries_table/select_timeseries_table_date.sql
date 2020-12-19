SELECT 
      id
    , info
    , CAST(valid_from AS char) 
    , CAST(valid_to AS char) 
    , CAST(modified_at AS char) 
    , changed_by
FROM example.timeseries_table
WHERE 1=1
AND valid_from <= {0}
AND valid_to > {0};