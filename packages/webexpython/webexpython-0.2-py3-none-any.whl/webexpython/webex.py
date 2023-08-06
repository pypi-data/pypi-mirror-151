import requests, json

API_BASE_URL = "https://webexapis.com/v1/"

#Get a bearer token from the refresh token (the bearer tokens expire frequently, while the refresh tokens do not)
def refreshToken(client_id,client_secret,refresh_token):
    data = {'grant_type': 'refresh_token', 'client_id' : client_id, 'client_secret' : client_secret, 'refresh_token': refresh_token}
    bodyPayloadText = json.dumps(data) 
    refresh_URL = "https://webexapis.com/v1/access_token"
    API_HEADERS = { 'Content-Type' : 'application/json'}
    API_RESPONSE = requests.post(refresh_URL, headers=API_HEADERS, data = bodyPayloadText) 
    access_token = API_RESPONSE.json()["access_token"]
    return access_token

#List admin audit events in your organization
def adminAuditEvents(bearer_token, orgId, fromDateTime, toDateTime, actorId): 
#    API_URL = API_BASE_URL + "adminAudit/events" + "?orgId=" + orgId + "&from=" + fromDateTime + "&to=" + toDateTime + "&actorId=" + actorId + "&max=" + max + "&offset=" + offset
    API_URL = API_BASE_URL + "adminAudit/events" + "?orgId=" + orgId + "&from=" + fromDateTime + "&to=" + toDateTime 

    print('API URL: ' + API_URL)
    API_HEADER = {'Authorization': 'Bearer ' + bearer_token, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    API_RESPONSE = requests.get(API_URL, headers=API_HEADER, verify=True) 
    items = API_RESPONSE.text
    return items


#This function will get the Webex UserID value from a provided email address
def getUserId(bearer_token, emailaddress): 
    API_URL = API_BASE_URL + "people/?email="+ emailaddress
    API_HEADER = {'Authorization': 'Bearer ' + bearer_token, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    API_RESPONSE = requests.get(API_URL, headers=API_HEADER, verify=True) 
    
    #print("API Response is: " + str(API_RESPONSE.json()))
    if API_RESPONSE.json()["items"]:
        #print("We have a user")
        userId = API_RESPONSE.json()["items"][0]["id"]
        return userId
    else:
        return("No User Found")
                
            #
#Shows details for a person, by ID.
def getUserDetails(bearer_token, userId): 
    API_URL = API_BASE_URL + "people/"+ userId
    API_HEADER = {'Authorization': 'Bearer ' + bearer_token, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    API_RESPONSE = requests.get(API_URL, headers=API_HEADER, verify=True) 
    return API_RESPONSE.text
    

#This function will get the licenses associated with an organization from a provided org id
def getLicenses(bearer_token, ordId):
    API_URL = API_BASE_URL + "licenses" + "?" + ordId
    API_HEADER = {'Authorization': 'Bearer ' + bearer_token, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
      
    data = {
        'grant_type': 'bearer_token'
        }
    
    bodyPayloadText = json.dumps(data) # This formats the contents of 'data' into proper JSON for sending in the request body
    API_RESPONSE = requests.get(API_URL, headers=API_HEADER, data = bodyPayloadText ) 
    licenses = API_RESPONSE.text
    return licenses

def getLocationIds(bearer_token, orgId):
    API_URL = API_BASE_URL + "locations" + "?" + "callingData=true"
    API_HEADER = {'Authorization': 'Bearer ' + bearer_token, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    API_RESPONSE = requests.get(API_URL, headers=API_HEADER, verify=True) 
    locationids = API_RESPONSE.text
    return locationids

def setVoicemailZeroOut(bearer_token, enableOrDisable, userId, destination):
    
    if enableOrDisable == "enable":
        print("Enabling Zero Out")
        print()
        data = { 
                "transferToNumber": {
                    "enabled": True,
                    "destination": destination
                }
            }        
    
    if enableOrDisable == "disable":
        print("Disabling Zero Out")
        print()
        data = { 
                "transferToNumber": {
                    "enabled": False
                }
            }        
    
    bodyPayloadText = json.dumps(data) # This formats the contents of 'data' into proper JSON for sending in the request body

    API_URL = API_BASE_URL + "people/" + userId + "/features/voicemail"
    API_HEADER = {'Authorization': 'Bearer ' + bearer_token, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    
    API_RESPONSE = requests.put(API_URL, headers=API_HEADER, data = bodyPayloadText )     
    if API_RESPONSE.text == "":
        return ("Success Setting Voicemail Parameters")
    else:  
        return("Error Setting Voicemail Parameters: " + API_RESPONSE.text)

def setVoicemailEmailNotify(bearer_token, enableOrDisable, userId, destination):
    
    if enableOrDisable == "enable":
        print("Enabling Email Notification")
        data = { 
                "emailCopyOfMessage": {
                "enabled": True,
                "emailId": destination
                }
            }        

    if enableOrDisable == "disable":
        print("Disabling Email Notification")
        data = { 
                "emailCopyOfMessage": {
                "enabled": False
                }
            }          
    
    bodyPayloadText = json.dumps(data) # This formats the contents of 'data' into proper JSON for sending in the request body

    #print(bodyPayloadText)
    API_URL = API_BASE_URL + "people/" + userId + "/features/voicemail"
    API_HEADER = {'Authorization': 'Bearer ' + bearer_token, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    print(API_URL)
    API_RESPONSE = requests.put(API_URL, headers=API_HEADER, data = bodyPayloadText )     
    if API_RESPONSE.text == "":
        return ("Success Setting Voicemail Parameters")
    else:  
        return("Error Setting Voicemail Parameters: " + API_RESPONSE.text)



    
def createUser(bearer_token, email, extension, DID, firstName, lastName, location, license, orgId):
    data = { 
        "emails": email,
        #"phoneNumbers": 
        #{
         #"type" : "work",
         #"value" : DID
        #},
        "extension": extension,
        "firstName": firstName,
        "lastName": lastName,
        "orgId": orgId,
        "location": location,
        "licenses": license
        
    }
   
    API_URL = API_BASE_URL + "people/" + "?" + "callingData=true"
    API_HEADER = {'Authorization': 'Bearer ' + bearer_token, 'Content-Type' : 'application/json', 'Accept' : '*/*'}

    bodyPayloadText = json.dumps(data) 
    print(bodyPayloadText)
    API_RESPONSE = requests.post(API_URL, headers=API_HEADER, data = bodyPayloadText) 
    results = API_RESPONSE.text
    return results


    bodyPayloadText = json.dumps(data) 

def deleteUser(bearer_token, userId):
    API_URL = API_BASE_URL + "people/"+ userId
    API_HEADER = {'Authorization': 'Bearer ' + bearer_token, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    API_RESPONSE = requests.delete(API_URL, headers=API_HEADER, verify=True) 
    
    if API_RESPONSE.status_code == 204:
        print("Deleted Successfully") 
        return("User Found")
    else:
        return("No User Found")
   
def createCallQueue(bearer_token, locationId, name, phoneNumber, extension, firstName, lastName, callPolicies, agents):
    data = {
        "locationId" : locationId, 
        "name": name,
        "phoneNumber": phoneNumber,
        "extension": extension,
        "firstName": firstName,
        "lastName": lastName,
        "callPolicies": callPolicies,
        "agents": agents,
        "enabled": "true",
        #"phoneNumbers": 
        #{
         #"type" : "work",
         #"value" : DID
        #},
          
        
    }
    API_URL = API_BASE_URL + "telephony/config/locations/"+ locationId + "/queues"
    API_HEADER = {'Authorization': 'Bearer ' + bearer_token, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    API_RESPONSE = requests.post(API_URL, headers=API_HEADER, data = bodyPayloadText) 