#!/bin/zsh
set -e
ROOT="${0:A:h:h}"
DATA="$HOME/Library/Application Support/MentalOmegaMacOriginal"
mkdir -p "$DATA"
exec >> "$DATA/启动日志.txt" 2>&1
if [[ ! -d "$DATA/Game" ]]; then /usr/bin/ditto "$ROOT/Resources/Game" "$DATA/Game"; fi
export WINEPREFIX="$DATA/Prefix"
export WINEDEBUG=-all
WINE="$ROOT/Resources/Engine.app/Contents/Resources/wine/bin/wine"
if [[ ! -f "$DATA/initialized" ]]; then
 export WINEDLLOVERRIDES="mscoree,mshtml,winemenubuilder.exe,winebus.sys,wineusb.sys,winebth.sys=d"
 "$WINE" wineboot -i
 mkdir -p "$WINEPREFIX/dosdevices"
 ln -sfn "$DATA/Game" "$WINEPREFIX/dosdevices/n:"
 touch "$DATA/initialized"
fi
export WINEDLLOVERRIDES="ddraw=n,b;winemenubuilder.exe,winebus.sys,wineusb.sys,winebth.sys=d"
cd "$DATA/Game"
exec "$WINE" cmd /c 'cd /d N:\ && Resources\clientogl.exe'
