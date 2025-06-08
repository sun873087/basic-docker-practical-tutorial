# 基礎 Docker 實作教學(第三部分：Dockerfile 實作)

課程時間：25 分鐘

- Dockerfile 基本結構與常用指令
- 實作練習：建立自定義 Web 應用

---

## Dockerfile 基本結構與常用指令

### ✨什麼是 Dockerfile？

Dockerfile 是一個文本檔案，包含了一系列的指令和參數，用來自動化建立 Docker 映像檔。透過 Dockerfile，我們可以定義：
- 從哪個基礎映像開始
- 需要安裝哪些軟體和套件
- 如何配置應用程式環境
- 容器啟動時要執行什麼指令

簡單來說，Dockerfile 就像是建立映像檔的「食譜」，告訴 Docker 如何一步步製作出我們想要的應用環境。

### 🏗️ Dockerfile 基本結構

一個標準的 Dockerfile 通常包含以下結構：

```dockerfile
# 註解：從基礎映像開始
FROM base_image:tag

# 設定工作目錄
WORKDIR /app

# 複製檔案到容器
COPY source destination

# 安裝套件或執行指令
RUN command

# 暴露端口
EXPOSE port

# 設定容器啟動指令
CMD ["executable", "param1", "param2"]
```

### 📋 常用 Dockerfile 指令詳解

#### 1. FROM - 指定基礎映像
```dockerfile
# 使用官方 Python 映像作為基礎
FROM python:3.9

# 使用 Ubuntu 作為基礎映像
FROM ubuntu:20.04

# 使用輕量級的 Alpine Linux
FROM alpine:latest
```
**說明**：FROM 指令必須是 Dockerfile 的第一個指令（除了註解），用來指定基礎映像。

#### 2. WORKDIR - 設定工作目錄
```dockerfile
# 設定工作目錄為 /app
WORKDIR /app

# 後續的指令都會在這個目錄下執行
COPY . .
RUN pip install -r requirements.txt
```
**說明**：設定容器內的工作目錄，如果目錄不存在會自動建立。

#### 3. COPY vs ADD - 複製檔案
```dockerfile
# COPY：複製本地檔案到容器
COPY app.py /app/
COPY requirements.txt /app/
COPY . /app/

# ADD：功能更強大，支援 URL 和自動解壓縮
ADD https://example.com/file.tar.gz /app/
ADD archive.tar.gz /app/
```
**最佳實踐**：優先使用 COPY，只有需要特殊功能時才使用 ADD。

#### 4. RUN - 執行指令
```dockerfile
# 安裝套件
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim

# 安裝 Python 套件
RUN pip install -r requirements.txt

# 建立目錄
RUN mkdir -p /app/logs
```
**注意**：每個 RUN 指令會建立一個新的映像層，盡量將相關指令合併到一個 RUN 中。

#### 5. EXPOSE - 聲明端口
```dockerfile
# 聲明應用程式使用的端口
EXPOSE 8000
EXPOSE 80 443
```
**說明**：EXPOSE 只是聲明端口，實際運行時還需要用 -p 參數映射端口。

#### 6. ENV - 設定環境變數
```dockerfile
# 設定環境變數
ENV PYTHON_VERSION=3.9
ENV APP_HOME=/app
ENV DEBUG=False

# 使用環境變數
WORKDIR $APP_HOME
```

#### 7. CMD vs ENTRYPOINT - 容器啟動指令
```dockerfile
# CMD：可被 docker run 參數覆蓋
CMD ["python", "app.py"]
CMD python app.py

# ENTRYPOINT：不會被覆蓋，docker run 參數會作為額外參數
ENTRYPOINT ["python", "app.py"]

# 組合使用
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8000"]
```

### 🎯 Dockerfile 最佳實踐

1. **使用適當的基礎映像**：選擇最小且安全的基礎映像
2. **善用多階段建構**：減少最終映像大小
3. **合併 RUN 指令**：減少映像層數
4. **使用 .dockerignore**：排除不必要的檔案
5. **不要在容器中儲存敏感資料**：使用環境變數或掛載卷

---

## 實作練習：建立自定義 Web 應用

在這個實作練習中，我們將建立一個簡單的 Python Flask Web 應用，並使用 Dockerfile 將它容器化。這個練習將幫助您掌握 Dockerfile 的撰寫和應用，並學會如何建立和運行自定義 Docker 映像。

### 🎯 練習目標
- 建立一個簡單的 Flask Web 應用
- 撰寫 Dockerfile 來容器化應用
- 建立並運行自定義 Docker 映像
- 測試應用程式功能
- 學習故障排除技巧

### 📁 步驟 1：建立應用程式檔案 & 撰寫 Dockerfile

首先，讓我們建立一個簡單的 Flask Web 應用 和 `Dockerfile`，因教學時間關係，我們將使用 GitHub 上的範例專案。請參考[基礎 Docker 實作教學 第 1 部分：快速入門](基礎%20Docker%20實作教學%20第%201%20部分：快速入門.md)中的範例。檔案結構：
```
flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── templates/
    └── index.html
```
**`.dockerignore` 文件：**

用於排除不必要的檔案，可至 [Docker 官方文件](https://docs.docker.com/engine/reference/builder/#dockerignore-file)查詢

**`Dockerfile` 文檔說明：**
```dockerfile
# 使用官方 Python 3.9 映像作為基礎
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Python 套件
# 先複製 requirements.txt 可以利用 Docker 快取機制
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安裝 procps 套件（提供 ps 指令）
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

# 複製應用程式代碼
COPY . .

# 建立非 root 使用者（安全最佳實踐）
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# 聲明應用程式端口
EXPOSE 5000

# 設定環境變數
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 健康檢查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 設定容器啟動指令
CMD ["python", "app.py"]
```



### 🔨 步驟 3：建立 Docker 映像

使用以下指令建立 Docker 映像：

```bash
# 建立映像（注意最後有個點）
docker build -t flask-demo:v1.0 .

# 查看建立的映像
docker images | grep flask-demo
```

**建立過程說明：**
- `-t flask-demo:v1.0`：為映像指定名稱和標籤
- `.`：指定建立內容為當前目錄

### 🚀 步驟 4：運行容器

運行我們剛建立的容器：

```bash
# 運行容器，映射端口到本機 8080
docker run -d -p 8080:5000 --name my-flask-app flask-demo:v1.0

# 查看容器狀態
docker ps

# 查看容器日誌
docker logs my-flask-app
```

### 🧪 步驟 5：測試應用程式

**測試網頁介面：**
- 在 Play with Docker 中，點擊端口 8080 連結
- 或在瀏覽器中訪問顯示的 URL

**測試 API 端點：**
```bash
# 健康檢查端點
curl http://localhost:8080/health

# 應用資訊端點
curl http://localhost:8080/api/info
```

**進入容器查看：**
```bash
# 進入容器內部
docker exec -it my-flask-app bash

# 查看應用檔案
ls -la /app

# 查看進程
ps aux

# 離開容器
exit

# 停止容器
docker stop my-flask-app

# 刪除容器
docker rm my-flask-app
```

### 🛠️ 故障排除和常見問題

#### 1. 容器無法啟動
```bash
# 查看容器日誌
docker logs my-flask-app

# 查看容器詳細資訊
docker inspect my-flask-app
```

#### 2. 端口無法訪問
```bash
# 檢查端口映射
docker port my-flask-app

# 確認容器是否在運行
docker ps
```

#### 3. 映像建立失敗
```bash
# 查看建立過程的詳細輸出
docker build -t flask-demo:v1.0 . --no-cache --progress=plain

# 檢查 Dockerfile 語法
cat Dockerfile
```

#### 4. 依賴套件安裝問題
```bash
# 進入容器除錯
docker run -it flask-demo:v1.0 bash

# 手動測試安裝
pip install -r requirements.txt
```

### 📈 進階練習

完成基本練習後，可以嘗試以下進階功能：

1. **修改應用程式**：
```bash
# 停止目前容器
docker stop my-flask-app
docker rm my-flask-app

# 修改 app.py，新增功能後重新建立映像
docker build -t flask-demo:v2.0 .
docker run -d -p 8080:5000 --name my-flask-app-v2 flask-demo:v2.0
```

2. **環境變數配置**：
```bash
# 使用環境變數運行
docker run -d -p 8080:5000 -e PORT=5000 -e FLASK_ENV=development --name flask-dev flask-demo:v1.0
```

3. **掛載本機目錄**：
```bash
# 掛載本機代碼目錄，便於開發
docker run -d -p 8080:5000 -v $(pwd):/app --name flask-dev flask-demo:v1.0
```

### 🎉 練習總結

透過這個實作練習，您已經學會了：

✅ 建立 Python Flask Web 應用
✅ 撰寫完整的 Dockerfile
✅ 使用 Docker 建立自定義映像
✅ 運行和測試容器化應用
✅ 基本的故障排除技巧
✅ Docker 最佳實踐應用

**清理資源：**
```bash
# 停止並刪除容器
docker stop my-flask-app
docker rm my-flask-app

# 刪除映像（可選）
docker rmi flask-demo:v1.0
```

這個練習展示了 Docker 容器化的完整流程，從應用開發到部署的每個步驟。掌握這些技能後，您就可以將任何應用程式容器化，為進階的 Docker 應用和 Kubernetes 部署打下堅實的基礎！🚀