-- Create database
CREATE DATABASE pebotuwa_maha_vidyalaya
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


-- System users

DROP TABLE IF EXISTS public.system_users;

CREATE TABLE IF NOT EXISTS public.system_users
(
    first_name character varying(128) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(128) COLLATE pg_catalog."default" NOT NULL,
    username character varying(64) COLLATE pg_catalog."default" NOT NULL,
    user_type integer NOT NULL,
    password character varying(255) COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.system_users
    OWNER to postgres;


-- Teachers

DROP TABLE IF EXISTS public.teachers;

CREATE TABLE IF NOT EXISTS public.teachers
(
    full_name character varying COLLATE pg_catalog."default" NOT NULL,
    full_name_initials character varying COLLATE pg_catalog."default" NOT NULL,
    dob character varying(16) COLLATE pg_catalog."default" NOT NULL,
    nic character varying(16) COLLATE pg_catalog."default" NOT NULL,
    address character varying(255) COLLATE pg_catalog."default" NOT NULL,
    distance character varying(255) COLLATE pg_catalog."default" NOT NULL,
    tp_land character varying(16) COLLATE pg_catalog."default",
    tp_mobile character varying(16) COLLATE pg_catalog."default",
    email character varying COLLATE pg_catalog."default",
    married_person_name character varying COLLATE pg_catalog."default",
    married_person_job character varying COLLATE pg_catalog."default",
    original_appointment_date character varying(16) COLLATE pg_catalog."default",
    grade_class character varying COLLATE pg_catalog."default",
    salary_implement_date character varying COLLATE pg_catalog."default",
    previous_serviced_schools character varying COLLATE pg_catalog."default",
    education_qualifications character varying COLLATE pg_catalog."default",
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    status integer NOT NULL,
    CONSTRAINT teachers_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.teachers
    OWNER to postgres;


-- Insert admin system user
INSERT INTO public.system_users(first_name, last_name, username, user_type, password)
                VALUES ('Admin', 'Admin', 'admin', '1', '21232f297a57a5a743894a0e4a801fc3');