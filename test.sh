TOKEN=$(curl -s -H 'content-type: application/json' -d '{"username": "test","password": "test"}' http://localhost/login | jq -r .access_token)

curl -H "Authorization: Bearer $TOKEN" http://localhost/api/v1/actions/
