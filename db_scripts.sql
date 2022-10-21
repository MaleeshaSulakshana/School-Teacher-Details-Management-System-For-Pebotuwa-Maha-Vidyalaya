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
    id integer,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.teachers
    OWNER to postgres;