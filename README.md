# HRResumeBank



### Запуск pre-commit
uv run pre-commit run --all-files

# Остановить и удалить контейнер
docker stop ваш_контейнер_postgres
docker rm ваш_контейнер_postgres

# Удалить volume с данными (если нужно полностью очистить)
docker volume rm ваш_volume_postgres