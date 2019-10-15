#!/bin/bash

# Complete script for API-driven runs.
# Documentation can be found at:
# https://www.terraform.io/docs/cloud/run/api.html

# 1. Define Variables

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] ; then
  echo "Usage: $0 <organization>/<workspace> key value"
  exit 0
fi

ORG_NAME="$(cut -d'/' -f1 <<<"$1")"
WORKSPACE_NAME="$(cut -d'/' -f2 <<<"$1")"
KEY=$2
VALUE=$3


echo "OrgName   ${ORG_NAME}"
echo "Workspace ${WORKSPACE_NAME}"

WORKSPACE_ID=($(curl \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  https://app.terraform.io/api/v2/organizations/$ORG_NAME/workspaces/$WORKSPACE_NAME \
  | jq -r '.data.id'))

echo "WORKSPACE_ID ${WORKSPACE_ID}"

# 3. create env variable

JSON_FMT='
{
  "data": {
    "type":"vars",
    "attributes": {
      "key":"%s",
      "value":"%s",
      "category":"terraform",
      "hcl":false,
      "sensitive":false
    },
    "relationships": {
      "workspace": {
        "data": {
          "id":"%s",
          "type":"workspaces"
        }
      }
    }
  }
}
'


printf "$JSON_FMT" "$KEY" "$VALUE" "$WORKSPACE_ID" > create_env.json

cat create_env.json
curl \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request POST \
  --data @create_env.json \
  https://app.terraform.io/api/v2/vars




