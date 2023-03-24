from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from faker import Faker
from ...models import Product, SubCategory, User


fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake products'

    def handle(self, *args, **options):
        for i in range(5):
            name = fake.name()
            email = fake.email()
            password = 'emmanueZ@9'
            whatsapp_number = fake.phone_number()
            state = fake.state()
            address = fake.address()
            description = fake.text(max_nb_chars=1000)
            is_seller = random.choice([True, False])
            ordered = random.randint(0, 10)
            user = User.objects.create(
                name=name,
                email=email,
                password=password,
                whatsapp_number=whatsapp_number,
                state=state,
                address=address,
                description=description,
                is_seller=is_seller,
                ordered=ordered,
            )