import yaml

class OZTEC():
    '''
    This class describe the agent instance what works with oZteServer
    '''
    config = None
    def __init__(self,id=None,URL=None):
        if id is not None:
            self._load_config(id=id)
        elif URL is not None:
            #initiate registration
            pass
        else:
            return None

        pass
    def _init_cripto(self):
        pass
    def _load_config(self,path='..\\config.yml', id=None):
        with open(path) as f:
            try :
                self.config = yaml.safe_load(f)[0]
            except yaml.YAMLError as exc :
                #print(exc)
                pass
            print(self.config)
            if id is not None:
                self.config = self.config.get('agents').get(id)

        pass

if __name__ == "__main__":
    oztec = OZTEC(id='aa')
    print(oztec.config)
