@debug
Feature: Create Product Type Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Create Product Type without Manager Access
    # login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create product type
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_product_type.graphql')
    And def variables = { title:Batter,tax:10.00, unit:PACKET, isCreditAvailable:true, isActive:true}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only MANAGER or ADMIN can Access!'

  Scenario: Create Product Type with Invalid parent Id with Manager Access
    # Login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create product type with invalid parent ID
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_product_type.graphql')
    And def variables = { title:Batter,tax:10.00, unit:PACKET, isCreditAvailable:true, isActive:true, parentId:55}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Parent Product!'

  Scenario: Create Product Type with Manager Access
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create product type with valid data
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_product_type.graphql')
    And def variables = { title:batter,tax:10.00, unit:PACKET, isCreditAvailable:true, isActive:true}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createProductType.productType.title == 'batter'


  Scenario: Create Product Type with Admin Access
    # login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create product type with valid data
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_product_type.graphql')
    And def variables = { title:Batter,tax:10.00, unit:PACKET, isCreditAvailable:true, isActive:true}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createProductType.productType.title == 'Batter'