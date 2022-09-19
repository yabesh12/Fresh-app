@debug
Feature: Create and Update Route Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Create Route without Manager Access
    # login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create route
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_or_update_route.graphql')
    And def variables = { name:vadapalani-nungambakkam, startingPoint:vadapalani, endingPoint:nungambakkam, description:vadapalani-nungambakkam-route }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only MANAGER or ADMIN can Access!'

  Scenario: Create or Update Existing Route with Manager Access
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    #  create or update route
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_or_update_route.graphql')
    And def variables = { name:vadapalani-nungambakkam, startingPoint:vadapalani, endingPoint:nungambakkam, description:vadapalani-nungambakkam-route }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createUpdateRoute.message == "Route vadapalani-nungambakkam updated successfully." || response.data.createUpdateRoute.message == 'New Route vadapalani-nungambakkam created successfully.'

  Scenario: Update Existing Route without Manager Access
    # login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # update existing route
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_or_update_route.graphql')
    And def variables = { name:vadapalani-nungambakkam, startingPoint:vadapalani, endingPoint:nungambakkam, description:vadapalani-nungambakkam-route }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == "Only MANAGER or ADMIN can Access!"
