#!/bin/bash

source .env/bin/activate && gunicorn server:app &
