# Use the official Python image as the base
FROM python:alpine
# defining the directory

WORKDIR /work

#copy the contents to the working dir
COPY . /work

# Setting the path for env variable
ENV PYTHONPATH=~/work/app/

#running all the dependencies
RUN pip install --upgrade pip

# Install the required dependencies
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Set the entrypoint command
CMD ["python", "run.py"]