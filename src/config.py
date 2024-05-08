import yaml


class Config:
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 5000
    DEBUG_MODE: bool = True
    API_SECRET_KEY: str = "your_strong_secret_key"
    JWT_SECRET_KEY: str = "your_jwt_secret_key"

    @staticmethod
    def parse():
        try:
            with open("tunepy_config.yml", "r") as config_file:
                config_doc = yaml.safe_load(config_file)
                Config.API_HOST = config_doc["api"]["host"]
                Config.API_PORT = config_doc["api"]["port"]
                Config.DEBUG_MODE = config_doc["api"]["debug"]
                Config.API_SECRET_KEY = config_doc["api"]["secret_key"]
                Config.JWT_SECRET_KEY = config_doc["api"]["jwt_secret_key"]
        except FileNotFoundError:
            print("Configuration file 'tunepy_config.yml' not found!")
        except TypeError:
            print("Configuration file 'tunepy_config.yml' is invalid!")
