#!/bin/bash

alembic upgrade head
exec fastapi dev app/main.py --host 0.0.0.0 --port 8000