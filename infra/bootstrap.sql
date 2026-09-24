-- Local development credentials only; database is bound to loopback.
CREATE ROLE ehr_app LOGIN PASSWORD 'local-development' NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
ALTER USER ehr_owner PASSWORD 'local-owner';
CREATE DATABASE ehr OWNER ehr_owner;
CREATE DATABASE ehr_test OWNER ehr_owner;
