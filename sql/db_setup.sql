DROP DATABASE data_wellness_companion;

CREATE DATABASE data_wellness_companion
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

DROP TABLE IF EXISTS PUBLIC.TB_SESSION_CONFIGURATION;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTION_SUGGESTIONS;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTION;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTIONNAIRE_STATUS_SUGGESTIONS;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTIONNAIRE_STATUS;


CREATE TABLE PUBLIC.TB_LANGUAGE (
	ID serial NOT NULL,
	LANGUAGE_CODE CHARACTER VARYING(2) NOT NULL UNIQUE,
	PRIMARY KEY (ID)
);

CREATE TABLE PUBLIC.TB_QUESTIONNAIRE_STATUS (
	ID serial NOT NULL,
	SESSION_ID CHARACTER VARYING(36) NOT NULL,
	QUESTION CHARACTER VARYING(65535) NOT NULL,
	ANSWER CHARACTER VARYING(4096) NULL,
	FINAL_REPORT boolean, 
	CREATED_AT TIMESTAMP DEFAULT NOW(),
	UPDATED_AT TIMESTAMP DEFAULT NOW(),
	TOTAL_COST NUMERIC(9, 5) NULL,
	PRIMARY KEY (ID)
);

CREATE TABLE PUBLIC.TB_QUESTION (
	ID serial NOT NULL,
	QUESTION CHARACTER VARYING(1024) NOT NULL,
	PREFERRED_QUESTION_ORDER int NULL,
	LANGUAGE_ID INTEGER NULL,
	PRIMARY KEY (ID),
	CONSTRAINT LANGUAGE_ID
		FOREIGN KEY (LANGUAGE_ID) REFERENCES PUBLIC.TB_LANGUAGE (ID) 
		MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);

-- ALTER TABLE TB_QUESTION ADD LANGUAGE_ID INTEGER NULL;
-- ALTER TABLE TB_QUESTION ADD CONSTRAINT LANGUAGE_ID
--     FOREIGN KEY (LANGUAGE_ID) REFERENCES PUBLIC.TB_LANGUAGE (ID) 
--     MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;

CREATE TABLE PUBLIC.TB_QUESTION_SUGGESTIONS(
	ID serial NOT NULL,
	IMG_SRC CHARACTER VARYING(100) NOT NULL,
	IMG_ALT CHARACTER VARYING(256) NOT NULL,
	TITLE CHARACTER VARYING(256) NOT NULL,
	MAIN_TEXT CHARACTER VARYING(1024) NOT NULL,
	QUESTION_ID integer NOT NULL,
	PRIMARY KEY (ID),
	CONSTRAINT QUESTION_ID
		FOREIGN KEY (QUESTION_ID) REFERENCES PUBLIC.TB_QUESTION (ID) 
		MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID
);

CREATE TABLE PUBLIC.TB_SESSION_CONFIGURATION(
	ID serial NOT NULL,
	SESSION_ID CHARACTER VARYING(36) NOT NULL,
	CONFIG_KEY CHARACTER VARYING(36) NOT NULL,
	CONFIG_VALUE CHARACTER VARYING(255) NOT NULL,
	PRIMARY KEY (ID)
);

CREATE TABLE PUBLIC.TB_QUESTIONNAIRE_STATUS_SUGGESTIONS(
	ID serial NOT NULL,
	QUESTIONNAIRE_STATUS_ID INTEGER NOT NULL,
	MAIN_TEXT CHARACTER VARYING(2048) NOT NULL,
	PRIMARY KEY (ID),
	CONSTRAINT QUESTIONNAIRE_STATUS_ID
		FOREIGN KEY (QUESTIONNAIRE_STATUS_ID) REFERENCES PUBLIC.TB_QUESTIONNAIRE_STATUS (ID) 
		MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);
