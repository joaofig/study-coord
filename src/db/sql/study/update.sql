UPDATE study SET
    name = COALESCE(?, name)
,   sponsor = COALESCE(?, sponsor)
,   start_date = COALESCE(?, start_date)
,   end_date = COALESCE(?, end_date)
,   protocol_visits = COALESCE(?, protocol_visits)
,   comments = COALESCE(?, comments)
WHERE id = ?
