start-local:
	docker-compose up -d

stop-local:
	docker-compose stop

restart-local:
	docker-compose restart

build:
	docker-compose up -d --build

test:
	docker-compose run --rm backend coverage run -m pytest -vv
	docker-compose run --rm backend coverage report
