# 1. Start with an official Python base image.
# This line gives a lightweight Linux OS with Python and pip pre-installed.

FROM python:3.11-slim

# 2. Set the working directory inside the container.
# This is where the code will live and run.
WORKDIR /app

# 3. Copy the dependencies list into the container.
COPY requirements.txt .

# 4. Install the Python libraries needed by the script.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all the local Python scripts into the container
COPY *.py ./

# 6. This is the command that will run when the container starts.
# Set the "entrypoint" to be "python" and the default command to be the script.
ENTRYPOINT ["python", "log_analyser.py"]

