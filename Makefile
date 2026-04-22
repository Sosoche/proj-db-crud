.PHONY: start down restart logs ps clean

start:
	docker compose build
	docker compose up -d

down:
	docker compose down

restart: down start

logs:
	docker compose logs -f web

ps:
	docker compose ps

clean:
	docker compose down -v
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
