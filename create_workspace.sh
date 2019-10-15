#!/bin/bash

# Complete script for API-driven runs.
# Documentation can be found at:
# https://www.terraform.io/docs/cloud/run/api.html

# 1. Define Variables

if [ -z "$1" ] ; then
  echo "Usage: $0 <organization>/<workspace>"
  exit 0
fi

ORG_NAME="$(cut -d'/' -f1 <<<"$1")"
WORKSPACE_NAME="$(cut -d'/' -f2 <<<"$1")"

TARGET_LOCATION="ccqdsd"

echo "OrgName   ${ORG_NAME}"
echo "Workspace ${WORKSPACE_NAME}"

# 2. Create the Workspace
JSON_FMT='{ "data": { "attributes": { "name": "%s" }, "type": "workspaces" } }'
printf "$JSON_FMT" "$WORKSPACE_NAME" > create_workspace.json

cat create_workspace.json


curl --header "Authorization: Bearer $TOKEN"         \
  --header "Content-Type: application/vnd.api+json"  \
  --request POST \
  --data @create_workspace.json \
  https://app.terraform.io/api/v2/organizations/$ORG_NAME/workspaces


# 3. Look Up the Workspace ID
curl --header "Authorization: Bearer $TOKEN" --header "Content-Type: application/vnd.api+json" https://app.terraform.io/api/v2/organizations/$ORG_NAME/workspaces/$WORKSPACE_NAME


WORKSPACE_ID=($(curl \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  https://app.terraform.io/api/v2/organizations/$ORG_NAME/workspaces/$WORKSPACE_NAME \
  | jq -r '.data.id'))

echo "WORKSPACE_ID ${WORKSPACE_ID}"

