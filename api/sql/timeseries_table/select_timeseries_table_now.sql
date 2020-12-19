SELECT 
      id
    , info
    , CAST(valid_from AS char) 
    , CAST(valid_to AS char) 
    , CAST(modified_at AS char) 
    , changed_by
FROM example.vt_timeseries_table;