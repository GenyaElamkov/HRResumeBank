DC = docker-compose
STORAGES_FILE = docker_compose/storages.yaml
LOGS = docker logs
EXEC = docker exec -it
DB_CONTAINER = example-db
ENV = --env-file .env
APP_FILE = docker_compose/app_dev.yaml
APP_FILE_PROD = docker_compose/app_prod.yaml
APP_CONTAINER = main-app
MANAGE_PY = python manage.py


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

.PHONY: app-prod
app-prod:
	$(DC) -f $(APP_FILE_PROD) -f $(STORAGES_FILE) $(ENV) up -d --build

.PHONY: app-logs
app-logs:
	$(LOGS) $(APP_CONTAINER) -f

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) -f $(STORAGES_FILE) $(ENV) down

.PHONY: app-prod-down
app-prod-down:
	$(DC) -f $(APP_FILE_PROD) -f $(STORAGES_FILE) $(ENV) down

.PHONY: app-img-down
app-img-down:
	$(DC) -f $(APP_FILE) -f $(STORAGES_FILE) down -v

.PHONY: migrate
migrate:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) migrate

.PHONY: migrations
migrations:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) makemigrations

# Схлопывание миграции
.PHONY: squashmigrations
squashmigrations:
	$(EXEC) $(MANAGE_PY) squashmigrations ${APP_CONTAINER}


.PHONY: superuser
superuser:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) createsuperuser

.PHONY: collectstatic
collectstatic:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) collectstatic --clear

# Faker
.PHONY: seed
seed:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) seed

.PHONY: seed-prod
seed-prod:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) seed_prod


# Очистить историю audilog
.PHONY: clear_history
clear_history:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) axec_reset

# Fixture
.PHONY: fixture
fixture:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) load_help_data

.PHONY: check
check:
	$(EXEC) $(APP_CONTAINER) $(MANAGE_PY) check
