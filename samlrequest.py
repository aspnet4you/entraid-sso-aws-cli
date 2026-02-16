import base64
import uuid
import zlib
import urllib.parse
from datetime import datetime

def generate_saml_request(tenant_id, acs_url, issuer):
    # 1. Build AuthnRequest XML
    request_id = "_" + uuid.uuid4().hex
    issue_instant = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    xml = f"""<samlp:AuthnRequest
    xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
    xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
    ID="{request_id}"
    Version="2.0"
    IssueInstant="{issue_instant}"
    ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
    AssertionConsumerServiceURL="{acs_url}">
        <saml:Issuer>{issuer}</saml:Issuer>
        <samlp:NameIDPolicy
            AllowCreate="true"
            Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified"/>
    </samlp:AuthnRequest>""".strip()

    # 2. Raw DEFLATE (strip zlib header/footer)
    deflated = zlib.compress(xml.encode("utf-8"))[2:-4]

    # 3. Base64 encode
    b64 = base64.b64encode(deflated)

    # 4. URL encode
    return urllib.parse.quote_plus(b64)