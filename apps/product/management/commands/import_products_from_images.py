from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File
from django.utils.text import slugify
from apps.product.models import Product, ProductCategory, ProductImage
from apps.users.models import User
import os
import random


def get_ai_metadata(image_path, name):
    """Stub for AI metadata extraction.

    Replace this with a call to your AI provider (OpenAI, etc.).
    It should return a dict with keys: name, description, brand_name, price, category_name, stock, is_sale, sale_price
    """
    # Simple heuristic: use filename-derived name and placeholders
    base_name = name or os.path.splitext(os.path.basename(image_path))[0]
    desc = f"Auto-generated description for {base_name}." 
    brand = "Generic"
    price = round(random.uniform(10.0, 199.99), 2)
    category_name = "Uncategorized"
    stock = True
    is_sale = False
    sale_price = 0
    return {
        "name": base_name,
        "description": desc,
        "brand_name": brand,
        "price": price,
        "category_name": category_name,
        "stock": stock,
        "is_sale": is_sale,
        "sale_price": sale_price,
    }


class Command(BaseCommand):
    help = "Import image files from a directory and create Product entries."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            dest="dir",
            help="Directory (absolute or relative to project root) that contains images to import",
            required=True,
        )
        parser.add_argument(
            "--user-id",
            dest="user_id",
            type=int,
            help="ID of the User to assign as product owner (required unless a default user exists)",
        )
        parser.add_argument(
            "--ai",
            action="store_true",
            dest="use_ai",
            help="(Optional) Use AI to generate richer metadata if integrated",
        )

    def handle(self, *args, **options):
        images_dir = options.get("dir")
        user_id = options.get("user_id")
        use_ai = options.get("use_ai")

        if not images_dir:
            raise CommandError("Please provide --dir with the path to images")

        # Resolve relative paths against project root
        if not os.path.isabs(images_dir):
            project_root = settings.BASE_DIR if hasattr(settings, 'BASE_DIR') else os.getcwd()
            images_dir = os.path.join(project_root, images_dir)

        if not os.path.isdir(images_dir):
            raise CommandError(f"Directory not found: {images_dir}")

        # Determine user
        user = None
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise CommandError(f"User with id {user_id} does not exist")
        else:
            user = User.objects.first()
            if not user:
                raise CommandError("No user found in database. Provide --user-id to assign products.")

        supported_ext = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
        count = 0

        for fname in os.listdir(images_dir):
            fpath = os.path.join(images_dir, fname)
            if not os.path.isfile(fpath):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext not in supported_ext:
                continue

            name_from_file = os.path.splitext(fname)[0].replace("_", " ")

            # Obtain metadata (AI stub)
            metadata = get_ai_metadata(fpath, name_from_file) if use_ai else get_ai_metadata(fpath, name_from_file)

            category, _ = ProductCategory.objects.get_or_create(name=metadata.get("category_name") or "Uncategorized")

            product = Product(
                name=metadata.get("name")[:255],
                description=metadata.get("description", ""),
                brand_name=metadata.get("brand_name", ""),
                price=metadata.get("price") or 0,
                stock=metadata.get("stock", True),
                user=user,
                categories=category,
                is_sale=metadata.get("is_sale", False),
                sale_price=metadata.get("sale_price", 0),
            )

            # Attach main image
            with open(fpath, "rb") as fh:
                django_file = File(fh)
                # create product without image first to get an ID, then assign image name
                product.image.save(slugify(metadata.get("name")) + ext, django_file, save=False)
                product.save()

            # Optionally create ProductImage entries if you want gallery images
            ProductImage.objects.create(product=product, image=product.image)

            count += 1
            self.stdout.write(self.style.SUCCESS(f"Created product {product.name} (id={product.id})"))

        self.stdout.write(self.style.SUCCESS(f"Imported {count} images as products."))
