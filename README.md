# README #

Template for a simple stream processing service in Python. You can run everything in the
diagram locally with docker-compose (see "Running the service locally").

```                                                                       

                                       Service                                  

                            ┌────────────────────────────┐                      
┌──────────────┐            │  ┌──────────────┐          │                      
│              │            │  │              │          │                      
│ HTTP clients │──────JWT───┼─▶│   REST API   │          │                      
│              │            │  │              │          │                      
└──────────────┘            │  ├──────────────┤          │                      
                            │  │              │   ┌────┐ │                      
                            │  │     Core     │───│ DB │ │                      
                            │  │              │   └────┘ │                      
┌──────────────┐            │  ├──────────────┤          │    ┌──────────────┐  
│              ├─┐          │  │              │          │    │              ├─┐
│    Kafka     │ ├──────────┼─▶│  Kafka API   │──────────┼───▶│    Kafka     │ │
│              │ │          │  │              │          │    │              │ │
└─┬────────────┘ │          │  └──────────────┘          │    └─┬────────────┘ │
  └──────────────┘          └────────────────────────────┘      └──────────────┘                                    
```

## Running the service locally

Start the service:
```
make compose_up
```

Call Web API:

```
# Get token
TOKEN=$(curl -s -H 'content-type: application/json' -d '{"username": "test","password": "test"}' http://localhost/login | jq -r .access_token)

# Create actions
curl -H "Content-type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"subject": "foo", "action": "Jump through hoops"}' http://localhost/api/v1/actions/
curl -H "Content-type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"subject": "bar", "action": "Walk a tightrope"}' http://localhost/api/v1/actions/

# Retrieve actions
curl -H "Authorization: Bearer $TOKEN" http://localhost/api/v1/actions/
```

Stop the service:
```
make compose_down
```
