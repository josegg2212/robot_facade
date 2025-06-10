FROM python:3.9.18

WORKDIR /home/code


ENV PYTHONDONTWRITEBYTECODE=1
ENV CUDA_VISIBLE_DEVICES=-1

COPY ./docker/requirements.in /home/requirements.in

RUN pip install --upgrade pip
RUN pip install -r /home/requirements.in

RUN pip install --no-cache-dir -r requirements.in | true


CMD ["python3", "-u","/home/code/robot_facade.py"]

