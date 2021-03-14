# Django:
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

# Firstparty:
from grab_money.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        auth_admin.UserAdmin.fieldsets
    )  # (("User", {"fields": ("age", "language", "name")}),) + auth_admin.UserAdmin.fieldsets
    list_display = [
        "username",
        "is_superuser",
    ]  # "name", "age", "language"]
    search_fields = ["username"]
