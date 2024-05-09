import os

import yaml


class Config:
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 5000
    DEBUG: bool = True
    API_SECRET_KEY: str = "your_strong_secret_key"
    JWT_SECRET_KEY: str = "your_jwt_secret_key"
    DB_FILENAME: str = "tunepy_database.db"
    SONGS_DIRECTORY: str = "./songs/"

    @staticmethod
    def parse():
        try:
            with open("tunepy_config.yml", "r") as config_file:
                config_doc = yaml.safe_load(config_file)
                Config.API_HOST = config_doc["api"]["host"]
                Config.API_PORT = config_doc["api"]["port"]
                Config.DEBUG = config_doc["api"]["debug"]
                Config.API_SECRET_KEY = config_doc["api"]["secret_key"]
                Config.JWT_SECRET_KEY = config_doc["api"]["jwt_secret_key"]
                Config.DB_FILENAME = config_doc["database"]["filename"]
        except FileNotFoundError:
            print("Configuration file 'tunepy_config.yml' not found!")
            Config.write()
        except TypeError:
            print("Configuration file 'tunepy_config.yml' is invalid! Using default configuration.")

        try:
            os.mkdir(Config.SONGS_DIRECTORY)
        except FileExistsError:
            pass
        except IOError as io_error:
            print(io_error)
            exit(1)

    @staticmethod
    def write():
        try:
            with open("tunepy_config.yml", "w") as config_file:
                config_dict = {
                    "api": {
                        "host": Config.API_HOST,
                        "port": Config.API_PORT,
                        "debug": Config.DEBUG,
                        "secret_key": Config.API_SECRET_KEY,
                        "jwt_secret_key": Config.JWT_SECRET_KEY
                    },
                    "database": {
                        "filename": Config.DB_FILENAME
                    }
                }
                print("Writing configuration file 'tunepy_config.yml'.")
                yaml.safe_dump(config_dict, stream=config_file)
        except IOError as io_error:
            print(io_error)
