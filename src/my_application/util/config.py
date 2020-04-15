import yaml

def readConfig(path):
    config = None
    with open(path, "r") as stream:
        config = yaml.safe_load(stream)
    if config is None:
        sys.exit("No valid configuration file found. The application will terminate.")
    else:
        return config
