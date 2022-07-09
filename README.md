This repo is loosely forked from https://github.com/guillermo-k/App_restaurant

## Run the project
``` 
export FLASK_DEBUG=1; export FLASK_APP=resto_billing; export FLASK_ENV=development; flask run
```

This is the login page you should see
![image](https://user-images.githubusercontent.com/69116761/172068154-09012fb7-008b-4923-ac53-741072d86a4c.png)


## Useful PostgreSQL commands
Create  database:
```
sudo service postgresql start
sudo -u postgres psql -c "create role resto_billing with password 'resto_billing'"
sudo -u postgres psql -c "ALTER ROLE resto_billing WITH LOGIN;"
sudo -u postgres psql -c 'CREATE DATABASE my_resto WITH OWNER resto_billing'
```

Drop database:
```
sudo -u postgres psql -c 'DROP DATABASE my_resto'
```

Interactive PostgreSQL console:
```
sudo -u postgres psql
```

List databases:
```
# \l
```

Connect to the project's database:
```
# \c my_resto
```

List tables:
```
# \dt
```
