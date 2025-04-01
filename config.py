import os


CONFIG = {
    "env" :  'development',
    "debug" : 'true',
    "host" :  '0.0.0.0',
    "port" :  8000,
    "database_url" : 'sqlite:///./test.db',
    "redis_url" : 'redis://localhost:6379/0',
    "log_level" : 'INFO',
    "log_file" :  'app.log',
    "app_prefix" :  'app_prefix',
    "mongo_user" :  'root',
    "mongo_password" : 'example',
    "mongo_host" : '123.249.37.220',
    "mongo_port" :  27017,
    "default_db" : 'stock',
    "default_collection" :  'hq',
    "app_name" :  'app_name',
    "app_description" :  'app_description',
    "app_version" :  '1.0',
    "app_env_prefix" :  'app',

}
def load_config():
    """
    Load configuration from environment variables.
    """
    app_env_prefix = CONFIG.get("app_env_prefix", "APP").upper()
    for key, value in CONFIG.items():
        name = f"{app_env_prefix}_{key.upper()}"
        if name in os.environ:
            CONFIG[key] = os.environ[name]
        elif name not in os.environ:
            os.environ[name] = str(value)
    return CONFIG


if __name__ == '__main__':
    pass