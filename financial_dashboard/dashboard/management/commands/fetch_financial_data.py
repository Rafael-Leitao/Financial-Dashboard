import requests
from django.core.management.base import BaseCommand
from dashboard.models import Transaction
from django.contrib.auth.models import User
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetches transactions from the API and saves them to the database.'

    def handle(self, *args, **kwargs):
        api_url = 'https://sandbox.plaid.com'
        response = requests.get(api_url)
         # Print the raw response for debugging
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        # Attempt to parse JSON
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as e:
            self.stderr.write(f"JSONDecodeError: {e}")
            return

        user = User.objects.get(username='example_user')
        for item in data:
            Transaction.objects.create(
                user=user,
                date=datetime.strptime(item['date'], '%Y-%m-%d'),
                description = item['description'],
                amount = item['item'],
                category = item['category']
            )
        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored data'))


