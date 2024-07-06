alembic-revision:
    @read -p "Enter migration message: " message; \
    docker compose exec oauth_api alembic revision --autogenerate -m "$$message"

alembic-upgrade-head:
	docker compose exec oauth_api alembic upgrade head

alembic-upgrade-version:
	@read -p "Enter version: " version; \
	docker compose exec oauth_api alembic upgrade $$version

alembic-downgrade-head:
	docker compose exec oauth_api alembic downgrade head

alembic-downgrade-version:
	@read -p "Enter version: " version; \
	docker compose exec oauth_api alembic downgrade $$version

alembic-history:
	docker compose exec oauth_api alembic history

install-package:
	@read -p "Enter package name: " package; \
	docker compose exec oauth_api poetry add $$package

remove-package:
	@read -p "Enter package name: " package; \
	docker compose exec oauth_api poetry remove $$package

reset-db:
	docker compose exec oauth_api python -m api.reset_db