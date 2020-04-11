compose_up:
	docker-compose up --force-recreate --build --remove-orphans
.PHONY: compose_up

compose_down:
	docker-compose down
	docker volume rm penny-analytics-actions_db-data
.PHONY: compose_down
