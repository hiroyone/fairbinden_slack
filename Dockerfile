FROM ubuntu:latest
RUN apt-get update -y \
    && apt-get install -y python3-pip python3-dev build-essential
    # && cd /usr/local/bin \
    # && ln -s /usr/bin/python3 python \
    # && pip3 install --upgrade pip
COPY . /app
WORKDIR /app 
RUN pip3 install -r requirements.txt
# RUN python3 database_setup.py
# RUN python3 lotsofmenus.py  
ENTRYPOINT ["python3"]
CMD ["main.py"]

