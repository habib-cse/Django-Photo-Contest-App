from django import template
register = template.Library() 
from core.models import Gallery



@register.filter
def judges_for_gallery(self):
    invests = Invest.objects.filter(status=False, payment_status=False).order_by('-timestamp')[0:10]
    if invests:
        return invests