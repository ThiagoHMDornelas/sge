from rest_framework.permissions import BasePermission, SAFE_METHODS


class ModelPermissionsByMethod(BasePermission):
    """
    Permissões genéricas baseadas no model da view
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        model = getattr(view, 'queryset', None)
        if model is None:
            return False

        model_name = model.model._meta.model_name
        app_label = model.model._meta.app_label

        if request.method in SAFE_METHODS:
            return user.has_perm(f'{app_label}.view_{model_name}')

        if request.method == 'POST':
            return user.has_perm(f'{app_label}.add_{model_name}')

        if request.method in ['PUT', 'PATCH']:
            return user.has_perm(f'{app_label}.change_{model_name}')

        if request.method == 'DELETE':
            return user.has_perm(f'{app_label}.delete_{model_name}')

        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


# from rest_framework.permissions import BasePermission, SAFE_METHODS


# class BrandPermissions(BasePermission):

#     def has_permission(self, request, view):
#         user = request.user

#         if not user or not user.is_authenticated:
#             return False

#         # LISTAR
#         if request.method == 'GET':
#             return user.has_perm('brands.view_brand')

#         # CRIAR
#         if request.method == 'POST':
#             return user.has_perm('brands.add_brand')

#         # UPDATE
#         if request.method in ['PUT', 'PATCH']:
#             return user.has_perm('brands.change_brand')

#         # DELETE
#         if request.method == 'DELETE':
#             return user.has_perm('brands.delete_brand')

#         return False

#     def has_object_permission(self, request, view, obj):
#         user = request.user

#         # LEITURA (DETAIL)
#         if request.method in SAFE_METHODS:
#             return user.has_perm('brands.view_brand')

#         # UPDATE
#         if request.method in ['PUT', 'PATCH']:
#             return user.has_perm('brands.change_brand')

#         # DELETE
#         if request.method == 'DELETE':
#             return user.has_perm('brands.delete_brand')

#         return False
