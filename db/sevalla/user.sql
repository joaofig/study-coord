-- Table: public.user

-- DROP TABLE IF EXISTS public."user";

CREATE TABLE IF NOT EXISTS public."user"
(
    user_id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    user_name character varying(64) COLLATE pg_catalog."default" NOT NULL,
    pass_hash character varying(64) COLLATE pg_catalog."default" NOT NULL,
    user_role character varying(64) COLLATE pg_catalog."default" NOT NULL,
    change_pass boolean NOT NULL DEFAULT false,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    created_by character varying(64) COLLATE pg_catalog."default" NOT NULL,
    updated_at timestamp without time zone NOT NULL DEFAULT now(),
    updated_by character varying(64) COLLATE pg_catalog."default" NOT NULL,

    CONSTRAINT user_pkey PRIMARY KEY (user_id),
    CONSTRAINT user_user_name_key UNIQUE (user_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."user"
    OWNER to "creepy-aquamarine-tortoise";
-- Index: index_user_pass

-- DROP INDEX IF EXISTS public.index_user_pass;

CREATE UNIQUE INDEX IF NOT EXISTS index_user_pass
    ON public."user" USING btree
    (user_name COLLATE pg_catalog."default" ASC NULLS LAST, pass_hash COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;


INSERT INTO public."user" (user_name, pass_hash, user_role, change_pass, created_by, updated_by)
VALUES ('admin', '299390b0010c72e591e83f0679d04a49304c9e40c31c4fc8ebad257f82db5ee8',
        'Admin', false, 'system', 'system');
