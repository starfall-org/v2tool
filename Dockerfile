FROM python:latest

RUN useradd -m -u 1000 user 

COPY requirements.txt . 

RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /home/user/api

RUN chown -R user:user /home/user/api

USER user 

COPY --chown=1000 ./ /home/user/api

EXPOSE 8080

ENTRYPOINT gunicorn -b 0.0.0.0:8080 main:app