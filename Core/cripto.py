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
from OpenSSL import crypto, rand
import os
import json


class Cripto():
    key = None
    cert = None
    config = None
    CA_crt = None

    def __init__(self, config: dict):
        self.config = config

        pass

    def create_CSR(self, profile=None):
        # ----------------
        # TODO refactor this part to get information from config
        emailAddress = "kovalenkokv@gmail.com"
        commonName = "test_server"
        countryName = "Ru"
        localityName = "RF"
        stateOrProvinceName = "Tatarstan"
        organizationName = "organizationName"
        organizationUnitName = "organizationUnitName"
        key_lenght = 1024

        # create a key pair
        key_pair = crypto.PKey()
        key_pair.generate_key(crypto.TYPE_RSA, key_lenght)

        # generate CSR
        csr = crypto.X509Req()
        csr.get_subject().C = countryName
        csr.get_subject().ST = stateOrProvinceName
        csr.get_subject().L = localityName
        csr.get_subject().O = organizationName
        csr.get_subject().OU = organizationUnitName
        csr.get_subject().CN = commonName
        csr.get_subject().emailAddress = emailAddress
        csr.set_pubkey(key_pair)
        csr.sign(key_pair, "sha256")
        self.config[0]['configuration']['agent']['keys'] = {
            'csr': crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr).decode("utf-8"),
            'private': crypto.dump_privatekey(crypto.FILETYPE_PEM, key_pair).decode("utf-8")}
        # with open("agent_req.csr","wb") as f:
        #     f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr))
        # with open("agent.key","wb") as f:
        #     f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM,key_pair))
        #
        # follw part is for CA (
        # cert = crypto.X509()
        # cert.get_subject().C = countryName
        # cert.get_subject().ST = stateOrProvinceName
        # cert.get_subject().L = localityName
        # cert.get_subject().O = organizationName
        # cert.get_subject().OU = organizationUnitName
        # cert.get_subject().CN = commonName
        # cert.get_subject().emailAddress = emailAddress
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
        # # Export
        # with open("..\\tmp\\cer.p12", "wb") as f:
        #     f.write(pkcs12.export())
        # pass

    def _export_config(self):
        print(self.config)
        with open('cripto_conf.json', 'w') as file:
            json.dump(self.config, file)
        pass


if __name__ == '__main__':
    with open('../tests/pki/profile.json', 'r') as cripto_cfg:
        profile = json.load(cripto_cfg)
    cript = Cripto(profile)
    cript.create_CSR()
    cript._export_config()