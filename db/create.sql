DROP DATABASE IF EXISTS devdb;
CREATE DATABASE devdb;
\connect devdb;
CREATE SCHEMA "user";

DROP DATABASE IF EXISTS testdb;
CREATE DATABASE testdb;
\connect testdb;
CREATE SCHEMA "user";
