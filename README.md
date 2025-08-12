<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#configuration">Installation</a></li>
      </ul>
    </li>
    <li><a href="#database-setup">Database Setup</a></li>
    <li><a href="#environment-configuration">Environment Configuration</a></li>
    <li><a href="#build-and-run">Build And Run</a></li>
  </ol>
</details>

### About The Project

This application retrieves data from GitLab's API about Merge Requests and Discussions and presents it in a dashboard for a more comprehensive code review process. By looking at these charts, developers can grasp their team's code review instead of having to look through Gitlab long discussions. 


### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites:

1. Docker: The application is Dockerized for easy setup and distribution. Make sure you have Docker installed on your system. Download it from here: (https://www.docker.com/products/docker-desktop)

2. Docker Compose: Docker Compose is used to manage the application services. It's usually installed with Docker Desktop. If not, install it from here: (https://docs.docker.com/compose/install/)

3. Git: Git clone to clone the project

```
git clone https://github.com/vinhwin1810/code-review-dashboard.git
```

### Configuration

In the docker-compose.yml file, update to your actual credentials
ENV GITLAB_URL='<your_gitlab_url>'
ENV GITLAB_TOKEN='<your_token>'

## In controller folder -> controller.py -> under function fetch_merge_requests():

```python
# Fetch merge requests from the project
    project_id = "<project_id>" #REPLACE <project_id> by your actual project id
```

### Database Setup:

1. Install MySQL Server on your local machine, if not already installed.
2. Create a new MySQL database for this application. You can name it whatever you prefer.
3. Record the username, password, and database name for the next step. For simplicity, the database name must be MR_data

### Environment Configuration:

1. In the docker-compose.yml file, update the MYSQL_ROOT_PASSWORD fields under the db service to match your local MySQL root password you created in step 1.
2. Also, update the DATABASE_URL field under the api service to match your database credentials. The format is: "mysql+pymysql://<user>:<password>@db/MR_data". Replace <user>, <password> with your actual database username, password.

### Build and Run:

Build and start the services using Docker Compose with the command:

```
docker-compose build
docker-compose up
```
