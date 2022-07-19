#!/bin/bash
while !</dev/tcp/db/5432; do sleep 1; done;

uvicorn main:app --reload --host 0.0.0.0
