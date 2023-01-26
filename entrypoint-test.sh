#!/bin/bash

until nc -z -v -w30 db 5432
do
  echo 'Waiting for database connection'
  sleep 5
done

alembic upgrade head
uvicorn app.app:app --reload --host 0.0.0.0 --port 82