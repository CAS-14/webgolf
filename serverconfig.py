bind = "0.0.0.0:80"
backlog = 2048
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
spew = False

# log file "-" for stdout/stderr, None for none
# loglevel can be debug, info, warning, error, critical
errorlog = "-"
accesslog = "-"
loglevel = "info"  
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

#certfile = "/etc/letsencrypt/live/example.com/fullchain.pem"
#keyfile = "/etc/letsencrypt/live/example.com/privkey.pem"
#ca_certs = "/root/app/ca_bundle.crt"