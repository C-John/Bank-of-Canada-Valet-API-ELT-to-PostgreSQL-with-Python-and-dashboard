# Use the official Microsoft Python image
FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Install libpq-dev so psycopg can connect to PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set the working directory inside the container
WORKDIR /workspaces/currency-project