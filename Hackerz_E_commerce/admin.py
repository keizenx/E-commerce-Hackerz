from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review, Coupon


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated', 'featured']
    list_filter = ['available', 'created', 'updated', 'featured', 'category']
    list_editable = ['price', 'stock', 'available', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'active', 'created']
    list_filter = ['active', 'rating', 'created']
    search_fields = ['title', 'comment', 'user__username', 'product__name']
    list_editable = ['active']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'paid', 'status', 'created']
    list_filter = ['paid', 'status', 'created', 'updated']
    search_fields = ['first_name', 'last_name', 'email', 'address']
    inlines = [OrderItemInline]
    list_editable = ['paid', 'status']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'min_purchase', 'used_count', 'max_uses', 'valid_from', 'valid_to', 'active']
    list_filter = ['active', 'discount_type', 'created']
    search_fields = ['code']
    list_editable = ['active']
    readonly_fields = ['used_count', 'created', 'updated']
    fieldsets = (
        ('Informations du Code', {
            'fields': ('code', 'active')
        }),
        ('Configuration de la Réduction', {
            'fields': ('discount_type', 'discount_value', 'min_purchase')
        }),
        ('Limites d\'utilisation', {
            'fields': ('max_uses', 'used_count')
        }),
        ('Période de validité', {
            'fields': ('valid_from', 'valid_to')
        }),
        ('Métadonnées', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Cart)
admin.site.register(CartItem)