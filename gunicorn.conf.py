import time

time_str = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

accesslog = "gunicorn_log/{}_gunicorn.access.log".format(time_str)
errorlog = "gunicorn_log/{}_gunicorn.log".format(time_str)
loglevel = "info"
capture_output = True

worker_class = "gevent"
workers = 6
threads = 8

bind = ["127.0.0.1:5000"]