#!/bin/sh

PROJECTS=" \
legacy/ecore:ecore-1.7 \
legacy/efreet:efreet-1.7 \
core/elementary:elementary-1.7 \
core/enlightenment:enlightenment-0.17 \
enlightenment/modules/eweather:enlightenment-0.17 \
enlightenment/modules/news:enlightenment-0.17 \
enlightenment/modules/places:enlightenment-0.17 \
"

# Variables for scripts.
RE="^([^-]+):(.*)$"
SRC=$(pwd)

