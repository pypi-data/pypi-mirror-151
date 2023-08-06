# DRF Hybdrid Router

Install the package

```python
pip install tms_django_router
```

The router can be instanciate this way:

```python
from tms_django_router.routers import HybridRouter

router = HybridRouter()
```

Then it can use the same `register` method than the original DRF `DefaultRouter`
```python
from tms_django_router.routers import HybridRouter
from mypackage import views

router = routers.HybridRouter()

router.register(r"endpoint", views.MyViewSet)
```

And provides a way to add api view to DRF browsable api without using viewsets:
```
from django.urls import path

router.add_api_view(
    "another",
    path(
        "version/",
        views.MyView.as_view(),
        name="another",
    ),
)
```

Then the urls can be included the same way than `DefaultRouter`:
```python
from django.urls import include

urls = [
    path("api/", include(router.urls))
]
