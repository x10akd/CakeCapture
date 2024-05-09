# 16th-CakeCapture
## 環境變數設定與使用
1. 使用 `$ poetry install` 安裝環境變數套件 django-environ
2. 在 core 資料夾中，使用 `$ touch .env` 建立 .env 檔案，並確保該檔案沒有被版控
3. 編輯 .env 檔案，並加入自己本機端的資訊，範例如下：
    ```py
    # in .env
    # 以下皆不用加引號
    SECRET_KEY= # settings.py 的 SECRET_KEY
    DB_NAME= # Database 的名稱，如：cakecapture_db
    DB_USER= # PostgreSQL 的使用者名稱，如：postgres
    DB_PASSWORD= # PostgreSQL 的使用者密碼，預設應該為空白
    DB_HOST= # PostgreSQL 的伺服器，預設為 localhost
    DB_PORT= # PostgreSQL 的端口號，預設為 5432
    ```
