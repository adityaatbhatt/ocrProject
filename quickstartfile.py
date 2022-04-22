from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import requests, webbrowser, json
import os
from PIL import Image
from url_creator import urlcreator
import time

'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = "e78f0660f4f942a9a06fb1711c892e35"
endpoint = "https://shouryajoshi.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
'''
END - Authenticate
'''

'''
OCR: Read File using the Read API, extract text - remote
This example will extract text in an image, then print results, line by line.
This API call can also extract handwriting style text (not shown).
'''
# Get an image with text

def ocr(read_image_url):
    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read(read_image_url,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    textmessage = ''
    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                textmessage+=line.text+' '
                print(line.bounding_box)

    print(textmessage.rstrip())
        
    '''
    END - Read File - remote
    '''

    print("End of Computer Vision quickstart.")
    file = open('QNA.txt','r')
    n=1
    print((textmessage.rstrip()).lower())
    while n:
        x=file.readline()
        if( x.rstrip()).lower()==(textmessage.rstrip()).lower():
            print('hi')
            im = Image.open(file.readline()[:-1])
            im.show()
            break
        else:
            if x=='':
                file.close()
                n=0
    else:
        res = requests.get('https://www.google.com/search?q= '+textmessage)
        print(str(res))
        if res.status_code ==200:
            webbrowser.open('https://www.google.com/search?q= '+textmessage)
