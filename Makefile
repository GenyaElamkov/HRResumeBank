# local
DC = docker-compose
STORAGES_FILE = docker_compose/storages.yaml
APP_FILE = docker_compose/app_dev.yaml

# prod
# Debian 12 использует команду: docker compose
DC_PROD = docker-compose
APP_FILE_PROD = docker_compose/app_prod.yaml

# all
DB_CONTAINER = example-db
ENV = --env-file .env
LOGS = docker logs
EXEC = docker exec -it
APP_CONTAINER = main-app
MANAGE_PY = python manage.py

# LOCAL
.PHONY: storages
storages:
	$(DC) -f $(STORAGES_FILE) $(ENV) up -d

.PHONY: storages-down
storages-down:
	$(DC) -f $(STORAGES_FILE) $(ENV) down

.PHONY: storages-logs
storages-logs:
	$(LOGS) $(DB_CONTAINER) -f

.PHONY: postgres
postgres:
	$(EXEC) $(DB_CONTAINER) psql

.PHONY: app
app:
	$(DC) -f $(APP_FILE) -f $(STORAGES_FILE) $(ENV) up -d --build

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) -f $(STORAGES_FILE) $(ENV) down

# Faker
.PHONY: seed
seed:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) seed

.PHONY: app-img-down
app-img-down:
	$(DC) -f $(APP_FILE) -f $(STORAGES_FILE) down -v

# PROD
.PHONY: app-prod
app-prod:
	$(DC_PROD) -f $(APP_FILE_PROD) $(ENV) up -d --build

.PHONY: app-prod-down
app-prod-down:
	$(DC_PROD) -f $(APP_FILE_PROD) $(ENV) down

# ALL
.PHONY: app-logs
app-logs:
	$(LOGS) $(APP_CONTAINER) -f

.PHONY: migrate
migrate:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) migrate

.PHONY: migrations
migrations:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) makemigrations

# Схлопывание миграции
.PHONY: squashmigrations
squashmigrations:
	$(EXEC) $(MANAGE_PY) squashmigrations $(APP_CONTAINER)

.PHONY: superuser
superuser:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) createsuperuser

.PHONY: collectstatic
collectstatic:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) collectstatic --clear

# Fixture по excel шаблону
.PHONY: seed-prod
seed-prod:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) seed_prod

# Fixture
.PHONY: fixture
fixture:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) load_help_data

# Очистить историю audilog
.PHONY: clear_history
clear_history:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) axec_reset

.PHONY: check
check:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) check
