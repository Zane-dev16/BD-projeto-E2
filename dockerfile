FROM postgres:latest

# Set environment variables
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=mydatabase

# Copy initialization script
COPY data/ /docker-entrypoint-initdb.d/
