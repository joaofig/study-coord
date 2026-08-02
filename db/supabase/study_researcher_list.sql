-- View: public.study_researcher_list

-- DROP VIEW public.study_researcher_list;

CREATE OR REPLACE VIEW public.study_researcher_list
 AS
 SELECT researcher_id,
    number,
    name,
    phone,
    email,
    comments,
    ( SELECT count(0) AS count
           FROM study_researcher sr
          WHERE sr.researcher_id = r.researcher_id) AS studies,
    created_at,
    created_by,
    updated_at,
    updated_by
   FROM researcher r;

ALTER TABLE public.study_researcher_list
    OWNER TO postgres;

GRANT ALL ON TABLE public.study_researcher_list TO anon;
GRANT ALL ON TABLE public.study_researcher_list TO authenticated;
GRANT ALL ON TABLE public.study_researcher_list TO postgres;
GRANT ALL ON TABLE public.study_researcher_list TO service_role;

