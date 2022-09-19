@debug
Feature: Create Sales Executive Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Create Sales Executive without Manager Access
    # login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create sales executive
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_sales_executive.graphql')
    And def variables = { name: testsalesExecutive, mobileNumber:7878787878, password1:test, password2:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only MANAGER or ADMIN can Access!'

  Scenario: Create Sales Executive with Invalid mobile number
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create sales executive with invalid mobile number
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_sales_executive.graphql')
    And def variables = { name: testsalesExecutive, mobileNumber:78788, password1:test, password2:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Please enter a valid phone number'

  Scenario: Create Sales Executive with password mismatch
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create sales executive with password mismatch
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_sales_executive.graphql')
    And def variables = { name: testsalesExecutive1, mobileNumber:8578487584, password1:test, password2:ttest}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == "Password did not match please try again"



  Scenario: Create Existing Sales Executive with Manager Access
    # login as a Manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create sales executive that already exist
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_sales_executive.graphql')
    And def variables = { name: testsalesExecutive, mobileNumber:7878787878, password1:test, password2:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Username Already exists'

