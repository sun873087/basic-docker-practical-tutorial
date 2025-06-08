-- 建立資料庫（如果不存在）
CREATE DATABASE IF NOT EXISTS flask_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用資料庫
USE flask_app;

-- 建立使用者表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入範例資料
INSERT INTO users (name, email) VALUES 
('張小明', 'ming@example.com'),
('李小華', 'hua@example.com'),
('王大同', 'wang@example.com')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 建立索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);