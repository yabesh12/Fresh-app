@debug
Feature: Get all Routes Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Get All Routes
    # login as sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Get all routes
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('get_all_routes.graphql')
    And request {query:'#(query)'}
    When method post
    Then status 200
    Then match response.data.allRoutes[0].name == 'koyambedu-nungambakkam'

  Scenario: Get All Routes without login
    Given path '/'
    Given def query = read('get_all_routes.graphql')
    And request {query:'#(query)'}
    When method post
    Then status 200
    Then match response.errors[0].message == 'You do not have permission to perform this action'


  Scenario: Get Single Route
    # login as sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Get single routes
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('get_single_route.graphql')
    And def variables = { routeId:Um91dGVUeXBlOjEw }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.getRoute.name == 'koyambedu-nungambakkam'