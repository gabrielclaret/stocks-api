run-compose:
	docker-compose -f docker-compose.yaml down --remove-orphans
	docker-compose -f docker-compose.yaml up --build 

local-environment:
	docker-compose -f docker-compose-local.yaml down --remove-orphans
	docker-compose -f docker-compose-local.yaml up --build 

run-tests:
	docker-compose -f docker-compose-tests.yaml down --remove-orphans
	docker-compose -f docker-compose-tests.yaml up --build --exit-code-from app-tests

tests-local-environment:
	docker-compose -f docker-compose-tests.yaml down --remove-orphans
	docker-compose -f docker-compose-tests.yaml up --build mongo-db gcs-mock

run-docker:
	docker build -t stocks-api .
	docker run -it --env-file .env -p 8000:8000 stocks-api
