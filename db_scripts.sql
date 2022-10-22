-- Create database
CREATE DATABASE pebotuwa_maha_vidyalaya
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


-- Create system user table
CREATE TABLE public.system_users
(
    first_name character varying(128) NOT NULL,
    last_name character varying(128) NOT NULL,
    username character varying(64) NOT NULL,
    user_type integer NOT NULL,
    password character varying(255) NOT NULL
);

ALTER TABLE IF EXISTS public.system_users
    OWNER to postgres;


-- Create Teacher table
CREATE TABLE public.teachers
(
    full_name character varying NOT NULL,
    full_name_initials character varying NOT NULL,
    dob character varying(16) NOT NULL,
    nic character varying(16) NOT NULL,
    address character varying(255) NOT NULL,
    distance character varying(255) NOT NULL,
    tp_land character varying(16),
    tp_mobile character varying(16),
    email character varying,
    married_person_name character varying,
    married_person_job character varying,
    original_appointment_date character varying(16),
    grade_class character varying,
    salary_implement_date character varying,
    previous_serviced_schools character varying,
    education_qualifications character varying,
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    status integer NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.teachers
    OWNER to postgres;


-- ******************************************************************
-- System users
-- ******************************************************************

-- Table: public.system_users

-- DROP TABLE IF EXISTS public.system_users;

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


-- ******************************************************************
-- Teachers
-- ******************************************************************

-- Table: public.teachers

-- DROP TABLE IF EXISTS public.teachers;

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