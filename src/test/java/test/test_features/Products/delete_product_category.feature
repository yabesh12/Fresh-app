@debug
Feature: Delete Category Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Delete Invalid Category with Admin Access
    # login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the invalid category
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_product_category.graphql')
    And def variables = { categoryIds:[145,31]}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.deleteCategory.message == "Invalid Category!"

  Scenario: Delete Category without Admin Access
    # login as a Manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the category
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_product_category.graphql')
    And def variables = { categoryIds:[24]}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only ADMIN can Access!'

  Scenario: Delete Category with Admin Access
    # Login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the category
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_product_category.graphql')
    And def variables = { categoryIds:[22]}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.deleteCategory.message == 'Category(s) Deleted Successfully!'