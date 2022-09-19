@debug
Feature: Get all Price Groups Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: View all price groups with manager or admin access
    # login
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # View All Price Groups
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('get_all_price_groups.graphql')
    And request {query:'#(query)'}
    When method post
    Then status 200
    Then match response.data.priceGroups[0].name == 'premium'

  Scenario: View all price groups without login
    # View All Price Groups without Login
    Given path '/'
    Given def query = read('get_all_price_groups.graphql')
    And request {query:'#(query)'}
    When method post
    Then status 200
    Then match response.errors[0].message == 'You do not have permission to perform this action'

  Scenario: View all price groups with Sales Executive Access
    # login
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # View All Price Groups without Login
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('get_all_price_groups.graphql')
    And request {query:'#(query)'}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only MANAGER or ADMIN can Access!'