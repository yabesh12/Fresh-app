@debug
Feature: Delete Route Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""


  Scenario: Delete the Invalid Route with Admin Access
    # login as a admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # delete route
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_route.graphql')
    And def variables = { routeId:Um91dGVUeXBlOjE= }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then print response
    Then status 200
    Then match response.errors[0].message == 'Invalid Route!'