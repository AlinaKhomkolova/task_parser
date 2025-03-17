DROP TABLE IF EXISTS problem_tags;
DROP TABLE IF EXISTS problems;
DROP TABLE IF EXISTS tags;

-- Создание таблицы для хранения тегов
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Создание таблицы для хранения задач
CREATE TABLE IF NOT EXISTS problems (
    id SERIAL PRIMARY KEY,
    contest_id INT NOT NULL,
    index VARCHAR(15) NOT NULL,
    name VARCHAR(255) NOT NULL,
    rating SMALLINT,
    solved_count INT,
    UNIQUE (contest_id, index)
);

-- Создание таблицы для связи задач и тегов
CREATE TABLE IF NOT EXISTS problem_tags (
    problem_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (problem_id, tag_id),
    FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);