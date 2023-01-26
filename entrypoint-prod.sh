#!/bin/bash

alembic upgrade head
uvicorn app.app:app --reload --host 0.0.0.0 --port 80