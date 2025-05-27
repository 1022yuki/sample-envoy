## Component
### Envoy
- Listens on 9080
- ExtAuthZ filter hits idp:8081/token_exchange
- Routes by Host header
  - service1.local → micro_service_cluster_1
  - service2.local → micro_service_cluster_2
  - other → 404
### IdP (FastAPI)
- Always returns 200 OK with
  - x-envoy-auth-headers-to-remove: authorization
  - Authorization: Bearer NEW_TOKEN_123
### micro_service_1 – httpbin (port 80)
- placeholder for micro_service
- echoes the rewritten header
### micro_service_2 – stub container (FastAPI, port 8083)
- placeholder for micro_service

## QA in local
### Request to httpbin (HOST: service1.local)
Request
```
curl -v -H "Host: service1.local" \
     -H "Authorization: Bearer OLD_TOKEN" \
     http://localhost:9080/headers
```
Response
```
* Host localhost:9080 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:9080...
* Connected to localhost (::1) port 9080
> GET /headers HTTP/1.1
> Host: service1.local
> User-Agent: curl/8.7.1
> Accept: */*
> Authorization: Bearer OLD_TOKEN
> 
* Request completely sent off
< HTTP/1.1 200 OK
< server: envoy
< date: Tue, 27 May 2025 16:35:57 GMT
< content-type: application/json
< content-length: 201
< access-control-allow-origin: *
< access-control-allow-credentials: true
< x-envoy-upstream-service-time: 41
< 
{
  "headers": {
    "Accept": "*/*", 
    "Authorization": "Bearer NEW_TOKEN_123", 
    "Host": "service1.local", 
    "User-Agent": "curl/8.7.1", 
    "X-Envoy-Expected-Rq-Timeout-Ms": "15000"
  }
}
* Connection #0 to host localhost left intact
```

### Request to mock service (HOST: service2.local)
Request
```
curl -v -H "Host: service2.local" \
     -H "Authorization: Bearer OLD_TOKEN" \
     http://localhost:9080/hoge
```
Response
```
* Host localhost:9080 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:9080...
* Connected to localhost (::1) port 9080
> GET /hoge HTTP/1.1
> Host: service2.local
> User-Agent: curl/8.7.1
> Accept: */*
> Authorization: Bearer OLD_TOKEN
> 
* Request completely sent off
< HTTP/1.1 200 OK
< date: Tue, 27 May 2025 16:36:47 GMT
< server: envoy
< content-length: 37
< content-type: application/json
< x-envoy-upstream-service-time: 39
< 
* Connection #0 to host localhost left intact
{"micro_service":"ok","path":"/hoge"}%   
