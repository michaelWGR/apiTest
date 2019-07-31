import yaml
import os


def get_conf(key):
    conf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml')
    with open(conf_path, 'rb') as cf:
        d = yaml.load(cf, Loader=yaml.FullLoader)
        if d[key]:
            return d[key]
        else:
            return
