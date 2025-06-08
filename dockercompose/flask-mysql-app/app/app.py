from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)

# 資料庫連接配置
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'database'),
    'user': os.environ.get('DB_USER', 'appuser'),
    'password': os.environ.get('DB_PASSWORD', 'apppass'),
    'database': os.environ.get('DB_NAME', 'flask_app'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def get_db_connection():
    """建立資料庫連接，包含重試機制"""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            return connection
        except mysql.connector.Error as e:
            print(f"資料庫連接失敗 (嘗試 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # 等待 5 秒後重試
            else:
                raise

@app.route('/')
def home():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 查詢使用者資料
        cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('index.html', users=users)
    except Exception as e:
        return render_template('index.html', users=[], error=str(e))

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        
        if not name or not email:
            return jsonify({'success': False, 'error': '姓名和電子郵件為必填欄位'})
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (name, email)
        )
        connection.commit()
        
        user_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'user_id': user_id, 'message': '使用者新增成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        connection.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': time.time()
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)