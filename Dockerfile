# 使用官方的 Python 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件到工作目录
COPY requirements.txt /app/

# 使用 pip 安装 requirements.txt 中的依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 复制整个应用程序到工作目录
COPY . /app/

# 暴露容器的 8000 端口供外部访问
EXPOSE 7788

# 运行 FastAPI 应用程序
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7788"]