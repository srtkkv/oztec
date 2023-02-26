# https://cryptography.io/en/latest/x509/tutorial/#creating-a-self-signed-certificate
#
"""
This class is working with crypro sub system ozte environment.
 this class is starting with profile confing. (config is describing the server configuration and
 client Cripto key configuration.

#TODO UnitTest Generate certificate request for oztes registration
#TODO UnitTest load certificate (private key and cert) from config file
#TODO Sign the messages to OZES
#TODO verify messages from OZTES
#TODO encript messages
# TODO: Unittest coverage
#       - generate private key with test policy
#       - issue the certificate
#
"""
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography import x509

import json


class Crypto():
    key = None
    cert = None
    config = None
    CA_crt = None
    server_crt = None
    sign_type = None

    def __init__(self, config: dict):
        self.config = config
        keys = self.config['configuration']['agent'].get('keys')
        # load cert, in case if exists

        if keys.get('cert') != None:
            self.cert = x509.load_pem_x509_certificates(bytes(keys.get('cert'), "utf-8"))

        # Load priv Key from confg
        if keys.get('private') != None:
            self.key = serialization.load_pem_private_key(bytes(keys.get('private'), "utf-8"), password=None)
        else:  # in case if no keys in config, generate a new one and store it in config.
            self._create_private()
        # load CA cert
        if self.config['configuration']['CA'].get("cert") != None:
            self.CA_crt = x509.load_pem_x509_certificates(
                bytes(self.config['configuration']['CA'].get("cert"), "utf-8"))
        # load Server cert
        if self.config['configuration']['server'].get("cert") != None:
            self.server_crt = x509.load_pem_x509_certificates(
                bytes(self.config['configuration']['server'].get("cert"), "utf-8"))
        self.sign_type = self.config['configuration']['agent']['key_profile'].get('sign_type')
        self.sign_type = self.sign_type if self.sign_type != None else "sha256"

        pass

    def _create_private(self):
        key_lenght = int(self.config['configuration']['agent']['key_profile'].get('key_lenght')) \
            if self.config['configuration']['agent']['key_profile'].get('key_lenght') != '' else 2048
        self.key = rsa.generate_private_key(public_exponent=65537, key_size=key_lenght)
        self.config['configuration']['agent']['keys'] = {
            'private': self.key.private_bytes(encoding=serialization.Encoding.PEM,
                                              format=serialization.PrivateFormat.TraditionalOpenSSL,
                                              encryption_algorithm=None)}

    def create_CSR(self):
        # generate CSR
        profile = self.config['configuration']['agent'].get('cert_profile')

        # Fill up certificate Fields by using ServerProfile
        oids = []
        for item in profile:
            if profile[item] == '':
                val = input(f'Please provide "{item}" attribute value: ')
                oids.append(x509.NameAttribute(x509.ObjectIdentifier(item), val))
                self.config['configuration']['agent']['cert_profile'][item] = val
            else:
                oids.append(x509.NameAttribute(x509.ObjectIdentifier(item), profile[item]))
        subject = x509.Name(oids)
        csr = x509.CertificateSigningRequestBuilder().subject_name(subject).sign(self.key, hashes.SHA256())

        self.config['configuration']['agent']['keys']['csr'] = \
            csr.public_bytes(serialization.Encoding.PEM).decode("utf-8")
        self._export_config()
        return csr.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    def _issue_cert(self):
        # TODO  1) load CSR from string
        #           2) load Server keys (CA)
        #           3) Sign CSR by server keys
        #           4) Export cert

        with open('../tests/pki/server_key.pem', 'rb') as key_file:
            ca_key_pair = serialization.load_pem_private_key(bytes(key_file.read(), "utf-8"), password=None)
            # ca_key_pair = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())
        # load CA Cert
        with open('../tests/pki/server_cert.crt', 'rb') as cert_file:
            ca_cert = x509.load_pem_x509_certificates(bytes(cert_file.read(), "utf-8"))
            # ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_file.read())
        # load CSR
        with open('../tests/artifacts/agent_req.csr', 'rb') as csr_file:
            csr = x509.load_pem_x509_csr(bytes(csr_file.read(), "utf-8"))

        builder = x509.CertificateBuilder()
        builder = builder.serial_number(x509.random_serial_number())
        # builder = builder.not_valid_before(datetime.datetime.now())
        # builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 30))
        builder = builder.issuer_name(x509.Certificate(ca_cert).subject)
        builder = builder.public_key(csr.public_key())

        # REVIEW Here we need to review CERT fields (and change if needed)
        # cert.set_subject(csr.get_subject())
        # ---------
        cert = builder.sign(
            private_key=ca_key_pair, algorithm=hashes.SHA256(),
        )
        with open("../tests/artifacts/agent.crt", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

    def _apply_cert(self, pem: str) -> bool:
        # This method get pem string with cert from oztes response and implement it to cripto profile if public key is the same
        # as in private key.
        # return: False|True of implementation

        cert = x509.load_pem_x509_certificate(bytes(pem, "utf-8"))
        if cert.public_key() == self.key.public_key():
            self.cert = cert
            self.config['configuration']['agent']['keys']['cert'] = \
                self.cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

        else:
            Exception(f'The private key can use cert.')
            return False

        self._export_config()
        return True

    # TODO refactor to store config changes in the oztec config file
    def _export_config(self):
        print(self.config)
        with open('../tests/artifacts/criptografy_conf.json', 'w') as file:
            json.dump(self.config, file)
        pass


if __name__ == '__main__':
    with open('../tests/artifacts/criptografy_conf.json', 'r') as cripto_cfg:
        profile = json.load(cripto_cfg)
    cript = Crypto(profile)
    print(cript.create_CSR())
    print(cript.config)
    # cript.create_CSR()
    # cript._export_config()
    # cript._issue_cert()
