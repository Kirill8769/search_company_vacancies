-- Создаём таблицу employers

CREATE TABLE IF NOT EXISTS employers (
    id SERIAL PRIMARY KEY,
    employer_id VARCHAR(16) UNIQUE NOT NULL,
    name VARCHAR(64),
    url VARCHAR(128),
    open_vacancies INTEGER
);


-- Создаём таблицу vacancies с привязкой к employers по employer_id
CREATE TABLE IF NOT EXISTS vacancies (
    id SERIAL PRIMARY KEY,
    vacancy_id VARCHAR(16) UNIQUE NOT NULL,
    employer_id VARCHAR(16),
    name VARCHAR(512),
    area VARCHAR(64),
    url VARCHAR(128),
    salary_from INT,
    salary_to INT,
    currency VARCHAR(16),
    status VARCHAR(32),
    published_date TIMESTAMP,
    description TEXT,
    FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
    ON DELETE CASCADE
);