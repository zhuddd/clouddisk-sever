from django.contrib import admin

from file.models import Files, FileUser


# Register your models here.
@admin.register(Files)
class MyAdmin(admin.ModelAdmin):
    list_display = ("id", "size", "broken")
    search_fields = ("id",)
    readonly_fields = ("hash", "check_hash", "size",)


@admin.register(FileUser)
class MyAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "file_name", "file_type", "parent_folder", "file", "file_face", "is_folder", "is_delete",
        "is_uploaded", "upload_time")
    search_fields = (
        "id", "user__id", "user__email", "file_name", "file_type", "parent_folder")
    list_filter = ("file_face", "is_folder", "is_delete", "is_uploaded", "upload_time")
    autocomplete_fields = ("file", "user")
    readonly_fields = (
        "id", "user", "file_name", "file_type", "parent_folder", "file", "file_face", "is_folder",  "upload_time")
