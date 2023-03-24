from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from ...models import Category, SubCategory


fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake products'

    def handle(self, *args, **options):
        # Create 10 fake categories
        for i in range(10):
            category = Category.objects.create(
                name=fake.word(),
                description=fake.sentence(),
            )
            # Create 5 fake subcategories for each category
            for j in range(5):
                SubCategory.objects.create(
                    name=fake.word(),
                    description=fake.sentence(),
                    category=category,
                )




