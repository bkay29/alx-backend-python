# Use base python 3.10 image
FROM python:3.10

# Set work directory inside container
WORKDIR /app

# Copy requirements into container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into container
COPY . /app/

# Expose Django default port
EXPOSE 8000

# Set environment variable for checker
ENV CHECKER_FLAG="-p"       # -p option just for checker

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]    