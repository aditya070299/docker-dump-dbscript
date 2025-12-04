FROM postgres:15

# Install python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Create backups directory
RUN mkdir /backups

# Copy script and requirements
COPY backup.py /backup.py
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip3 install -r /requirements.txt

# Run both PostgreSQL + backup script
CMD ["bash", "-c", "\
    python3 /backup.py & \
    docker-entrypoint.sh postgres \
"]
