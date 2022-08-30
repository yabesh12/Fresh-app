

@debug
Feature: User Login Test

  Background:
    * url 'http://localhost:8009/graphql/'
    * def token = ""

  Scenario: Login with Invalid username or password
    Given path '/'
    Given def query = read('login.graphql')
    And def variables = {username:testinguser, password:testuserr}
    And request {query: '#(query)', variables:'#(variables)'}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Please enter valid credentials'

  Scenario: login with valid username
      Given path '/'
      Given def query = read('login.graphql')
      And def variables = {username:defaultuser, password:defaultuser}
      And request {query:'#(query)',variables:"#(variables)"}
      When method post
      Then status 200
      * def token = response.data.tokenAuth.token
      Then print token

