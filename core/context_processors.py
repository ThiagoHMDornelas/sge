from django.conf import settings


def detail_layout(request):
    return {
        "DETAIL_LAYOUT": getattr(settings, "DETAIL_LAYOUT", "minimal")
    }
