# Python Base
FROM python:3.12.10-slim

# Directory
WORKDIR /dcc

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source code
COPY src ./src

# Port
EXPOSE 8080

# Run main script
CMD ["python", "src/main.py"]
