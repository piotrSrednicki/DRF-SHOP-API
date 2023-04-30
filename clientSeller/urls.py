from django.urls import path
from .views import *

urlpatterns = [
    path('productCategories/', AllModelsAPIView.as_view(currentModel=ProductCategory,
                                                        currentSerializer=ProductCategorySerializer),
         name='productCategories'),

    path('products/', AllModelsAPIView.as_view(currentModel=Product,
                                               currentSerializer=ProductSerializer),
         name='products'),

    path('orders/', AllModelsAPIView.as_view(currentModel=Order,
                                             currentSerializer=OrderSerializer),
         name='orders'),

    path('productCategories/<str:pk>', AllModelsDetailsAPIView.as_view(currentModel=ProductCategory,
                                                                       currentSerializer=ProductCategorySerializer),
         name='productDetails'),

    path('products/<str:pk>', AllModelsDetailsAPIView.as_view(currentModel=Product,
                                                              currentSerializer=ProductSerializer),
         name='orderDetails'),

    path('orders/<int:pk>', AllModelsDetailsAPIView.as_view(currentModel=Order,
                                                            currentSerializer=OrderSerializer),
         name='productCategoryDetails'),
    path('statistics/', StatisticsAPIView.as_view(),
         name='productStatistics'),
    path('pictures/<str:path>', PictureView.as_view(),
         name='Picture'),
    path('miniatures/<str:path>', MiniaturePictureView.as_view(),
         name='MiniaturePicture'),
]
