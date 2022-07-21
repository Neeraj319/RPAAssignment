#!/bin/bash

if [ ! -z "$1" -a "$1" != " " ];
then
    alembic revision --autogenerate -m "$1"
    alembic upgrade head
else
    echo "enter migration name"
fi