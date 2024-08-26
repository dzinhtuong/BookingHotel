# Use the official Python image as a base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./requirements.txt /app/requirements.txt

# Install any dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary


# Copy the project files to the working directory
COPY . /app

# Expose the port that Django will run on
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
