# Python Package for Cisco Webex Calling API

## Webex API Documentation

- https://developer.webex.com/docs/

## Installation

```bash
pip install webexpython
```

testing in a lab is highly recommended prior to using in a production environment. (Devnet Sandboxes are great for this!)

## Reserve a DevNet Sandbox (if required)

The	DevNet	Sandbox	is	accessible	 through	Cisco	DevNet	at	http://developer.cisco.com

Select	Collaboration	on	the	right	hand category menu	and	then look	for	the	“Collaboration	12.5”	tile.	
Hit	reserve.

To connect to the lab, you'll need to use VPN.

VPN Credentials will be sent to your DevNet registered email account, or you can view the _OUTPUT_ from the topology page. 

Once connected, you can click on the server, in this case CUCM, and select _ATTRIBUTES_ to find username, password, and hostname / ip address.



## Notes

The webexpython package was written to enable ease of configuration for webex calling parameters. 
Note: There is currently only limited API support for Webex calling. Some features simply cannot be configured via API. Sorry. :(

## Configuration Pre-Requisites

You will require a bearer token from Cisco in order to use the webex api.  

TALK MORE ABOUT HOW TO SET THAT UP HERE

1) Get an access code.   

Use the HTML below to create grant.html and get an access code.  You will be prompted to login, and the acceess code will be available in the URL bar as a parameter (code=your access code). Write down this code.
```html
<!DOCTYPE html>
<html>
  <head>
    <title>Get an authorization code</title>
    <meta charset='utf-8'>
  </head>
  <body>
        <h1>Get a webex teams authorization code</h1>
        </div>
        <div class='spacer-small'></div>
        <div class='center'>
          <a href="https://webexapis.com/v1/authorize?client_id=<insert your client id here>&response_type=code&redirect_uri=http%3A%2F%2Fwebex.com&scope=spark-admin%3Abroadworks_subscribers_write%20meeting%3Aadmin_preferences_write%20spark%3Aall%20meeting%3Aadmin_preferences_read%20analytics%3Aread_all%20meeting%3Aadmin_participants_read%20spark-admin%3Apeople_write%20spark%3Apeople_write%20spark%3Aorganizations_read%20spark-admin%3Aworkspace_metrics_read%20spark-admin%3Aplaces_read%20spark-admin%3Awholesale_billing_reports_read%20spark-compliance%3Ateam_memberships_write%20spark%3Aplaces_read%20identity%3Atokens_read%20spark-compliance%3Amessages_read%20spark-admin%3Adevices_write%20spark-admin%3Aworkspaces_write%20spark%3Acalls_write%20spark-compliance%3Ameetings_write%20meeting%3Aadmin_schedule_write%20Identity%3Aone_time_password%20identity%3Aplaceonetimepassword_create%20spark-admin%3Aorganizations_write%20spark-admin%3Aworkspace_locations_read%20spark%3Adevices_write%20spark-admin%3Abroadworks_billing_reports_write%20spark%3Axapi_commands%20spark-compliance%3Awebhooks_read%20spark-admin%3Acall_qualities_read%20spark-compliance%3Amessages_write%20spark%3Akms%20meeting%3Aparticipants_write%20meeting%3Aadmin_transcripts_read%20spark-admin%3Apeople_read%20spark-compliance%3Amemberships_read%20spark-admin%3Aresource_groups_read%20meeting%3Arecordings_read%20meeting%3Aparticipants_read%20meeting%3Apreferences_write%20spark-admin%3Awholesale_billing_reports_write%20spark-admin%3Aorganizations_read%20meeting%3Aadmin_recordings_read%20spark-compliance%3Awebhooks_write%20meeting%3Atranscripts_read%20identity%3Atokens_write%20spark%3Axapi_statuses%20meeting%3Aschedules_write%20spark-compliance%3Ateam_memberships_read%20spark-admin%3Adevices_read%20meeting%3Acontrols_read%20spark-admin%3Ahybrid_clusters_read%20spark-admin%3Aworkspace_locations_write%20spark-admin%3Atelephony_config_read%20spark-admin%3Atelephony_config_write%20spark-admin%3Abroadworks_billing_reports_read%20meeting%3Aadmin_schedule_read%20spark-admin%3Abroadworks_enterprises_write%20meeting%3Aschedules_read%20spark-compliance%3Amemberships_write%20spark-admin%3Abroadworks_enterprises_read%20spark%3Acalls_read%20spark-admin%3Aroles_read%20meeting%3Arecordings_write%20meeting%3Apreferences_read%20spark-compliance%3Ameetings_read%20spark-admin%3Aworkspaces_read%20spark%3Adevices_read%20spark-admin%3Aresource_group_memberships_read%20spark-compliance%3Aevents_read%20spark-admin%3Aresource_group_memberships_write%20spark-compliance%3Arooms_read%20spark-admin%3Abroadworks_subscribers_read%20meeting%3Acontrols_write%20meeting%3Aadmin_recordings_write%20spark-admin%3Ahybrid_connectors_read%20audit%3Aevents_read%20spark-compliance%3Ateams_read%20spark-admin%3Aplaces_write%20spark-admin%3Alicenses_read%20spark-compliance%3Arooms_write%20spark%3Aplaces_write&state=set_state_here">
            <div class='button' style='width:512px;'>GRANT</div>
          </a>
        </div>
      </div>
    </section>
  </body>
</html>
```

## Create your config.py file
We will store your sensitive information (tokens, secrets, etc) in this file.  Create a file config.py
and define the variables shown, populating them with the values issued by the webex api process.

```python
bearer_token = <insert value here in double quotes>
refresh_token = <insert value here in double quotes> 
client_id = <insert value here in double quotes>
client_secret = <insert value here in double quotes>
```

Fill in your unique values between the quotes

## Package Usage 

```python
from webexpython import webex


```

## Token Management

#### Get a bearer token from the refresh token 
Bearer tokens expire fairly quickly (14 days?) so we will fetch a new bearer token using our refresh token before running calls against the API so we know our token will work

```python
from webexpython import webex
import config
import urllib.parse

refresh_token = config.refresh_token
client_id = config.client_id
client_secret = config.client_secret

access_token = webex.refreshToken(client_id,client_secret,refresh_token)
print(access_token)
```

## Users

#### Get User ID for a single user from email address 
You will need to get the user ID for a user before doing most other configuration tasks. In this example
we first use the refresh token to get an updated bearer/access token. We then use the new access token
to fetch the user ID value.  While other examples in this documentation may reference using a bearer
token directly, we consider it a best practice to execute a refreshToken function prior to making other
calls to ensure you are not attempting to use stale credentials, which will lead to other problems.


```python
from webexpython import webex
import config

refresh_token = config.refresh_token
client_id = config.client_id
client_secret = config.client_secret

access_token = webex.refreshToken(client_id,client_secret,refresh_token)

userId = webex.getUserId(access_token,"user@domain.com")
print("Received UserID: " + userId)
```

#### Configure the 'zero out' feature for voicemail for a single user


```python
import config,webex
bearer_token = config.bearer_token
#First we will fetch the userId from the email address
userId = webex.getUserId(bearer_token,"user@domain.com") 
enableOrDisable = "enable" # or "disable"
destination = "1000"
zeroOut = webex.setVoicemailZeroOut(bearer_token, enableOrDisable, userId, destination)
print(zeroOut)
```

## Organization

#### Get a list of the licenses assigned to the Organization 

```python
import config,webex
bearer_token = config.bearer_token
orgId = "X1zF69zcGFyazovL3VzL09SR0FOSVpBVElPTi8wNzExNTgyZS1kNGMxLTRmNWItYmVmZi03ZjdiMjM4Yjg3MTQ"
licenses = webex.getLicenses(bearer_token,orgId)
print(licenses)
```

#### Get a list of the locations (and location IDs) within the Organization 

```python
import config,webex
bearer_token = config.bearer_token
orgId = "X1zF69zcGFyazovL3VzL09SR0FOSVpBVElPTi8wNzExNTgyZS1kNGMxLTRmNWItYmVmZi03ZjdiMjM4Yjg3MTQ"
locations = webex.getLocations(bearer_token,orgId)
print(locations)


