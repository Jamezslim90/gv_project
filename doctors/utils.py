import datetime;
import json;
import requests;
import jwt;
import base64;


def createZoomMeeting(topic, start_time, duration, passcode, timezone):
    # time_now = datetime.datetime.now()
    # expiration_time = time_now + datetime.timedelta(minutes=10)
    # rounded_time = round(expiration_time.timestamp())
    
    # Get Headers from the JWT
    # headers = {'alg': 'HS256', 'typ': 'JWT'}
    # payload= {
    #     'iss': 'ABbHTbynSCmqzr3bmZCBKQ',
    #     'exp': rounded_time
    # }  
    # encoded_jwt= jwt.encode(payload, 'UzPvt0Ow0TWvmx6YK3I3QWmZtcDZ1QhtJUZi', algorithm='HS256', headers=headers)
    
    # Convert CLient ID & SECRET KEY TO base64Encoding
    data = "6vzyhZGVR22eILo66cSPzw:OHw8alGV3YLdA2Jq32N1VF7JaS2P0usb" # ID & CLIENT SECRET Key
    data_bytes = data.encode('ascii')

    base64_bytes = base64.b64encode(data_bytes)
    base64_string = base64_bytes.decode('ascii')

    header1 = {"authorization":"Basic " +  base64_string,"Host":"zoom.us", "content-type": "application/x-www-form-urlencoded"}

    # Make first request for access_token
    response = requests.post('https://zoom.us/oauth/token?grant_type=account_credentials&account_id=x05BQTNMTJ-viTB4BaJtFA', headers=header1)

    # Get the response and retrieve the token
    bearer = json.loads(response.text)
    token = bearer['access_token']  # Access token


    # Now make an API call using the access token
    
    url= "https://api.zoom.us/v2/users/" + "getvetplatform@gmail.com" + "/meetings"
    # date= datetime.datetime(2023,4,10,16,30).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    obj= {"topic": topic, "start_time":start_time, "duration": duration, 'password': passcode, 'timezone': timezone, 'agenda': topic }

    # header2 = {"authorization": "Bearer {} ".format(encoded_jwt), "content-type": "application/json"}

    header2 = {"authorization": "Bearer " + token , "content-type": "application/json", "host": "api.zoom.us"}
    create_meeting= requests.post(url, data=json.dumps(obj), headers=header2)

    return create_meeting.json()


