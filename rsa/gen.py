from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
import ipaddress

def save_pem(data, filename):
    with open(filename, "wb") as f:
        f.write(data)

def generate_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)

def generate_cert(subject, issuer, public_key, issuer_key, is_ca=False, san_list=None):
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(subject)
    builder = builder.issuer_name(issuer)
    builder = builder.public_key(public_key)
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.not_valid_before(datetime.utcnow() - timedelta(days=1))
    builder = builder.not_valid_after(datetime.utcnow() + timedelta(days=3650))
    if is_ca:
        builder = builder.add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        )
    else:
        builder = builder.add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        )
    if san_list:
        builder = builder.add_extension(
            x509.SubjectAlternativeName(san_list),
            critical=False
        )
    return builder.sign(private_key=issuer_key, algorithm=hashes.SHA256())

# 1. Generate CA key and self-signed cert
ca_key = generate_key()
ca_subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u'Test CA')])
ca_cert = generate_cert(ca_subject, ca_subject, ca_key.public_key(), ca_key, is_ca=True)

save_pem(
    ca_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ),
    "ca.key"
)
save_pem(
    ca_cert.public_bytes(serialization.Encoding.PEM),
    "ca.crt"
)

# 2. Generate server key and cert signed by CA, with SAN for localhost and IP
server_key = generate_key()
server_subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u'localhost')])
san_list = [
    x509.DNSName(u'localhost'),
    x509.IPAddress(ipaddress.IPv4Address('127.0.0.1')),
]
server_cert = generate_cert(server_subject, ca_subject, server_key.public_key(), ca_key, is_ca=False, san_list=san_list)

save_pem(
    server_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ),
    "server.key"
)
save_pem(
    server_cert.public_bytes(serialization.Encoding.PEM),
    "server.crt"
)

# 3. Generate client key and cert signed by CA
client_key = generate_key()
client_subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u'Test Client')])
client_cert = generate_cert(client_subject, ca_subject, client_key.public_key(), ca_key, is_ca=False)

save_pem(
    client_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ),
    "client.key"
)
save_pem(
    client_cert.public_bytes(serialization.Encoding.PEM),
    "client.crt"
)

print("All certificates and keys generated.")
