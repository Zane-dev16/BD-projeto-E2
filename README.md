# Projeto Base de Dados E2

The second university project in Databases

## Usage guide

### Prerequisites

- Docker installed on your machine. Find the installation here at [https://www.docker.com/get-started/](https://www.docker.com/get-started/)


1. Follow Lab-01 guides to run bdist-workplace
   
2. Copy E2-report-76.ipynb in the bdist-workplace/work

3. Run and make changes to the notebook in the bdist environment

## Contribution Guide

1. After making changes to the E2-report-76.ipynb in the bdist environment copy and update the E2-report-76.ipynb in this repository.

2. Once you're ready, commit and push your changes.

## How to run on your local machine

This guide will walk you through the necessary steps to set up the project locally


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
