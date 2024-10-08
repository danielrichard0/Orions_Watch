from django.contrib import admin
from .models import Order
from cart.models import Cart
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.core.mail import send_mail, EmailMultiAlternatives
from cart.models import Cart

# Register your models here.
class CartInline(admin.TabularInline):
    model = Cart
    readonly_fields = ['product', 'quantity', 'total_price']
    fields = ['product', 'quantity', 'total_price']
    extra = 0
    can_delete = False

    def total_price(self, obj):
        total = obj.product.price * obj.quantity
        humanized = intcomma(total)
        return f"Rp {humanized}"
    
    total_price.short_description = 'Total'

class OrderAdmin(admin.ModelAdmin):
    
    readonly_fields = ['first_name', 'last_name', 'email', 'address', 'user', 'cust_note',  'total_price_comma', 'ongkir_comma', 'total_price_ongkir_comma', ]
    fieldsets = [
        ("Keterangan", {"fields" : ['first_name', 'last_name', 'email', 'address', 'user', 'cust_note', 'total_price_comma','ongkir_comma', 'total_price_ongkir_comma']}),
        ("Status Pesanan", {"fields" : ['nomor_resi','status']})
    ]     
    inlines= [CartInline]
    list_filter = ['status']

    def ongkir_comma(self, obj):
        return "Rp. " + intcomma(obj.ongkir)

    def total_price_comma(self, obj):
        return "Rp. " + intcomma(obj.total_price)
    total_price_comma.short_description = 'Subtotal'

    def total_price_ongkir_comma (self, obj):
        return "Rp. " + intcomma(obj.total_final)
    total_price_ongkir_comma.short_description = 'Total'

    def save_model(self, request, obj, form, change):
        field = 'nomor_resi'
        super().save_model(request, obj, form, change)
        if change and field in form.changed_data and form.cleaned_data.get(field):
                
                items = Cart.objects.filter(order=obj.id)
                context = {'order' : obj}
                txt_content = render_to_string(
                    'admin/kirim-resi-alt.txt',
                    context
                )

                html_content = render_to_string(
                    'admin/kirim-resi.html',
                    context = {'order' : obj, 'products' : items, 'address' : None }
                )

                msg = EmailMultiAlternatives(
                    "Pesanan Anda Telah Kami Terima",
                    txt_content,
                    "admin@fetishia.store",
                    [obj.email],
                )
                
                msg.attach_alternative(html_content, "text/html")
                msg.send()

admin.site.register(Order, OrderAdmin)