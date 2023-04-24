import requests

token = "EAAEZBCK1xDcUBAB05qpve4HgT42colSRz0ZBr2Gtu34Xm1ajrH0uGuNjg1LZAUoTB1edrfngvo8vXbYkE01K6cvZBV44rlRhHO2WKVK07rTqQgFLdd0mGAfz3ZCfXdM4Lcx0AcWKqr2xtnuhOJhZAC26nK6hpo6Rzny7MmamIbqHvzv0eEF8U5nJXTv5wCbBeQqvB1RTdIqQZDZD"

def send_message(id, location):

    url = 'https://graph.facebook.com/v15.0/102862835820249/messages'

    payload = {
        "messaging_product":"whatsapp",
        "to":"263785731194",
        "type":"template",
        "template":{
            "name":"image_message",
            "language":{
                "code":"en"
            },
            "components":[
                {
                    "type":"body",
                    "parameters":[
                        {
                            "type":"text",
                            "text":location
                        }
                    ]
                },
                {
                    "type":"header",
                    "parameters":[
                        {
                            "type":"image",
                            "image":{
                                'id': id
                            }
                        }
                    ]
                }
            ]
        }
    }


    # Set headers (if needed)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    # Send the HTTP request
    response = requests.post(url, json=payload, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        print('Request successful')
    else:
        print('Request failed')
        
    # Print the response content
    print(response.content)

def upload(path, location):
    url = 'https://graph.facebook.com/v16.0/102862835820249/media'
   
    payload = {
        'type': 'image/jpeg',
        'messaging_product': 'whatsapp'
    }

    link = 'http://127.0.0.1:8000/media/' + path
    response = requests.get(link)

    # Get the file name from the URL
    file_name = path.split('/')[-1]

    # Add the file to the dictionary
    files = {
        'file': (file_name, response.content, 'image/jpeg')
    }
    
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = requests.post(url, headers=headers, data=payload, files=files)
    print(response.json())
    send_message(response.json()['id'], location)
    return True
