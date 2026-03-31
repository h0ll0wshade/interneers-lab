from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from mongoengine import connect, disconnect
import mongomock
from .models import Product, ProductCategory

class ECommerceAPITests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        disconnect() 
        connect('mongoenginetest', mongo_client_class=mongomock.MongoClient) # NEW WAY

    @classmethod
    def tearDownClass(cls):
        disconnect()
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        Product.objects.delete()
        ProductCategory.objects.delete()

        # 1. Manually generate test categories
        self.cat_electronics = ProductCategory(title="Electronics", description="Gadgets and devices").save()
        self.cat_clothing = ProductCategory(title="Clothing", description="Wearables").save()

        # 2. Manually generate test products and assign them to categories
        self.prod_phone = Product(
            name="Smartphone X", 
            brand="TechCorp", 
            price=999.00, 
            quantity=50,
            category=self.cat_electronics
        ).save()

        self.prod_laptop = Product(
            name="Pro Laptop", 
            brand="TechCorp", 
            price=1500.00, 
            quantity=20,
            category=self.cat_electronics
        ).save()

        self.prod_shirt = Product(
            name="Graphic T-Shirt", 
            brand="CottonCo", 
            price=25.00, 
            quantity=100,
            category=self.cat_clothing
        ).save()

        self.prod_unassigned = Product(
            name="Generic Coffee Mug", 
            brand="HomeGoods", 
            price=10.00, 
            quantity=200
            # Notice this one has no category yet
        ).save()


    # --- THE TESTS ---

    def test_get_all_categories(self):
        """Test fetching the categories we manually created."""
        response = self.client.get('/proj/categories/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # We created exactly 2 categories in setUp
        self.assertEqual(len(response.data), 2)

    def test_get_products_in_electronics_category(self):
        """Test fetching products for a specific category."""
        url = f'/proj/categories/{str(self.cat_electronics.id)}/products/'
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_assign_category_to_unassigned_product(self):
        """Test adding a product to a category via PATCH request."""
        url = f'/proj/products/{str(self.prod_unassigned.id)}/category/'
        payload = {'category_id': str(self.cat_clothing.id)}
        
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Pull the mug from the database again to see if it changed
        self.prod_unassigned.reload() 
        self.assertEqual(str(self.prod_unassigned.category.id), str(self.cat_clothing.id))

    def test_remove_product_from_category(self):
        """Test removing a product from a category by sending a null ID."""
        url = f'/proj/products/{str(self.prod_phone.id)}/category/'
        payload = {'category_id': None}
        
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # The phone should no longer have a category
        self.prod_phone.reload()
        self.assertIsNone(self.prod_phone.category)

    def test_delete_category_orphans_products(self):
        """Test deleting a category sets its products' category to null."""
        url = f'/proj/categories/{str(self.cat_electronics.id)}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # The electronics category should be gone
        self.assertEqual(ProductCategory.objects.count(), 1)
        
        # The Phone and Laptop should still exist, but their category should be None
        self.prod_phone.reload()
        self.prod_laptop.reload()
        self.assertIsNone(self.prod_phone.category)
        self.assertIsNone(self.prod_laptop.category)