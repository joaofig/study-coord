-- View: public.researcher_list

-- DROP VIEW public.researcher_list;

CREATE OR REPLACE VIEW public.researcher_list
 AS
 SELECT researcher_id,
    number,
    name,
    phone,
    email,
    comments,
    ( SELECT count(0) AS count
           FROM study_researcher sr
          WHERE sr.researcher_id = r.researcher_id) AS study_count,
    created_at,
    created_by,
    updated_at,
    updated_by
   FROM researcher r;

ALTER TABLE public.researcher_list
    OWNER TO postgres;

GRANT ALL ON TABLE public.researcher_list TO anon;
GRANT ALL ON TABLE public.researcher_list TO authenticated;
GRANT ALL ON TABLE public.researcher_list TO postgres;
GRANT ALL ON TABLE public.researcher_list TO service_role;

