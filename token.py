import requests
from oic import rndstr
from oic.oic import Client
from oic.oic.message import AuthorizationRequest
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
import os
user = "USER" #Enter your educonnect user creds
password = "PASS"



# Configurer les options du navigateur avec le proxy BrowserMob
chrome_options = webdriver.ChromeOptions()

#chrome_options.add_argument("--headless")
# Instancier le navigateur Selenium avec les options configurées
driver = webdriver.Chrome(options=chrome_options)
cli_id = 'SkoApp.Prod.0d349217-9a4e-41ec-9af9-df9e69e09494'
cli_secret = '7cb4d9a8-2580-4041-9ae8-d5803869183'




discovery_url = "https://sso.eclat-bfc.fr/oidc/.well-known/openid-configuration"
discovery_doc = requests.get(discovery_url).json()
endpoint = discovery_doc['token_endpoint']
print(endpoint)
client = Client(client_authn_method=None, config={
  'client_id': 'SkoApp.Prod.0d349217-9a4e-41ec-9af9-df9e69e09494',
  'client_secret': '7cb4d9a8-2580-4041-9ae8-d5803869183f',
  'redirect_uris': ['skoapp-prod://sign-in-callback'],

  'authorization_endpoint': discovery_doc['authorization_endpoint'],
  'token_endpoint': discovery_doc['token_endpoint'],
  'userinfo_endpoint': discovery_doc['userinfo_endpoint']
})

auth_request = AuthorizationRequest(
  client_id='SkoApp.Prod.0d349217-9a4e-41ec-9af9-df9e69e09494', 
  redirect_uri='skoapp-prod://sign-in-callback',
  response_type='code',
  scope=['openid']
)
auth_url = auth_request.request(client.authorization_endpoint)
final_url = f"https://sso.eclat-bfc.fr/oidc/oidcAuthorize{auth_url}"



driver.get(final_url)
print(f"Connectez-vous ici : {final_url}") 
while driver.current_url != "https://educonnect.education.gouv.fr/idp/profile/SAML2/POST/SSO?execution=e1s1":
   time.sleep(3)

#Se connecter
driver.find_element(By.XPATH, '//*[@id="bouton_eleve"]').click()
time.sleep(3)

driver.find_element(By.ID, "username").send_keys(user)
driver.find_element(By.ID, "password").send_keys(password)
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="bouton_valider"]').click()
req = driver.requests
for request in req:
  print(request.response.headers["location"])
  code_reflect = request.response.headers["location"] # <-- Response headers of selenium 
  code_list = []
  code_list.append(code_reflect)





# Parcourir la liste
for element in code_list:
    # Vérifier si l'élément commence par "skoapp-prod://sign-in-callback" et n'est pas None
    if element is not None and element.startswith("skoapp-prod://sign-in-callback"):
        # Si c'est le cas, imprimer l'élément et quitter la boucle
        print("Élément trouvé :", element)
        break
    

print(element)
index_debut_code = element.find("=")
code = element[index_debut_code + 1:]
print(code)

driver.quit()



      


resp = requests.get(f'{endpoint}?grant_type=authorization_code&client_id=SkoApp.Prod.0d349217-9a4e-41ec-9af9-df9e69e09494&client_secret=7cb4d9a8-2580-4041-9ae8-d5803869183f&redirect_uri=skoapp-prod://sign-in-callback&code='+code)
scrap_info = resp.json()
token = scrap_info['access_token'] 
refresh_token = scrap_info['refresh_token']
openid = scrap_info['scope']
os.system('cls')
print("TOKEN :" + token)
print("REFRESH TOKEN" + refresh_token)
print("OPENID" + openid)
print(resp.status_code)
input("Press Enter to continue...")

