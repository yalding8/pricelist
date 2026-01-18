"""
Gunicorn生产环境配置
"""
import os
import multiprocessing

# 服务器socket
bind = f"0.0.0.0:{os.getenv('PORT', '8001')}"
backlog = 2048

# Worker进程
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5

# 进程命名
proc_name = 'pricelist-web-app'

# 日志
accesslog = '/var/log/pricelist/access.log'
errorlog = '/var/log/pricelist/error.log'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程管理
daemon = False
pidfile = '/tmp/pricelist.pid'
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL（如果需要）
# keyfile = '/path/to/key.pem'
# certfile = '/path/to/cert.pem'

# 优雅重启
graceful_timeout = 30
