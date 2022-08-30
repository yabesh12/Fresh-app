
@debug
Feature: Password Reset OTP Send Test

  Background:
    * url 'http://localhost:8009/graphql/'

  Scenario: Password reset otp send with Invalid mobile number
    Given path '/'
    Given def query = read('password_reset_otp.graphql')
    And def variables = {mobileNumber:85878}
    And request {query: '#(query)', variables:'#(variables)'}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Please enter a valid phone number'