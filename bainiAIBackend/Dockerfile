# slim means lighweight version of py 3.10
FROM python:3.12-slim 

# curr dir is working dir
WORKDIR /app

# copy all the files in 'app'
COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# port for fast API
EXPOSE 8000

# run fastapi app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


