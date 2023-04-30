FROM python:3.9.6

WORKDIR /MBERTAPIEndpoints
COPY ./requirements.txt /MBERTAPIEndpoints/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /MBERTAPIEndpoints/requirements.txt

COPY . /MBERTAPIEndpoints/API
EXPOSE 8000
CMD ["uvicorn", "API.main:app", "--host", "0.0.0.0", "--port", "8000"]