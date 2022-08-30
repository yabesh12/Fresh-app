@debug
Feature: Get all Price Groups Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: View all price groups
    Given path '/'
    Given def query = read('login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('get_all_price_groups.graphql')
    And request {query:'#(query)'}
    When method post
    Then status 200
    Then match response.data.priceGroups[0].name == 'economy'

  Scenario: View all price groups without login
    Given path '/'
    Given def query = read('get_all_price_groups.graphql')
    And request {query:'#(query)'}
    When method post
    Then status 200
    Then match response.data.priceGroups[0].name == 'economy'