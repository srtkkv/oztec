import yaml
import os
class config():
    cfg_path = None
    config = None
    def __init__(self, conf_path=None):
        if conf_path == None:
            self.cfg_path = 'config.yaml'
            self.load_config()
            if  self.config== None:
                self.create()
        pass
    def create(self):
        print('create config')
        default_cfg = {'agents': {'asd':[{'a':'s'},{'b':'b'}]}}
        try:
            with open(self.cfg_path, "w") as cfg:
                yaml.dump(default_cfg, cfg)
        except:
            self.config = None
        pass

    def load_config(self, id=None):
        print(self.cfg_path,os.path.exists(self.cfg_path))
        if os.path.exists(self.cfg_path):
            with open(self.cfg_path, 'r') as f:
                try:
                    self.config = yaml.safe_load(f)
                    if id is not None:
                        self.config = self.config.get('agents').get(id)
                except yaml.YAMLError as exc:
                    self.config = None
                    print('Yaml Error')
        else:
            self.config = None



    def write_config(self, config, id=None ):
        pass