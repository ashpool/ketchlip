import ConfigParser

class Config():

    def __init__(self, params = {}):
        for k, v in params.items():
            setattr(self, k, v)

cfg = ConfigParser.ConfigParser()
cfg.read("./ketchlip.cfg")

config = Config()

config.consumer_key = cfg.get("Twitter", "CONSUMER_KEY")
config.consumer_secret = cfg.get("Twitter", "CONSUMER_SECRET")
config.access_token = cfg.get("Twitter", "ACCESS_TOKEN")
config.access_token_secret = cfg.get("Twitter", "ACCESS_TOKEN_SECRET")

config.base_dir = cfg.get("Files", "BASE_DIR")
config.log_dir = cfg.get("Files", "LOG_DIR")
config.www_root = cfg.get("Files", "WWW_ROOT")

config.test_property = cfg.get("Test", "TEST_PROPERTY")

