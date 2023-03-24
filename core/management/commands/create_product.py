from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from ...models import Product, SubCategory, User


fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake products'

    def handle(self, *args, **options):
        sub_categories = SubCategory.objects.all()
        users = User.objects.all()

        def create_image():
            # create a fake image file
            filename = fake.file_name(extension='jpg')
            file_content = SimpleUploadedFile(filename, fake.binary(length=1024), content_type='image/jpeg')
            return file_content

        images = [ create_image() for i in range(1, 20) ]

        for i in range(75):
            product = Product()
            product.name = fake.word()
            product.description = fake.text()
            product.state = fake.state()
            product.image = fake.random_element(elements=images)
            product.sub_category = fake.random_element(elements=sub_categories)
            product.price = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
            product.seller = fake.random_element(elements=users)
            product.ordered = fake.pyint(min_value=0, max_value=1000)
            product.is_approved = fake.pybool()
            product.date = fake.date_time_this_year()
            product.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully generated products. {i}'))
   