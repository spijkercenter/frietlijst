#!/bin/bash
zip deployable.zip \
  templates/*.html \
  models/*.py \
  main.py \
  token.json \
  requirements.txt