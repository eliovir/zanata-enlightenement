#!/bin/sh

PROJECTS=" \
apps/econnman:master \
apps/ecrire:master \
apps/empc:master \
apps/epour:master \
apps/espionage:master \
apps/terminology:master \
core/efl:master \
core/elementary:master \
core/enlightenment:master \
devs/ceolin/epulse:master \
devs/devilhorns/emote:master \
devs/huchi/eon:master \
devs/ngc891/eperiodique:master \
devs/rimmed/eflete:master \
e16/e16:master \
e16/e16-menuedit:master \
enlightenment/modules/alarm:master \
enlightenment/modules/comp-scale:master \
enlightenment/modules/cpu:master \
enlightenment/modules/empris:master \
enlightenment/modules/engage:master \
enlightenment/modules/everything-places:master \
enlightenment/modules/everything-websearch:master \
enlightenment/modules/eweather:master \
enlightenment/modules/forecasts:master \
enlightenment/modules/mail:master \
enlightenment/modules/moon:master \
enlightenment/modules/mpdule:master \
enlightenment/modules/net:master \
enlightenment/modules/news:master \
enlightenment/modules/penguins:master \
enlightenment/modules/photo:master \
enlightenment/modules/places:master \
enlightenment/modules/tclock:master \
enlightenment/modules/wlan:master \
games/elemines:master \
games/etrophy:master \
tools/edi:master \
"
# Those only contains .desktop{,.in} files
PROJECTS=$PROJECTS" \
apps/enjoy:master \
apps/ephoto:master \
apps/eruler:master \
devs/billiob/empeedee:master \
devs/discomfitor/e_physics:master \
devs/discomfitor/maelstrom:master \
devs/kuuko/editje:master \
devs/sachiel/maelstrom:master \
enlightenment/modules/desksanity:master \
enlightenment/modules/diskio:master \
enlightenment/modules/elev8:master \
enlightenment/modules/share:master \
games/e_cho:master \
games/econcentration:master \
libs/libeweather:master \
"

# Variables for scripts.
RE="^([^-]+):(.*)$"
SRC=$(pwd)

