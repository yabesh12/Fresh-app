@debug
Feature: User Registration Test

Background:
     * url 'http://localhost:8009/graphql/'

Scenario: user registration with existing user credentials
    Given path '/'
    Given def query = read('registration.graphql')
    And def variables = { username: testuser, mobileNumber:9999999999, password1:test, password2:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Username Already exists'

Scenario: user registration using invalid phone number
    Given path '/'
    Given def query = read('registration.graphql')
    And def variables = { username: defaultuser1, mobileNumber:8888, password1:test, password2:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Please enter a valid phone number'

Scenario: user registration using invalid email
    Given path '/'
    Given def query = read('registration.graphql')
    And def variables = { username: defaultuser4, mobileNumber:8659497948,email:test@,password1:test, password2:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == "['Enter a valid email address.']"


Scenario: user registration with password mismatch
    Given path '/'
    Given def query = read('registration.graphql')
    And def variables = { username: defaultuser5, mobileNumber:8787848787, password1:test, password2:testt}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Password does not match please try again.'

Scenario: user registration with valid data
    Given path '/'
    Given def query = read('registration.graphql')
    And def variables = { username: defaultuser, mobileNumber:9696969696, email:test@gmail.com, password1:test, password2:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200