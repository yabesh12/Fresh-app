from graphql import GraphQLError


def manager_only(view_func):
    """
    Only MANAGER or ADMIN can perform actions if used
    """

    def wrapper_func(self, info, *args, **kwargs):
        user = info.context.user
        print(user.is_superuser)
        if user is None or user.is_anonymous:
            raise GraphQLError("User must login!")
        if not user.is_manager and not user.is_admin:
            raise GraphQLError("Only MANAGER or ADMIN can Access!")
        return view_func(self, info, *args, **kwargs)

    return wrapper_func


def admin_only(view_func):
    """
    Only ADMIN can perform actions if used
    """

    def wrapper_func(self, info, *args, **kwargs):
        user = info.context.user
        if user is None or user.is_anonymous:
            raise GraphQLError("User must login!")
        if not user.is_admin:
            raise GraphQLError("Only ADMIN can Access!")
        return view_func(self, info, *args, **kwargs)

    return wrapper_func
