FROM node:20

# Install python 3.11.9
RUN apt-get update && \
    apt-get install -y wget build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev && \
    wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz && \
    tar xzf Python-3.11.9.tgz && \
    cd Python-3.11.9 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.11.9 Python-3.11.9.tgz

# Update pip to the specified version (e.g., pip 21.0.1)
RUN python3.8 -m ensurepip --upgrade && \
    python3.8 -m pip install --upgrade pip==24


COPY backend backend
COPY frontend frontend

# Install Python Packages
RUN python3.11 -m pip install -r backend/requirements.txt
# Editable install
RUN python3.11 -m pip install -e .

# Install Node Packages
RUN cd frontend && npm install

# Expose ports for FastAPI (8000) and Next.js (3000)
EXPOSE 3000

CMD ["sh", "-c", "cd backend && fastapi run examples/chameleon/fastapi_ex.py & cd frontend && npm run dev"]