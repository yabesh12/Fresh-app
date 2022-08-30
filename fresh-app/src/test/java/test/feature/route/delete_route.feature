@debug
Feature: Delete Route Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Delete Invalid Route with Admin Access
    Given path '/'
    Given def query = read('login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_route.graphql')
    And def variables = { routeId:5 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Route!'

  Scenario: Delete Route with Admin Access
    Given path '/'
    Given def query = read('login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_route.graphql')
    And def variables = { routeId:9 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.deleteRoute.message == 'Successfully deleted the route'