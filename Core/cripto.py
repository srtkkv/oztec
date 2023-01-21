#https://cryptography.io/en/latest/x509/tutorial/#creating-a-self-signed-certificate
#
from OpenSSL import crypto

class Cripto():
    key = None
    cert= None
    def __init__(self, config=None):

        pass
    def create_CSR(self, profile=None):

        emailAddress = "kovalenkokv@gmail.com"
        commonName = "test"
        countryName = "Ru"
        localityName = "RF"
        stateOrProvinceName = "Tatarstan"
        organizationName = "organizationName"
        organizationUnitName = "organizationUnitName"
        key_lenght = 1024

        # create a key pair
        key_pair=crypto.PKey()
        key_pair.generate_key(crypto.TYPE_RSA,key_lenght)

        #generate CSR
        csr = crypto.X509Req()
        csr.get_subject().C = countryName
        csr.get_subject().ST = stateOrProvinceName
        csr.get_subject().L = localityName
        csr.get_subject().O = organizationName
        csr.get_subject().OU = organizationUnitName
        csr.get_subject().CN = commonName
        csr.get_subject().emailAddress = emailAddress
        csr.set_pubkey(key_pair)
        csr.sign(key_pair,"sha256")
        with open("..\\tmp\\req.csr","wb") as f:
            f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr))
        with open("..\\tmp\\req.key","wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM,key_pair))
        cert = crypto.X509()
        cert.get_subject().C = countryName
        cert.get_subject().ST = stateOrProvinceName
        cert.get_subject().L = localityName
        cert.get_subject().O = organizationName
        cert.get_subject().OU = organizationUnitName
        cert.get_subject().CN = commonName
        cert.get_subject().emailAddress = emailAddress
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(315360000)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key_pair)
        cert.sign(key_pair , "sha256")
        with open("..\\tmp\\cer.crt" , "wb") as f :
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        pkcs12 = crypto.PKCS12()
        pkcs12.set_certificate(cert)
        pkcs12.set_privatekey(key_pair)

        with open("..\\tmp\\cer.p12" , "wb") as f :
            f.write(pkcs12.export())
        pass

'''sign_certificate_request(csr_cert, ca_cert, private_ca_key):
    cert = x509.CertificateBuilder()
    cert.subject_name(csr_cert.subject)
    cert.issuer_name(ca_cert.subject)
    cert.public_key(csr_cert.public_key())
    cert.serial_number(x509.random_serial_number())
    cert.not_valid_before(datetime.utcnow())
    cert.not_valid_after(datetime.utcnow() + timedelta(days=10))
    cert.sign(private_ca_key, hashes.SHA256())
    return cert.public_bytes(serialization.Encoding.DER)'''