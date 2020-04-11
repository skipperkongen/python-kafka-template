# README #

Template for a simple stream processing service in Python. You can run everything in the
diagram locally with docker-compose (see "Running the service locally").

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

## Running the service locally

Start the service:
```
make compose_up
```

Call Web API:

```
curl http://localhost
```

Stop the service:
```
make compose_down
```
