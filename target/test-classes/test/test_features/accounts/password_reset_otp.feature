

@debug
Feature: Send Password Reset OTP Test

  Background:
    * url 'http://localhost:8009/graphql/'
    * def otp = ''
    * def mobile = '7878787878'

  Scenario: Send Password reset otp with Invalid mobile number
    Given path '/'
    Given def query = read('password_reset_otp.graphql')
    And def variables = {mobileNumber:85878}
    And request {query: '#(query)', variables:'#(variables)'}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Please enter a valid phone number'

  Scenario: Send Password reset otp with valid mobile number
    Given path '/'
    Given def query = read('password_reset_otp.graphql')
    And def variables = {mobileNumber:'#(mobile)'}
    And request {query: '#(query)', variables:'#(variables)'}
    When method post
    Then status 200
    Then print response
    * def otp = response.data.passwordResetOtp.otp
    Then print otp
    Then match response.data.passwordResetOtp.message == 'Otp successfully sent to your mobile number.'

  Scenario: Password reset otp verify with Invalid otp
    Given path '/'
    Given def query = read('password_reset_otp.graphql')
    And def variables = {mobileNumber:'#(mobile)'}
    And request {query: '#(query)', variables:'#(variables)'}
    When method post
    Then status 200
    Then print response
    * def otp = response.data.passwordResetOtp.otp
    Then print otp
    Then match response.data.passwordResetOtp.message == 'Otp successfully sent to your mobile number.'
    Given path '/'
    Given def query = read('password_reset_otp_verify.graphql')
    And def variables = {mobileNumber:'#(mobile)', otp:7844}
    And request {query: '#(query)', variables:'#(variables)'}
    When method post
    Then status 200
    Then print response
    Then match response.errors[0].message == 'otp not matched'

  Scenario: Password reset otp verify with valid otp
    Given path '/'
    Given def query = read('password_reset_otp.graphql')
    And def variables = {mobileNumber:'#(mobile)'}
    And request {query: '#(query)', variables:'#(variables)'}
    When method post
    Then status 200
    Then print response
    * def otp = response.data.passwordResetOtp.otp
    Then print otp
    Then match response.data.passwordResetOtp.message == 'Otp successfully sent to your mobile number.'
    Given path '/'
    Given def query = read('password_reset_otp_verify.graphql')
    And def variables = {mobileNumber:'#(mobile)', otp:'#(otp)'}
    And request {query: '#(query)', variables:'#(variables)'}
    When method post
    Then status 200
    Then print response
    Then match response.data.passwordResetOtpVerify.message == 'Otp verified.'