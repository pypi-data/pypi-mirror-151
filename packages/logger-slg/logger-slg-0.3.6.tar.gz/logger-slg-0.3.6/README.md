from logger_slg import init_logger


init_logger(name = 'default_logger',
    log_path = '/var/log/slg/default_location.log',
    log_level = 'INFO',
    stream_log_level = 'DEBUG',
    formatter_str = '%(asctime)s | %(levelname)-8s | Line %(lineno)-4s | %(pathname)s | %(message)s',
    max_bytes=10000000,
    backup_count=5
)