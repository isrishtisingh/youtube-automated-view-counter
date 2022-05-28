import os
import json
import pickle
import pprint
import requests
from time import sleep
import googleapiclient.errors
from google.auth import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from six import viewitems


def getCredentials():
    credentials = None
    #to display data
    pp = pprint.PrettyPrinter(indent=4)

    # token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json',       ## replace this client secret files with your file
                scopes=[
                    'https://www.googleapis.com/auth/youtube.force-ssl'
                ]
            )

            flow.run_local_server(port=8080, prompt='consent',
                                authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)
            
    return credentials  
            
############################################################################


#def main():
def viewCounter():
    youtube = []
    credentials = getCredentials()
    #print(credentials)

    #youtube = build("youtube", "v3", credentials=credentials)
    youtube.append(googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials))


    count = 0
    curr_api = 0

    while(True): 

        # Request (This is what asks Youtube API for the video data)
        try:
            request = youtube[curr_api].videos().list(
                part="snippet,statistics",
                id="_VkAg7Tdb2s"    ## pass the video id
            )
            response = request.execute()

            data = response["items"][0]
            vid_snippet = data["snippet"]

            title = vid_snippet["title"]

            views = str(data["statistics"]["viewCount"])
            
            print("")
            print("Title of Video: " + title)
            print("Number of Views: " + views)

            change = (views not in title)

            if(change):
                title_upd = "This video has " + format(int(views), ",d") + " Views - Tom Scott"
                vid_snippet["title"] = title_upd

                request = youtube[curr_api].videos().update(
                    part="snippet",
                    body={
                        "id": "_VkAg7Tdb2s",
                        "snippet": vid_snippet
                    }
                )
                response = request.execute()
                
                print("Worked!" + str(count))
                sleep(47)
            count += 1
            
            
        except:
            print("Error, trying again")

        count += 1
        sleep(44)
 
#getCredentials()
viewCounter()
       
#run program
# if __name__ == "__main__":
#     main()


