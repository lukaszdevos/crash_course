start-local:
	docker-compose up -d

stop-local:
	docker-compose stop

restart-local:
	docker-compose restart

build:
	docker-compose up -d --build