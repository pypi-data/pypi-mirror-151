# py-fastapi-logging

## ENV-переменные для управления логами
#### Уровень логов. debug - для площадок отладки, info - для PROM
LOG_LEVEL=info
#### Формат логов: SIMPLE (обычный) или JSON
LOG_FORMAT=SIMPLE
#### Папка, в которой будут лежать логи
LOG_DIR=/var/log/<APP NAME>
#### Название файла лога
LOG_FILENAME=production.log
#### Фильтруемые ключи в payload и request_params
LOG_EXCLUDE_FIELDS=field1,field2,field3

## Интеграция в FastAPI приложение
```python
from fastapi import FastAPI
from py_fastapi_logging.middlewares.logging import LoggingMiddleware
app = FastAPI()
app.add_middleware(LoggingMiddleware, app_name='my_app_name')
```

