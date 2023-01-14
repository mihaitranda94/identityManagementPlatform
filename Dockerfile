FROM python:3.9
WORKDIR /home/web
ADD requirements /home/web/requirements
ADD idmdemo /home/web/idmdemo
RUN pip install -r requirements/dev.txt
WORKDIR /home/web/idmdemo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
 
