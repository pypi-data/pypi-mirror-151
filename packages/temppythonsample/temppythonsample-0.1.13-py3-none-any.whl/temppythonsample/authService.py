import requests

class Authentication():
    def getToken():
        url = "https://makana-app-staging-wa.azurewebsites.net/connect/token"
        payload='client_id=makana_api&grant_type=client_credentials&scope=makanaapp_api&client_secret=TAxhx@9tH(l^MgQ9FWE8}T@NWUT9U)'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response =  requests.post(url, headers=headers, data=payload, verify=False)
        auth_response_json = response.json()
        auth_token = auth_response_json["access_token"]
        auth_token_header_value = "Bearer %s" % auth_token
        return auth_token_header_value