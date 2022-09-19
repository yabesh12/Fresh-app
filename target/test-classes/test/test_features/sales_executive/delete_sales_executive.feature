@debug
Feature: Delete the Sales Executive

  Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Delete the Sales Executive without Admin Access
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the sales executive
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_sales_executive.graphql')
    And def variables = { salesExecutiveId:U2FsZXNFeGVjdXRpdmVUeXBlMw== }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only ADMIN can Access!'


  Scenario: Delete the Invalid Sales Executive with Admin Access
    # login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the sales executive
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_sales_executive.graphql')
    And def variables = { salesExecutiveId:U2FsZXNFeGVjdXRpdmVUeXBlOjU= }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Sales Executive.'