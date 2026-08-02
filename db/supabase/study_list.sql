-- View: public.study_list

-- DROP VIEW public.study_list;

CREATE OR REPLACE VIEW public.study_list
 AS
 SELECT study_id,
    name,
    sponsor,
    start_date,
    end_date,
    protocol_visits,
    comments,
    ( SELECT count(0) AS count
           FROM patient p
          WHERE p.study_id = s.study_id) AS patients,
    ( SELECT count(0) AS count
           FROM visit v
          WHERE v.study_id = s.study_id) AS visits,
    ( SELECT count(0) AS count
           FROM study_researcher sr
          WHERE sr.study_id = s.study_id) AS researchers,
    ( SELECT count(0) AS count
           FROM adverse_event ae
          WHERE ae.study_id = s.study_id) AS events
   FROM study s;

ALTER TABLE public.study_list
    OWNER TO postgres;

GRANT ALL ON TABLE public.study_list TO anon;
GRANT ALL ON TABLE public.study_list TO authenticated;
GRANT ALL ON TABLE public.study_list TO postgres;
GRANT ALL ON TABLE public.study_list TO service_role;

