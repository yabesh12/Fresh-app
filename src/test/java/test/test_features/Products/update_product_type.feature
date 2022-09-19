@debug
Feature: Update Product Type Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Update Product Type without Manager Access
    # login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # update the product type
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_product_type.graphql')
    And def variables = { productTypeId:11,tax:10.00, unit:PACKET, isCreditAvailable:true, isActive:true}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only MANAGER or ADMIN can Access!'

  Scenario: Update Product Type with Invalid Product Type Id with Manager Access
    # login as a Manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # update the product type with invalid Product Type
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_product_type.graphql')
    And def variables = { productTypeId:101,tax:10.00, unit:PACKET, isCreditAvailable:true, isActive:true}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid ProductType!'

  Scenario: Update Product Type with Invalid parent Id with Manager Access
    # login as manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # update the product type with invalid parent ID
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_product_type.graphql')
    And def variables = { parentId:122, productTypeId:23,tax:10.00, unit:PACKET, isCreditAvailable:true, isActive:true}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Parent ProductType!'

  Scenario: Update Product Type with Manager Access
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # update the product type with valid data
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_product_type.graphql')
    And def variables = { productTypeId:23,tax:20.00, unit:PACKET, isCreditAvailable:false, isActive:false}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.updateProductType.productType.tax == '20' || response.data.isCreditAvailable == false || response.data.isActive == false

  Scenario: Update Product Type with Admin Access
    # login as a admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # update the product type with valid data
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_product_type.graphql')
    And def variables = { productTypeId:23,tax:20.00, unit:PACKET, isCreditAvailable:false, isActive:false}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.updateProductType.productType.tax == '20' || response.data.isCreditAvailable == false || response.data.isActive == false
