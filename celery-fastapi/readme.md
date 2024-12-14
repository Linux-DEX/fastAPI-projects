# Instruction to run 

**start fastapi using uvicorn**

```
uvicorn main:app --reload
```

**start celery process**
```
celery -A celery_app.celery_app worker --loglevel=info
```
