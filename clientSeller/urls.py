from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # path('productCategories/', product_category_list),
    # path('products/', product_list),
    # path('orders/', order_list),
    # path('productCategories/<str:name>', product_category_detail),
    # path('products/<str:name>', product_detail),
    # path('orders/<int:pk>', order_detail),
    path('productCategories/', AllModelsAPIView.as_view(currentModel=ProductCategory,
                                                        currentSerializer=ProductCategorySerializer),
         name='productCategories'),

    path('products/', AllModelsAPIView.as_view(currentModel=Product,
                                               currentSerializer=ProductSerializer),
         name='products'),

    path('orders/', AllModelsAPIView.as_view(currentModel=Order,
                                             currentSerializer=OrderSerializer),
         name='orders'),

    path('productCategories/<str:name>', AllModelsDetailsAPIView.as_view(currentModel=ProductCategory,
                                                                         currentSerializer=ProductCategorySerializer),
         name='productDetails'),

    path('products/<str:name>', AllModelsDetailsAPIView.as_view(currentModel=Product,
                                                                currentSerializer=ProductSerializer),
         name='orderDetails'),

    path('orders/<int:pk>', AllModelsDetailsAPIView.as_view(currentModel=Order,
                                                            currentSerializer=OrderSerializer),
         name='productCategoryDetails'),
]
