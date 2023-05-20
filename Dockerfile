FROM python:3.8

# defining the directory
WORKDIR /work
#copy the contents to the working dir
COPY . /work

#running all the dependencies
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python"]
# command to start the container
CMD python ./run.py