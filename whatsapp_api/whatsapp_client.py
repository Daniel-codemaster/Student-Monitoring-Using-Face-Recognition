import json
import requests
from typing import List

class WhatsAppClient:
    def __init__(self, server_options):
        self.server_options = server_options
        self.http_client = None

    @property
    def http_client(self):
        if self._http_client is None:
            self._http_client = requests.Session()
            self._http_client.headers.update({
                "Authorization": f"Bearer {self.server_options['Token']}",
                "Content-Type": "application/json"
            })
        return self._http_client

    @http_client.setter
    def http_client(self, value):
        self._http_client = value

    def send_message(self, new_message):
        url = f"{self.server_options['ServerUrl']}/{self.server_options['ApiVersion']}/{self.server_options['PhoneNumberId']}/messages"
        data = json.dumps(new_message, default=lambda x: x.__dict__)
        response = self.http_client.post(url, data=data)
        response.raise_for_status()
        return response

    def send_message_legacy(self, template, recipient, header=None, media=None, body=None):
        components = []
        '''
        if body:
            parameters = []
            for item in body:
                parameters.append(Parameter(type="text", text=item))
            components.append(Component(type="body", parameters=parameters))
        if media:
            if media["media_type"] == MediaType.Document:
                components.append(Component(type="header", parameters=[Parameter(type="document", document=Document(link=media["link"]))]))
            elif media["media_type"] == MediaType.Image:
                components.append(Component(type="header", parameters=[Parameter(type="image", image=Image(link=media["link"]))]))
            elif media["media_type"] == MediaType.Video:
                components.append(Component(type="header", parameters=[Parameter(type="video", video=Video(link=media["link"]))]))
        if header:
            components.append(Component(type="header", parameters=[Parameter(type="text", text=header)]))
        message_template = MessageTemplate(name=template, language=MessageLanguage(code=self.server_options["Language"]), components=components)
        new_message = NewMessage(messaging_product="whatsapp", to=recipient, type="template", template=message_template)
        response = self.send_message(new_message)
        response_text = response.text
        response_json = json.loads(response_text)
        return response_json
        '''
        
