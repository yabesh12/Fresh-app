@debug
Feature: Get All Sales Executives Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Get All Sales Executives without Manager Access
    # login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # get all sales executive
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('get_all_sales_executives.graphql')
    And request {query:'#(query)'}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only MANAGER or ADMIN can Access!'

  Scenario: Get All Sales Executives with Manager Access
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # get all sales executives
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('get_all_sales_executives.graphql')
    And request {query:'#(query)'}
    When method post
    Then status 200
    Then match response.data.allSalesExecutives[0].vehicleNumber == '12345'