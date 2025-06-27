#!/bin/bash

RUNIT=false

# Loop through arguments
for arg in "$@"; do
  if [[ "$arg" == "--runit" ]]; then
    RUNIT=true
    break
  fi
done

# Name of the app
bund="ns-app-prolog"

# option -f force the deletion of any existing app with the same name
retval=`dx build -f $bund --destination /commons/ns-apps`
appret=`echo "$retval" | ssh is233959 jq -r '.id'`

echo "ns-app-prolog is succesfully compiled and uploaded in /commons/ns-apps"

if [ "$RUNIT" = true ]; then
  dx run --priority high $appret -ioutprefix=joli -y --watch
else
  echo "applet-id is: " $appret
fi