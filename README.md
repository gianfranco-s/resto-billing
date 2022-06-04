This repo is forked from https://github.com/guillermo-k/App_restaurant

## If using PostgreSQL
Create  database (after installing, of course):
```
sudo service postgresql start
sudo -u postgres psql -c "create role resto_billing with password 'resto_billing'"
sudo -u postgres psql -c "ALTER ROLE resto_billing WITH LOGIN;"
sudo -u postgres psql -c 'CREATE DATABASE my_resto WITH OWNER resto_billing'
```

Run the project:
``` 
export FLASK_DEBUG=1; export FLASK_APP=resto_billing; export FLASK_ENV=development; flask run
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