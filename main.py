import requests
import csv
import json

# Replace with your API credentials and Discord webhook URL
base_url = 'https://api.wallester.com'
access_token = 'YOUR_ACCESS_TOKEN'
api_key = 'YOUR_API_KEY'
discord_webhook_url = 'YOUR_DISCORD_WEBHOOK_URL'

# Set headers and parameters for API requests
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + access_token}
params = {'api_key': api_key}

# Read card data from CSV file
with open('card_data.csv', 'r') as csvfile:
    card_data_reader = csv.DictReader(csvfile)
    card_data_list = list(card_data_reader)

# Create CSV file to store credit card details
with open('credit_card_details.csv', 'w', newline='') as csvfile:
    fieldnames = ['card_number', 'expiry_date', 'cvv']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Create cards
    for card_data in card_data_list:
        create_card_response = requests.post(base_url + '/cards', headers=headers, params=params, data=json.dumps(card_data))
        created_card = create_card_response.json()
        print(created_card)

        # Send Discord webhook with card data
        webhook_data = {
            'username': 'Card Creator Bot',
            'avatar_url': 'https://i.imgur.com/5dKCAKe.png',
            'embeds': [{
                'title': 'New Card Created',
                'description': f'Cardholder Name: {created_card["cardholder_name"]}\nCard Type: {created_card["card_type"]}\nCurrency: {created_card["currency"]}\nBilling Address: {created_card["billing_address"]}',
                'color': 0x00ff00
            }]
        }
        requests.post(discord_webhook_url, json=webhook_data)

        # Save credit card details in CSV file
        credit_card_details = {
            'card_number': created_card['card_number'],
            'expiry_date': created_card['expiry_date'],
            'cvv': created_card['cvv']
        }
        writer.writerow(credit_card_details)
