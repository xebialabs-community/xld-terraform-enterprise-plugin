#!/bin/bash

# Complete script for API-driven runs.
# Documentation can be found at:
# https://www.terraform.io/docs/cloud/run/api.html
# ORG_TOK: oVmb0yuUnwmuzg.atlasv1.ithYUm5lI2zdHy2B9yIpgDaVMggP1LfcLNKnPDtyM60z6lWnL2BV6uOX8nBBU7vFozo
# USER_TOK: 6SPlj2JkS5LMuw.atlasv1.Lmuf1KzHzQ9FX82lM80Qjf96TrzWG4q3F4XTvxpeLehBBXmr7MjQmbGWrnkSUZy1oCg
# 1. Define Variables

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <path_to_content_directory> <organization>/<workspace>"
  exit 0
fi

CONTENT_DIRECTORY="$1"
ORG_NAME="$(cut -d'/' -f1 <<<"$2")"
WORKSPACE_NAME="$(cut -d'/' -f2 <<<"$2")"

echo "OrgName   ${ORG_NAME}"
echo "Workspace ${WORKSPACE_NAME}"
echo "CONTENT_DIRECTORY ${CONTENT_DIRECTORY}"

# 2. Create the File for Upload

UPLOAD_FILE_NAME="./content-$(date +%s).tar.gz"
tar -zcvf "$UPLOAD_FILE_NAME" -C "$CONTENT_DIRECTORY" .

# 3. Look Up the Workspace ID

curl --header "Authorization: Bearer $TOKEN" --header "Content-Type: application/vnd.api+json" https://app.terraform.io/api/v2/organizations/$ORG_NAME/workspaces/$WORKSPACE_NAME


WORKSPACE_ID=($(curl \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  https://app.terraform.io/api/v2/organizations/$ORG_NAME/workspaces/$WORKSPACE_NAME \
  | jq -r '.data.id'))

echo "WORKSPACE_ID ${WORKSPACE_ID}"
# 4. Create a New Configuration Version

echo '{"data":{"type":"configuration-version"}}' > ./create_config_version.json

#curl --header "Authorization: Bearer $USER_TOKEN"  --header "Content-Type: application/vnd.api+json"  --request POST  --data @create_config_version.json https://app.terraform.io/api/v2/workspaces/$WORKSPACE_ID/configuration-versions


UPLOAD_URL=($(curl \
  --header "Authorization: Bearer $USER_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request POST \
  --data @create_config_version.json \
  https://app.terraform.io/api/v2/workspaces/$WORKSPACE_ID/configuration-versions \
  | jq -r '.data.attributes."upload-url"'))

echo "UPLOAD_URL $UPLOAD_URL"
# 5. Upload the Configuration Content File

curl \
  --header "Content-Type: application/octet-stream" \
  --request PUT \
  --data-binary @"$UPLOAD_FILE_NAME" \
  $UPLOAD_URL

# 6. Delete Temporary Files

#rm "$UPLOAD_FILE_NAME"
#rm ./create_config_version.json
