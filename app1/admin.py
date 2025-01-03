from django.contrib import admin
from .models import UserRelation
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User
from .models import Messages

from accounts.models import CustomUser  # accounts で定義した CustomUser をインポート
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm  # 必要なフォームもインポート
from accounts.admin import CustomUserAdmin

from django.contrib.auth import get_user_model


class MessagesAdmin(admin.ModelAdmin):
    list_display = ("sender_name", "receiver_name", "time", "seen")
    list_filter = ("sender_name", "receiver_name", "seen")
    search_fields = ("sender_name__username", "receiver_name__username", "description")


admin.site.register(Messages, MessagesAdmin)


# Define a custom admin class for the User model
#class CustomUserAdmin(UserAdmin):
#    list_display = (
#        "id",
#        "username",
#        "email",
#        "first_name",
#        "last_name",
#        "is_staff",
#        "date_joined",
#    )
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']



# Unregister the default UserAdmin
admin.site.unregister(get_user_model())

# カスタムユーザーモデルを管理画面に登録
admin.site.register(CustomUser, CustomUserAdmin)
# Register the User model with the custom admin class
# admin.site.register(get_user_model(), CustomUserAdmin)


class UserRelationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "friend", "accepted")
    list_filter = ("user", "accepted")
    search_fields = ("user__username", "friend")


admin.site.register(UserRelation, UserRelationAdmin)
