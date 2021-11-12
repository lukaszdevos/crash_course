# crash course

### Create .env file in main catalog
```
#django setup
SECRET_KEY=django secret key
DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 0.0.0.0
#postgres setup
DB_HOST=db
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```
### Run project
:whale: :whale2: :whale:
```
make start-local
```

#### restart docker
`make restart-local`
#### stop docker
`make stop-local`
#### build docker
`make build`

### Other commands
#### testing
`make test`
