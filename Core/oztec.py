import yaml
from Core import cripto

class OZTEC():
    '''
    This class describe the agent instance what works with oZteServer
    '''
    config = None
    cripto = None
    def __init__(self,id=None,URL=None):
        if id is not None:
            self._load_config(id=id)
        elif URL is not None:
            #initiate registration
            self.register_agent(URL)
            pass
        else:
            return None

        pass

    # TODO
    def register_agent(self,URL):
        '''
        This metod called then there is not available profile and need to initiate the regitration to the oZTeServer
        :return:
        '''
        policy = self._get_ozres_userProfile(URL)
        pass
    def _init_cripto(self):

        pass

    def _get_ozres_userProfile(self,URL):
        import requests
        resp = requests.get(URL)
        if resp.status_code == 200:
            #dict(self.config)[URL[-8:]]  # need to create new profile in config
            profile = resp.json()
            self.cripto = cripto.Cripto()
            self.cripto.create_CSR(profile=profile)

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
    def _update_config(self):
        pass

if __name__ == "__main__":
    #oztec = OZTEC(id='aa')
    #print(oztec.config)
    #oztec.register_agent()
    cr = cripto.Cripto()
    cr.create_CSR(profile=None)

    pass
