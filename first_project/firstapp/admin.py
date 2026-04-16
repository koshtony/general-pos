from django.contrib import admin
from django.db.models import Sum
from unfold.admin import ModelAdmin
from .models import (
    Shops, Stocks, Cart, Sales, Invoices, Paid, mpesaPay, 
    Expenses, Transfers, Location, Tasks, Debts, Contacts, Organisation, Customers
)

# --- Mixins for common styling ---
class BaseAdmin(ModelAdmin):
    compressed_fields = True  # Makes the form more compact
    list_filter_submit = True  # Adds a "Filter" button to prevent unnecessary reloads
    list_fullwidth = True

@admin.register(Shops)
class ShopsAdmin(BaseAdmin):
    list_display = ("shop_name", "shop_cat", "shop_loc", "shop_created")
    search_fields = ("shop_name", "shop_cat")
    filter_horizontal = ("shop_auth",) # Styled many-to-many widget

@admin.register(Stocks)
class StocksAdmin(BaseAdmin):
    list_display = ("p_name", "p_qty", "p_price", "p_cost", "p_shop", "p_created")
    list_filter = ("p_shop", "p_category")
    search_fields = ("p_name", "p_serial")
    
    # Organizing inputs into sections (Styled by Unfold)
    fieldsets = (
        ("Basic Info", {
            "fields": (("p_name", "p_serial"), "p_category", "p_desc", "p_image")
        }),
        ("Inventory & Pricing", {
            "fields": (("p_qty", "p_price", "p_cost"), ("p_vat", "p_disc"))
        }),
        ("Ownership", {
            "fields": ("p_shop", "p_creator", "p_created")
        }),
    )

@admin.register(Sales)
class SalesAdmin(BaseAdmin):
    list_display = ("s_order_code", "s_name", "s_qty", "s_price", "s_profit", "s_status", "s_created")
    list_filter = ("s_status", "s_type", "s_shop")
    search_fields = ("s_order_code", "s_name")
    readonly_fields = ("s_created",)

@admin.register(Invoices)
class InvoicesAdmin(BaseAdmin):
    list_display = ("i_code", "i_name", "i_qty", "i_price", "i_status", "i_created")
    list_filter = ("i_status", "i_shop")

@admin.register(Paid)
class PaidAdmin(BaseAdmin):
    list_display = ("sn", "product", "qty", "amount", "profit", "waiter", "date")
    list_filter = ("pay_type", "waiter")

@admin.register(mpesaPay)
class MpesaPayAdmin(BaseAdmin):
    list_display = ("trans_id", "name", "phone", "amount", "date")
    search_fields = ("trans_id", "phone", "ref_no")

@admin.register(Expenses)
class ExpensesAdmin(BaseAdmin):
    list_display = ("exp_desc", "exp_amount", "exp_shop", "exp_creator", "exp_date")

@admin.register(Debts)
class DebtsAdmin(BaseAdmin):
    list_display = ("debt_cus", "debt_amnt", "debt_rem", "debt_last")
    search_fields = ("debt_cus",)

@admin.register(Organisation)
class OrganisationAdmin(BaseAdmin):
    list_display = ("org_name", "org_creator", "org_created")
    fieldsets = (
        (None, {"fields": ("org_name", "logo")}),
        ("Details", {"fields": ("org_details", "org_summary_notes")}),
        ("Admin", {"fields": ("org_creator", "org_created")}),
    )

@admin.register(Customers)
class CustomersAdmin(BaseAdmin):
    list_display = ("cus_name", "cus_phone", "cus_email", "cus_ref_code")
    search_fields = ("cus_name", "cus_phone")

# Registering remaining models with default ModelAdmin styling
admin.site.register(Cart, BaseAdmin)
admin.site.register(Transfers, BaseAdmin)
admin.site.register(Location, BaseAdmin)
admin.site.register(Tasks, BaseAdmin)
admin.site.register(Contacts, BaseAdmin)