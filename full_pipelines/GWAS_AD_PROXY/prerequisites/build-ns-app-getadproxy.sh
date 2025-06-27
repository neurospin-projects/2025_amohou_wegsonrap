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
bund="ns-app-getadproxy"

# option -f force the deletion of any existing app with the same name
retval=`dx build -f $bund --destination /commons/ns-apps`
appret=`echo "$retval" | ssh is233959 jq -r '.id'`

echo $bund "is succesfully compiled and uploaded in /commons/ns-apps"

if [ "$RUNIT" = true ]; then
  dx run --priority high $appret -itabexport_with_icd=/tmp/foret.csv -y --watch
else
  echo "applet-id is: " $appret
fi