@debug
Feature: Delete the Sales Executive

  Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Delete the Sales Executive without Admin Access
    Given path '/'
    Given def query = read('login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_sales_executive.graphql')
    And def variables = { salesExecutiveId:3}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only ADMIN can Access!'


  Scenario: Delete the Sales Executive with Admin Access
    Given path '/'
    Given def query = read('login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_sales_executive.graphql')
    And def variables = { salesExecutiveId:3}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.deleteSalesExecutive.message == 'Successfully deleted the Sales Executive.'