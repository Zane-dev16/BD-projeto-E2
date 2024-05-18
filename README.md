# Projeto Base de Dados E2

The second university project in Databases

## Usage Guide

This guide will walk you through the necessary steps to set up and verify the database.

### Prerequisites

- Docker installed on your machine. Find the installation here at [https://www.docker.com/get-started/](https://www.docker.com/get-started/)

### Instructions

1. Clone the repository to your local machine:

```bash
git clone https://github.com/Zane-dev16/BD-projeto-E2
```

2. Navigate to the directory of the repository:

```bash
cd /path/to/bd_proj_e2
```

3. Start the Docker containers using Docker Compose:

```bash
docker-compose up
```

4. Once the containers are up and running, access the PostgreSQL container by executing:

```bash
docker exec -it bd_proj_e2 bash
```

5. Within the container, login to the PostgreSQL database using the following command:

```bash
psql -U postgres
```

6. You are now logged into the PostgreSQL database. To verify that the database is populated with tables, execute the following command:

```sql
\dt
```
This command will display a list of all tables in the database.

## Contribution Guide

1. Note that `psql` commands will only affect the instance of the database that you are connected to locally. psql can be used to interact with the PostgreSQL database for testing purposes and will not be recorded into version control.

2. To contribute, place SQL queries in existing SQL files or create a new SQL file in the `data/` folder.

3. You can verify the changes made through your added SQL code by restarting the container. 

4. Once you're changes are ready, commit and push them to the repository.
