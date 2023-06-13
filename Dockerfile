FROM python:3.8 
# WORKDIR： 文件在容器中的存储路径
WORKDIR /Flask/demo  

COPY requirements.txt ./
RUN pip install -r requirements.txt 

COPY . .

CMD ["gunicorn", "app_helloWorld:app", "-c", "./guni.conf.py"]