from django.urls import path
from .views import (
    CategoryAPI, 
    CategoryProductsAPI, 
    ProductCategoryUpdateAPI, 
    BulkProductUploadAPI,
    CategoryDetailAPI,
    ProductAPI,
    ProductUpdateAPI
)

urlpatterns = [
    # Category - CRUD
    path('categories/', CategoryAPI.as_view(), name='categories'),
    path('categories/<str:category_id>/', CategoryDetailAPI.as_view(), name='category-detail'),

    #Fetch products belonging to a category
    path('categories/<str:category_id>/products/', CategoryProductsAPI.as_view(), name='category-products'),
    
    #Add/remove products from categories
    path('products/<str:product_id>/category/', ProductCategoryUpdateAPI.as_view(), name='update-product-category'),
    
    #Bulk CSV upload
    path('products/bulk-upload/', BulkProductUploadAPI.as_view(), name='bulk-product-upload'),

    # get/del all products
    path('products/', ProductAPI.as_view(), name='products-get'),
    path('products/<str:product_id>/', ProductUpdateAPI.as_view(), name='products-update'),

    # ordering of del products matters relative to bulk upload

]