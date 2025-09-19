.PHONY: up down ps logs seed psql

up:
	docker compose up -d --build

down:
	docker compose down -v

ps:
	docker compose ps

logs:
	docker compose logs -f --tail=200

seed:
	# runs the seeding script inside the API container
	docker compose exec api python -m seeds.seed

psql:
	# quick psql shell into Postgres
	docker compose exec db psql -U postgres
