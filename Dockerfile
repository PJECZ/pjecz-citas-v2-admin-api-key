FROM python:3.11

WORKDIR /
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8005

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:8005", "-k", "uvicorn.workers.UvicornWorker", "citas_v2_admin.app:create_app" ]
