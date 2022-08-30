from graphql import GraphQLError


def validate_mobile_number(mobile_number):
    """
    Validates the mobile number.
    """
    if not mobile_number.isdigit():
        raise GraphQLError("Please enter a valid phone number")
    if len(mobile_number) != 10:
        raise GraphQLError("Please enter a valid phone number")
    return mobile_number