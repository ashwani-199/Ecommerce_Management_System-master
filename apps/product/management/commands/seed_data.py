# yourapp/management/commands/seed_fake_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
from PIL import Image
from django.core.files.base import ContentFile
import io

from apps.product.models import ProductCategory, Product, ProductReview, ProductImage

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seed database with random products, reviews, and images using Faker"

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Starting Faker seeding...")

        # --- Ensure a user exists ---
        user, _ = User.objects.get_or_create(
            username="fakeruser",
            defaults={"email": "faker@example.com", "password": "password123"}
        )

        # --- Categories ---
        categories = []
        for name in ["Electronics", "Fashion", "Groceries", "Books", "Sports"]:
            cat, _ = ProductCategory.objects.get_or_create(name=name)
            categories.append(cat)

        # --- Products + Images + Reviews ---
        for _ in range(10):  # generate 20 products
            category = fake.random_element(categories)

            product = Product.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(max_nb_chars=200),
                brand_name=fake.company(),
                price=round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
                stock=fake.boolean(),
                image="product_oneimages/placeholder.jpg",  # placeholder path
                user=user,
                categories=category,
                is_sale=fake.boolean(),
                sale_price=round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

            # --- Generate 2 fake images per product ---
            for i in range(2):
                img = Image.new(
                    "RGB",
                    (200, 200),
                    color=(fake.random_int(0, 255), fake.random_int(0, 255), fake.random_int(0, 255))
                )
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG")
                image_file = ContentFile(buffer.getvalue(), f"{product.name.lower()}_{i}.jpg")

                ProductImage.objects.create(product=product, image=image_file)

            # --- Add a random review ---
            ProductReview.objects.create(
                product=product,
                user=user,
                rating=fake.random_int(min=1, max=5),
                description=fake.sentence(nb_words=15),
            )

        self.stdout.write(self.style.SUCCESS("✅ Faker seeding complete!"))
