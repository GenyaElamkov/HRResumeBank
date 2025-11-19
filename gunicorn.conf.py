import multiprocessing


# Бинд порт
bind = "0.0.0.0:8000"

# Количество воркеров (формула для CPU-bound приложений)
workers = max(2, multiprocessing.cpu_count() * 2) + 1

worker_class = "gthread"

# Количество потоков на воркер (для I/O bound приложений)
threads = 2

# Максимальное количество одновременных клиентов
worker_connections = 1000

# Таймауты
timeout = 30
keepalive = 2

# Логирование
accesslog = "-"  # stdout
errorlog = "-"   # stdout
loglevel = "warning"

# Перезапуск воркеров
max_requests = 1000
max_requests_jitter = 100


# Безопасность
limit_request_line = 4096
limit_request_fields = 100

# Preload для ускорения запуска
preload_app = True
