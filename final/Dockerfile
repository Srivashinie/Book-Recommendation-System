# Use the Python version of alpine as the base image
FROM python:3.12-alpine

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="sridhamo@pdx.edu"

# Install build dependencies
RUN apk --no-cache add build-base libffi-dev openssl-dev

# Copy the contents of the current directory into the container directory /app
COPY . /app

# Set the working directory of the container to /app
WORKDIR /app

# Upgrade pip
RUN pip3 install --upgrade pip

# Install the build dependencies for multidict
RUN apk add --no-cache --virtual .build-deps \
    build-base \
    openssl-dev \
    libffi-dev

# Install the Python packages specified by requirements.txt into the container
RUN pip3 install --no-cache-dir -r requirements.txt

# Remove build dependencies
RUN apk del .build-deps

# Set the program that is invoked upon container instantiation
ENTRYPOINT ["python3"]

# Set the parameters to the program
CMD ["app.py"]
