up:
	docker compose -f docker-compose-local.yml up -d

down:
	docker compose -f docker-compose-local.yml down && docker network prune --force

ps:
	docker compose -f docker-compose-local.yml ps

redis-cli:
	docker compose -f docker-compose-local.yml exec cache redis-cli
