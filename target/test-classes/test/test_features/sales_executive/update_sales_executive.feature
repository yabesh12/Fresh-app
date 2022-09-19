@debug
Feature: Update Sales Executive Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Update Sales Executive without Manager Access
    # login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # update the sales executive
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_sales_executive.graphql')
    And def variables = { salesExecutiveId:U2FsZXNFeGVjdXRpdmVUeXBlOjQ=, dateOfBirth:1999-06-20,vehicleNumber:37378}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only MANAGER or ADMIN can Access!'

  Scenario: Update the Sales Executive who does not exist with Manager Access
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # update the sales executive
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_sales_executive.graphql')
    And def variables = { salesExecutiveId:U2FsZXNFeGVjdXRpdmVUeXBlOjU=, dateOfBirth:1999-06-20,vehicleNumber:37378}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Sales Executive does not exist.'

