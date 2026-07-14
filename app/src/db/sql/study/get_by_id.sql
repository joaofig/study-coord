SELECT      id
,           name
,           sponsor
,           start_date
,           end_date
,           protocol_visits
,           comments
FROM        study
WHERE       id = ?;
