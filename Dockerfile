FROM python:latest

RUN useradd -m -u 1000 user 

COPY requirements.txt . 

RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /home/user/v2tool

RUN chown -R user:user /home/user/v2tool

USER user 

COPY --chown=1000 ./ /home/user/v2tool

EXPOSE 8080

ENTRYPOINT uvicorn main_fastapi:app --host 0.0.0.0 --port 8080