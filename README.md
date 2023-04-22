# Build Setup

```bash

#It's essential to use the following versions for correct running:


# Python 3.10

# Running the project:
Install the pgAdmin: https://www.pgadmin.org/download/
Set the configuration of the user and password
Create a database calling the challenge
Change the BASE_URL variable on the .env file with your credentials.

After that running

Copy the .env file on the directory root

$ python -m uvicorn main:app --reload

#Notes:
You can check all back-end endpoints at the following link:
http://localhost:8000/docs


```