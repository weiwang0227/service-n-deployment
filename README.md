# Overview
A script in Python which can deploy an executable code to an AWS server.

There are three computers that are involved with your deploy script:
* Where we are storing your code (github, bitbucket, etc.). This will be called the repository or repo.
* Where we develop your code, and where we run the deploy script from. This is called a local machine.
* The server that you are deploying your code to. This is the AWS EC2 server.

# The deploy.py which is running on the local machine
* Login, via SSH to the server.
* Clone the repository (and only your repository) to the server, in the home directory.
* Launch the http service remotely on the EC2 machine to be able to accept POST request for getting the JSON data for extraction (by `process_json.py`)
* Schedule, by `crontab`, to rename the log files to have the timestamped name. (by `log_rotate.py`)
