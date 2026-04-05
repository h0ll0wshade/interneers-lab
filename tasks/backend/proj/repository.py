from .models import Product, ProductCategory
import json
from bson.objectid import ObjectId

class CategoryRepository:
    def create(self, data):
        category = ProductCategory(**data)
        category.save()
        return str(category.id)

    def get_all(self):
        return json.loads(ProductCategory.objects.all().to_json())
    
    def delete(self, category_id):
        category = ProductCategory.objects(id=category_id).first()
        if category:
            category.delete()
            return True
        return False

class ProductRepository:
    def get_by_category(self, category_id):
        # Fetch all products where the reference matches the category_id
        products = Product.objects(category=category_id)
        return json.loads(products.to_json())

    def update_category(self, product_id, category_id): 
        product = Product.objects(id=product_id).first()
        if product:
            # If category_id exists, convert it to an ObjectId. Otherwise, set to None.
            if category_id:
                product.category = ObjectId(category_id)
            else:
                product.category = None
                
            product.save()
            return True
        return False
    
    def bulk_insert(self, product_objects):
        # Returning the result of .insert() gives you the objects with IDs attached
        return Product.objects.insert(product_objects)
    
    def get_products(self):
        return json.loads(Product.objects.all().to_json())