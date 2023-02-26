from Core import config, crypto
import requests
class OZTEC():
    '''
    This class describe the agent instance what works with oZteServer
    '''
    config = None
    cripto = None
    session = None
    def __init__(self,id=None,cfg=None):
        self.session = requests.session()
        self.config = config.config(conf_path=cfg)
        if id is not None:
            if self.config.load_config(id=id) == None:
                self.config.create()

    def register_agent(self,URL):
        '''

        This metod called then there is not available profile and need to initiate the regitration to the oZTeServer

        :return:

        '''

        #TODO Get oztes server profile and extract Cripto policy to generate the Agents Certificate
        policy = self._oztes_agentProfile(URL)
        print(policy)
        # self.cripto = cripto.Cripto()
        # self.cripto.create_CSR(profile=profile)
        pass
    def _init_cripto(self):

        pass

    def _oztes_agentProfile(self,URL,):
        resp = self.session.get(URL)
        if resp.status_code == 200:
            return resp.text
        else:
            return None


        pass
    def _update_config(self):
        pass


if __name__ == "__main__":
    # oztec = OZTEC(id='aa')
    # print(oztec.config)
    # oztec.register_agent()
    # cr = crypto.Crypto()
    # cr.create_CSR(profile=None)

    pass
