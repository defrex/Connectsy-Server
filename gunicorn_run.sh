#!/bin/sh

gunicorn -c gunicorn_config.py main:runserver