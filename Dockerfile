FROM nikolaik/python-nodejs

# Update pip to the specified version (e.g., pip 21.0.1)
RUN python -m ensurepip --upgrade && \
    python -m pip install --upgrade pip==24

COPY backend backend
COPY frontend frontend
COPY entrypoint.sh entrypoint.sh

# Install Python Packages
RUN cd backend && pip install -r requirements.txt && pip install -e .

# Install Node Packages
RUN cd frontend && npm install

ENTRYPOINT ["sh", "entrypoint.sh"]
