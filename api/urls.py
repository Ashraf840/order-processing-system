from django.urls import path

from rest_framework.routers import DefaultRouter
from product.views import *

router = DefaultRouter()
router.register("category", CategoryViewset)
router.register("brand", BrandViewset)
router.register("product-attribute", ProductAttributeViewset)
router.register("attribute-value", AttributeValueViewset)
router.register("product", ProductViewset)
router.register("product-line", ProductLineViewset)

urlpatterns = router.urls