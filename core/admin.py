from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """
    Admin base com configurações de auditoria
    Todos os admins podem herdar dele
    """
    readonly_fields = ['created_at', 'updated_at', 'user_created', 'user_updated']

    # Remove dos formulários
    exclude = ['user_created', 'user_updated']
