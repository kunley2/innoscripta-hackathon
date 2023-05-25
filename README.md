# Kunle And Manel Project
- this project for Kunle and Manel group on the innoscripta challenge of building a company information gathering system

## Running The project
- To install the relevant libraries the project, its recommended to create a virtual environment and install and the dependencies using pip install -r requirements.txt
- To start the project run python main.py after putting your env file

## Running using Docker
- To use docker please install docker desktop
- Use the command docker build -t [name of the container image] .
- Run docker run -p 8000:8000 -e [environment variable=value] [container name] or docker run -p 8000:8000 --env-file [path_to_env_file] [container_name]