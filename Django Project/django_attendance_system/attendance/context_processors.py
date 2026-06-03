from django.utils import timezone
from .models import Notice

def important_notices(request):
    today = timezone.localdate()
    notices = Notice.objects.filter(is_important=True, publish_date__lte=today).filter(
        expiry_date__isnull=True
    ) | Notice.objects.filter(is_important=True, publish_date__lte=today, expiry_date__gte=today)
    return {"important_notices_global": notices.order_by("-publish_date", "-created_at")[:5]}
