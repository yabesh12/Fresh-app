@debug
Feature: Delete Product Type Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Delete Invalid Product Type with Admin Access
    # Login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the Invalid product Type
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_product_type.graphql')
    And def variables = { productTypeIds:[1,3,4]}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.deleteProductType.message == "Invalid Product Type!"

  Scenario: Delete Product Type without Admin Access
    # Login as a Manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the product type
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_product_type.graphql')
    And def variables = { productTypeIds:[23]}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only ADMIN can Access!'

  Scenario: Delete Product Type with Admin Access
    # Login as Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the product type
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_product_type.graphql')
    And def variables = { productTypeIds:[23]}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.deleteProductType.message == 'ProductTypes Deleted Successfully.'