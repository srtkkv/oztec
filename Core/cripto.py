# https://cryptography.io/en/latest/x509/tutorial/#creating-a-self-signed-certificate
#
"""
This class is working with crypro sub system ozte environment.
 this class is starting with profile confing. (config is describing the server configuration and
 client Cripto key configuration.

#TODO Generate certificate request for oztes registration
#TODO load certificate (private key and cert) from config file
#TODO Sign the messages to OZES
#TODO verify messages from OZTES
#TODO encript messages
# TODO: Unittest coverage
#       - generate private key with test policy
#       -
"""
from OpenSSL import crypto
import json


class Cripto():
    key = None
    cert = None
    config = None
    CA_crt = None

    def __init__(self, config: dict):
        self.config = config

        pass

    def create_CSR(self):
        key_lenght = int(self.config['configuration']['agent']['key_profile'].get('key_lenght')) \
            if self.config['configuration']['agent']['key_profile'].get('key_lenght') != '' else 2048
        key_type = {"RSA": crypto.TYPE_RSA,
                    "DSA": crypto.TYPE_DSA,
                    "DH": crypto.TYPE_DH,
                    "EC": crypto.TYPE_EC,
                    "None": crypto.TYPE_RSA,
                    "": crypto.TYPE_RSA}
        # create a key pair
        key_pair = crypto.PKey()
        key_pair.generate_key(
            key_type[str(self.config['configuration']['agent']['key_profile'].get('key_type'))],
            key_lenght)

        # generate CSR
        profile = self.config['configuration']['agent'].get('cert_profile')
        csr = crypto.X509Req()
        # Fill up certificate Fields by using ServerProfile
        for item in profile:
            if profile[item] == '':
                val = input(f'Please provide "{item}" attribute value: ')
                csr.get_subject().__setattr__(name=item, value=val)
            else:
                csr.get_subject().__setattr__(name=item, value=profile[item])

        csr.set_pubkey(key_pair)
        csr.sign(key_pair, "sha256")
        self.config['configuration']['agent']['keys'] = {
            'csr': crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr).decode("utf-8"),
            'private': crypto.dump_privatekey(crypto.FILETYPE_PEM, key_pair).decode("utf-8")}
        with open("../tests/artifacts/agent_req.csr", "wb") as f:
            f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr))

    def _issue_cert(self):
        # TODO  1) load CSR from string
        #           2) load Server keys (CA)
        #           3) Sign CSR by server keys
        #           4) Export cert
        # with open("agent.key","wb") as f:
        #    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM,key_pair))

        # Load private Keys
        with open('../tests/pki/server_key.pem', 'rb') as key_file:
            ca_key_pair = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())
        # load CA Cert
        with open('../tests/pki/server_cert.crt', 'rb') as cert_file:
            ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_file.read())
        # load CSR
        with open('../tests/artifacts/agent_req.csr', 'rb') as csr_file:
            csr = crypto.load_certificate_request(crypto.FILETYPE_PEM, csr_file.read())
        print(csr)
        print(ca_cert)
        print(ca_key_pair)
        # cert = crypto.X509()
        # cert.set_serial_number(1000)
        # cert.gmtime_adj_notBefore(0)
        # cert.gmtime_adj_notAfter(315360000)
        # cert.set_issuer(cert.get_subject())
        # cert.set_pubkey(key_pair)
        # cert.sign(key_pair , "sha256")

        # with open("..\\tmp\\cer.crt", "wb") as f:
        #     f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        #
        # pkcs12 = crypto.PKCS12()
        # pkcs12.set_certificate(cert)
        # pkcs12.set_privatekey(key_pair)
        # #Export
        # with open("..\\tmp\\cer.p12", "wb") as f:
        #     f.write(pkcs12.export())
        # pass


    def _export_config(self):
        print(self.config)
        with open('../tests/artifacts/cripto_conf.json', 'w') as file:
            json.dump(self.config, file)
        pass


if __name__ == '__main__':
    with open('../tests/pki/profile.json', 'r') as cripto_cfg:
        profile = json.load(cripto_cfg)
    cript = Cripto(profile)
    # cript.create_CSR()
    # cript._export_config()
    cript._issue_cert()
