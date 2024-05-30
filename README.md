# How To Setup

1. Create a python virtual environment.
    > python -m venv env
2. Activate the environment. <br>
    > (for linux) source env/bin/activate <br>    
    (for windows) .\env\Scripts/activate
3. For being convenient in development & demonstration purposes, I've used **db.sqlite3** database. Thus use the following commands to make migrations files & apply those to the database.
    > python manage.py makemigrations <br>
    python manage.py migrate
4. I've used JWT authentication for certain routes. So for convenience of usage, I've installed a chrome extension called **MODHeader** to make seamless inteaction to the APIs from the browser. [Extension link](https://chromewebstore.google.com/detail/modheader-modify-http-hea/idgpnmonknjnojddfkpgkljpfnnfcklj)
    - Otherwise, the API testing platform like **Postman** or **Insomnia** can also be used for those APIs.
5. Use "**Bearer**" as the _AUTH_HEADER_TYPES_ along with the tokens.

NB: If there is any inconvenience, feel free to ping. Contact: **+8801896310270**
