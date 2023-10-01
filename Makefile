run-compose:
	docker-compose -f docker-compose.yaml down --remove-orphans
	docker-compose -f docker-compose.yaml up --build 

local-environment:
	docker-compose -f docker-compose-local.yaml down --remove-orphans
	docker-compose -f docker-compose-local.yaml up --build 