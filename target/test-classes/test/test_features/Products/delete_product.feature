@debug
Feature: Delete Product Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Delete Invalid Product with Admin Access
    # login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the invalid product
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_product.graphql')
    And def variables = { productIds:[322]}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.deleteProduct.message == "Invalid Product!"

  Scenario: Delete Product without Admin Access
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # delete the product
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_product.graphql')
    And def variables = { productIds:[23]}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only ADMIN can Access!'

  Scenario: Delete Product with Admin Access
    # login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # delete the product
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_product.graphql')
    And def variables = { productIds:[23]}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.deleteProduct.message == 'Product(s) Deleted Successfully.'