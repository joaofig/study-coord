-- Table: public.study

DROP TABLE IF EXISTS public.study;

CREATE TABLE IF NOT EXISTS public.study
(
    study_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(128) COLLATE pg_catalog."default" NOT NULL,
    sponsor character varying(128) COLLATE pg_catalog."default" NOT NULL,
    start_date date NOT NULL DEFAULT now(),
    end_date date,
    protocol_visits integer NOT NULL DEFAULT 0,
    comments text COLLATE pg_catalog."default",
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) COLLATE pg_catalog."default" NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT study_pkey PRIMARY KEY (study_id),
    CONSTRAINT study_name_key UNIQUE (name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.study
    OWNER to "creepy-aquamarine-tortoise";
