FROM python:3

WORKDIR /zpt-config-service

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

#CMD [ "python", "./main.py" ]


