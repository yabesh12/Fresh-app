import random
import graphene
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.validators import validate_email
from django.db.models import Q
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_jwt.refresh_token.models import RefreshToken
from graphql_jwt.shortcuts import get_token

from account.utils import generate_jti
from graph_api.core.utils import validate_mobile_number

User = get_user_model()


class CreateUser(graphene.Mutation):
    """
    Register the user
    -> If user not exists
    -> If mobile no, email and password is valid
    """

    class Arguments:
        username = graphene.String(required=True)
        mobile_number = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
        email = graphene.String()

    status = graphene.String()
    message = graphene.String()

    def mutate(self, info, username, mobile_number, password1, password2, **kwargs):
        user_objs = User.objects.filter(Q(username=username) | Q(mobile_number=mobile_number))
        if user_objs.exists():
            raise GraphQLError("Username Already exists")
        user_obj = User(username=username)
        validate_mobile_number(mobile_number)
        user_obj.mobile_number = mobile_number
        email = kwargs.get('email', '')
        if email != '':
            validate_email(email)
        user_obj.email = email
        if password1 != password2:
            raise GraphQLError("Password does not match please try again.")
        user_obj.set_password(password1)
        user_obj.save()
        return CreateUser(status="ok", message="Registered Successfully.")


class LogoutUser(graphene.Mutation):
    """
    Logout the user
    -> change the jti payload
    -> remove the refresh tokens
    """
    status = graphene.String()
    message = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        user_obj = info.context.user
        user_obj.jti = generate_jti()
        try:
            refresh_tokens = RefreshToken.objects.filter(user=user_obj)
            refresh_tokens.delete()
            user_obj.save()
        except Exception as e:
            return e
        return LogoutUser(status="Ok", message="Logged out successfully!")


class PasswordResetOtp(graphene.Mutation):
    """
    Send otp if user exists for password reset
    """

    class Arguments:
        mobile_number = graphene.String(required=True)

    status = graphene.String()
    message = graphene.String()
    otp = graphene.String()

    def mutate(self, info, mobile_number):
        validate_mobile_number(mobile_number)
        user_obj = User.objects.filter(mobile_number=mobile_number)
        if user_obj.exists():
            cache_time = 300  # cache time 5 minutes
            cache_key = mobile_number
            value = cache.get(cache_key)
            if value is not None:
                try:
                    result = cache.get(cache_key)
                except Exception as e:
                    return e
            else:
                try:
                    otp = random.randint(1000, 9999)
                    cache.set(cache_key, otp, cache_time)
                    result = cache.get(cache_key)
                except Exception as e:
                    return e
        else:
            raise GraphQLError("User not exists.")

        return PasswordResetOtp(status="Ok", otp=result, message="Otp successfully sent to your mobile number.")


class PasswordResetOtpVerify(graphene.Mutation):
    """
    Verify the Otp for password reset
    """

    class Arguments:
        mobile_number = graphene.String(required=True)
        otp = graphene.Int(required=True)

    status = graphene.String()
    token = graphene.String()
    message = graphene.String()

    def mutate(self, info, mobile_number, otp):
        validate_mobile_number(mobile_number)
        try:
            user_obj = User.objects.filter(mobile_number=mobile_number)
            if user_obj.exists():
                cache_key = mobile_number
                value = cache.get(cache_key)
                if otp != value:
                    raise GraphQLError("otp not matched")
            else:
                raise GraphQLError("User not exists.")
        except Exception as e:
            return e
        token = get_token(user_obj.first())
        return PasswordResetOtpVerify(status="Ok", message="Otp verified.", token=token)


class PasswordReset(graphene.Mutation):
    """
    Reset the password with new password
    """

    class Arguments:
        password = graphene.String(required=True)
        confirm_password = graphene.String(required=True)

    status = graphene.String()
    message = graphene.String()

    @login_required
    def mutate(self, info, password, confirm_password):
        try:
            user = info.context.user
            if password != confirm_password:
                raise GraphQLError("Password does not match.")
            else:
                user.set_password(password)
                user.save()
        except Exception as e:
            return e

        return PasswordResetOtpVerify(status="Ok", message=f"Password changed successfully for {user.username}.")


class AccountMutation(graphene.ObjectType):
    sign_up = CreateUser.Field()
    logout = LogoutUser.Field()
    password_reset_otp = PasswordResetOtp.Field()
    password_reset_otp_verify = PasswordResetOtpVerify.Field()
    password_reset = PasswordReset.Field()
