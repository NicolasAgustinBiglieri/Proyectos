
### Ejemplo de Archivo `create_users_table.sql`

```sql
CREATE DATABASE my_new_api_db;
\c my_new_api_db
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    dateofbirth DATE,
    country VARCHAR(255),
    city VARCHAR(255),
    email_verif BOOLEAN DEFAULT FALSE,
    registered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password VARCHAR(255) NOT NULL
);
