from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from samlrequest import generate_saml_request
from awsassumerole import assume_role_with_saml

TENANT_ID = "entra-tenant-id-replace-it"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
ACS = "https://signin.aws.amazon.com/saml"
ISSUER = "https://signin.aws.amazon.com/saml#4"
AWS_ROLE_ARN = "arn:aws:iam::<<aws-account-replace-it>>:role/AWS-ANALYST"
AWS_PRINCIPAL_ARN = "arn:aws:iam::<<aws-account-replace-it>>:saml-provider/Azure-AD-SAML-SSO"

saml_request = generate_saml_request(TENANT_ID, ACS, ISSUER)
samlurl = f"{AUTHORITY}/saml2?SAMLRequest={saml_request}"
print(f"SAML Url: {samlurl}")

# Initialize the Chrome driver (make sure the driver is in your PATH or provide the path)

driver = webdriver.Chrome()
driver.get(samlurl)

# The script will pause here for up to 5 minutes (300s) 
# while you manually complete the interactive sign-in
wait = WebDriverWait(driver, 360)
wait.until(EC.presence_of_element_located((By.NAME, "SAMLResponse")))

hidden_samlresponse_element = driver.find_element(By.NAME, "SAMLResponse")
SAMLResponse = hidden_samlresponse_element.get_attribute("value")
#SAMLResponse = wait_for_saml_response(driver)
print(f"SAMLResponse is: {SAMLResponse}")

driver.quit()


creds = assume_role_with_saml(SAMLResponse, AWS_ROLE_ARN, AWS_PRINCIPAL_ARN)

print("AccessKeyId:", creds["AccessKeyId"])
print("SecretAccessKey:", creds["SecretAccessKey"])
print("SessionToken:", creds["SessionToken"])
print("Expiration:", creds["Expiration"])

