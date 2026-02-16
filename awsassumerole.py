import boto3
import base64

def assume_role_with_saml(saml_response_b64: str, role_arn: str, principal_arn: str):

    sts = boto3.client("sts")

    response = sts.assume_role_with_saml(
        RoleArn=role_arn,
        PrincipalArn=principal_arn,
        SAMLAssertion=saml_response_b64
    )

    return response["Credentials"]