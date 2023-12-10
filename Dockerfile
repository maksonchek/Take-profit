FROM ubuntu 

COPY Backend/src/ /opt/
COPY Algorithm /opt/

WORKDIR /opt/

RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip \ 
    rar \
    unrar

RUN pip install -r requirements.txt
CMD ["python3", "app.py"]