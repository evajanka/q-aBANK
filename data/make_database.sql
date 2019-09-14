DROP TABLE IF EXISTS guestions;
DROP TABLE IF EXISTS answers;

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    submission_time INTEGER NOT NULL,
    vote_number INTEGER NOT NULL,
    question_id character varying NOT NULL,
    message character varying NOT NULL,
    image character varying NOT NULL
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    submission_time INTEGER NOT NULL,
    view_number INTEGER varying NOT NULL,
    vote_number INTEGER varying NOT NULL,
    title character varying NOT NULL,
    message character varying NOT NULL,
    image character varying NOT NULL
);

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at timestamp default NULL
);


