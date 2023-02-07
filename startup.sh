#!/bin/sh
gunicorn -c config/gunicorn/dev.py
