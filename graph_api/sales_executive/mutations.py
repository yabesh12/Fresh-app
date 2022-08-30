import graphene
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from address.models import Address
from graph_api.accounts.decorators import manager_only, admin_only
from graph_api.core.utils import validate_mobile_number
from sales_executive.models import SalesExecutive

User = get_user_model()


class CreateSalesExecutive(graphene.Mutation):
    """
    Create Sales Executive only by manager
    """

    class Arguments:
        name = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
        date_of_birth = graphene.Date()
        mobile_number = graphene.String(required=True)
        is_active = graphene.Boolean()
        vehicle_number = graphene.String()

    status = graphene.String()
    message = graphene.String()

    @login_required
    @manager_only
    @transaction.atomic
    def mutate(self, info, name, password1, password2,
               mobile_number, **kwargs):
        try:
            validate_mobile_number(mobile_number)
            user_objs = User.objects.filter(Q(username=name) & Q(mobile_number=mobile_number))
            if user_objs.exists():
                raise GraphQLError("Username Already exists")
            user_obj = User(username=name)
            user_obj.mobile_number = mobile_number
            if password1 != password2:
                raise GraphQLError("Password did not match please try again")
            user_obj.set_password(password1)
            user_obj.save()
            vehicle_no = kwargs.get('vehicle_number')
            date_of_birth = kwargs.get('date_of_birth')
            is_active = kwargs.get('is_active', '')
            sales_executive_obj = SalesExecutive(user=user_obj, date_of_birth=date_of_birth, vehicle_number=vehicle_no)
            if is_active != '':
                sales_executive_obj.is_active = is_active
            sales_executive_obj.save()
        except Exception as e:
            return e

        return CreateSalesExecutive(status="ok",
                                    message=f"Added new Sales Executive - {user_obj.username} successfully.")


class UpdateSalesExecutive(graphene.Mutation):
    """
    Manager can
    -> Update the sales executive's DOB, vehicle no, is_active
    Admin can
    -> Update the sales executive's DOB, vehicle no, is_active and mobile no
    """

    class Arguments:
        sales_executive_id = graphene.ID(required=True)
        date_of_birth = graphene.Date()
        mobile_number = graphene.String()
        is_active = graphene.Boolean()
        vehicle_number = graphene.String()

    status = graphene.String()
    message = graphene.String()

    @login_required
    @manager_only
    def mutate(self, info, sales_executive_id, **kwargs):
        try:
            with transaction.atomic():
                sales_executive_obj = SalesExecutive.objects.filter(id=sales_executive_id).exclude(
                    is_deleted=True).first()
                if sales_executive_obj is not None:
                    if vehicle_no := kwargs.get('vehicle_number'):
                        sales_executive_obj.vehicle_number = vehicle_no
                    if is_active := kwargs.get('is_active'):
                        sales_executive_obj.is_active = is_active
                    if date_of_birth := kwargs.get('date_of_birth'):
                        sales_executive_obj.date_of_birth = date_of_birth
                    sales_executive_obj.save(update_fields=['is_active', 'vehicle_number', 'date_of_birth'])
                    user_obj = User.objects.filter(username=sales_executive_obj.user.username).first()
                    requested_user = info.context.user
                    if user_obj is None:
                        raise GraphQLError("User does not exist.")
                    elif user_obj is not None and requested_user.is_admin:
                        mobile_no = kwargs.get('mobile_number', '')
                        if mobile_no != '':
                            validate_mobile_number(mobile_no)
                            user_obj.mobile_number = mobile_no
                            user_obj.save(update_fields=['mobile_number'])
                    else:
                        return UpdateSalesExecutive(status="ok",
                                                    message=f"Updated Sales Executive - {user_obj.username} details successfully. Only Admin can update sales executive's mobile number!",
                                                    )
                else:
                    raise GraphQLError("Sales Executive does not exist.")

        except Exception as e:
            return e

        return UpdateSalesExecutive(status="ok",
                                    message=f"Updated Sales Executive - {user_obj.username} details successfully.")


class CreateSalesExecutivePermanentAddress(graphene.Mutation):
    """
    Create Sales Executive permanent address only by manager
    """

    class Arguments:
        sales_executive_id = graphene.ID(required=True)
        address_line1 = graphene.String(required=True)
        address_line2 = graphene.String()
        city = graphene.String(required=True)
        state = graphene.String(required=True)
        pincode = graphene.String(required=True)
        country = graphene.String(required=True)
        is_active = graphene.Boolean(required=True)

    status = graphene.String()
    message = graphene.String()

    @login_required
    @manager_only
    @transaction.atomic
    def mutate(self, info, sales_executive_id, address_line1, city, state, pincode, country, is_active, **kwargs):
        try:
            sales_executive_obj = SalesExecutive.objects.filter(id=sales_executive_id).exclude(is_deleted=True).first()
            if sales_executive_obj is not None:
                address_line2 = kwargs.get('address_line2')
                address_obj = Address.objects.create(address_line1=address_line1, address_line2=address_line2,
                                                     city=city, state=state, pincode=pincode, country=country,
                                                     is_active=is_active)
                sales_executive_obj.permanent_address = address_obj
                sales_executive_obj.save()

            else:
                raise GraphQLError("Sales Executive is not exists.")
        except Exception as e:
            return e

        return CreateSalesExecutivePermanentAddress(status="Ok",
                                                    message=f"Sales Executive {sales_executive_obj.user.username} permanent address details Created successfully.")


class CreateSalesExecutiveTemporaryAddress(graphene.Mutation):
    """
    Create Sales Executive temporary address only by manager
    """

    class Arguments:
        sales_executive_id = graphene.ID(required=True)
        address_line1 = graphene.String(required=True)
        address_line2 = graphene.String()
        city = graphene.String(required=True)
        state = graphene.String(required=True)
        pincode = graphene.String(required=True)
        country = graphene.String(required=True)

        is_active = graphene.Boolean()

    status = graphene.String()
    message = graphene.String()

    @login_required
    @manager_only
    @transaction.atomic
    def mutate(self, info, sales_executive_id, address_line1, city, state, pincode, country, **kwargs):
        try:
            sales_executive_obj = SalesExecutive.objects.filter(id=sales_executive_id).exclude(is_deleted=True).first()
            if sales_executive_obj is not None:
                address_line2 = kwargs.get('address_line2')
                address_obj = Address.objects.create(address_line1=address_line1, address_line2=address_line2,
                                                     city=city, state=state, pincode=pincode, country=country)
                sales_executive_obj.temporary_address = address_obj
                sales_executive_obj.save()

            else:
                raise GraphQLError("Sales Executive is not exists.")
        except Exception as e:
            return e

        return CreateSalesExecutiveTemporaryAddress(status="Ok",
                                                    message=f"Sales Executive {sales_executive_obj.user.username} temporary address details Created successfully.")


class DeleteSalesExecutive(graphene.Mutation):
    """
    Admin can
    -> Remove the sales executive if sales executive exists
    """

    class Arguments:
        sales_executive_id = graphene.ID(required=True)

    message = graphene.String()

    @login_required
    @admin_only
    def mutate(self, info, sales_executive_id, **kwargs):

        try:
            sales_executive_obj = SalesExecutive.objects.get(id=sales_executive_id)
            sales_executive_obj.is_deleted = True
            sales_executive_obj.save(update_fields=['is_deleted'])

        except SalesExecutive.DoesNotExist:
            raise GraphQLError(f'Invalid Sales Executive.')

        return DeleteSalesExecutive(message="Successfully deleted the Sales Executive.")


class SalesExecutiveMutation(graphene.ObjectType):
    create_sales_executive = CreateSalesExecutive.Field()
    update_sales_executive = UpdateSalesExecutive.Field()
    create_sales_executive_permanent_address = CreateSalesExecutivePermanentAddress.Field()
    create_sales_executive_temporary_address = CreateSalesExecutiveTemporaryAddress.Field()
    delete_sales_executive = DeleteSalesExecutive.Field()
