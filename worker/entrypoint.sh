#!/bin/bash

while !</dev/tcp/db/5432; do sleep 1; done;

dramatiq worker_init --watch .