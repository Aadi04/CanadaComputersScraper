import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime
import time
from os import environ

website = requests.get('https://www.canadacomputers.com/product_info.php?cPath=710_1925_1920_1923&item_id=187885')

src = website.content
soup = BeautifulSoup(src, "html.parser")

def main():
  get_content_from_canada_computers()


def get_content_from_canada_computers():
   result = soup.find_all('i', attrs = {'class' : 'fas fa-ban red text-danger'})
   counter = 0 
   attempts = 0
   for text in result:
       counter = counter +1
    
   while (True):
        if counter == 2: 
            # Not in Stock
            print('Time = ' + str(datetime.now()) + "-Attempt = " + str(attempts))
            attempts += 1
            time.sleep(5)
        
        elif counter > 2:
            #Incase something weird happens 
            publish('Something weird has happend in the Canada Computers Script; check the website out just incase something is broken or it is in stock')
            break
        else:
            #Instock!! 
            publish('Lets gooo its in stock in Canada Computers!!! Goooooo!')
            break


def publish(message):
    arn = 'arn:aws:sns:ca-central-1:616203313326:InStockTopic'
    sns_client = boto3.client (
        'sns',
        aws_access_key_id = environ['ACCESS_KEY'], 
        aws_secret_access_key = environ['SECRET_ACCESS_KEY'],
        region_name = 'ca-central-1'
    )
    response = sns_client.publish(TopicArn = arn, Message = message)
    print(response)


main()