FROM python:3.8

ADD main.py .

RUN pip install requests python-time pysqlite3 pandas urllib3 openpyxl

CMD ["python", "main.py"]