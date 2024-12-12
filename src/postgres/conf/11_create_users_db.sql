--init.sql


CREATE DATABASE users;

\c users;


-- Table "users"
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY UNIQUE,
  username VARCHAR(25) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  role INTEGER NOT NULL,
  verified BOOLEAN DEFAULT FALSE
);


-- Table "user_infos"
CREATE TABLE IF NOT EXISTS user_infos (
  user_id UUID PRIMARY KEY UNIQUE,
  address VARCHAR(255),
  zipcode INTEGER,
  city VARCHAR(100),
  country VARCHAR(25),
  phone VARCHAR(15),
  email VARCHAR(255),
  CONSTRAINT fk_user_infos_user_id
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
);


-- Table "user_logs"
CREATE TABLE IF NOT EXISTS user_logs (
  user_id UUID PRIMARY KEY UNIQUE,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  last_login TIMESTAMP NOT NULL,
  CONSTRAINT fk_user_logs_user_id
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
);


-- Table "roles"
CREATE TABLE IF NOT EXISTS roles (
  id SERIAL PRIMARY KEY UNIQUE,
  role VARCHAR(30) UNIQUE NOT NULL
);



-- Add foreign key constraint to users table
ALTER TABLE IF EXISTS users
ADD CONSTRAINT fk_users_role
FOREIGN KEY (role) REFERENCES roles(id);


-- Add default roles
INSERT INTO roles (role) VALUES ('basic'), ('premium'), ('admin');