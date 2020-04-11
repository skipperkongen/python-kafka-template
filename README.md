# README #

Template for a simple stream processing service in Python

```                                                                       

                                   HTTP clients                               

                                         │                                    
                                         ▼                                    
                                 ┌──────────────┐                             
┌──────────────┐                 │   REST API   │           ┌──────────────┐  
│              ├─┐               ├──────────────┤           │              ├─┐
│              │ │               │              │           │              │ │
│   Upstream   │ │               │              │           │  Downstream  │ │
│              │ │               │   Service    │           │              │ │
│              │ │────Kafka─────▶│              │────Kafka──┤              │ │
│              │ │               │              │           │              │ │
└─┬────────────┘ │               │              │           └─┬────────────┘ │
  └──────────────┘               └──────────────┘             └──────────────┘
                                         │                                    
                                         ▼                                    
                                     ┌───────┐                                
                                     │   DB  │                                
                                     │       │                                
                                     └───────┘                                                        
```

## How to run locally

Option 1:
```
# Start service
make compose_up
# Stop service
make compose_down
```

Option 2:
```
# Start service
docker-compose up --force-recreate --build --remove-orphans
# Stop service
docker-compose down
docker volume rm python-kafka-template_db-data
```
