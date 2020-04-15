TOKEN=$(curl -s -H 'content-type: application/json' -d '{"username": "test","password": "test"}' http://localhost/login | jq -r .access_token)

curl -H "Content-type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"subject": "foo", "action": "Jump through hoops"}' http://localhost/api/v1/actions/
curl -H "Content-type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"subject": "bar", "action": "Walk a tightrope"}' http://localhost/api/v1/actions/

curl -H "Authorization: Bearer $TOKEN" http://localhost/api/v1/actions/
