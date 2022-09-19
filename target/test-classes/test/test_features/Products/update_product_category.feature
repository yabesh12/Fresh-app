@debug
Feature: Update Product Category Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Update Product Category without Manager Access
    # Login as manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Update the product category
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_product_category.graphql')
    And def variables = { categoryId:4, name:IDLY BATTER }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only MANAGER or ADMIN can Access!'

  Scenario: Update the non existing category with Manager Access
    # Login as a Manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Update the category that not exists
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_product_category.graphql')
    And def variables = { categoryId:444, name:IDLY BATTER }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Category!'

  Scenario: Update Category with Invalid parent Id with Manager Access
    # Login as a Manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Update the category with invalid parent ID
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_product_category.graphql')
    And def variables = { parentId:122, categoryId:4, isActive:true, name:Idly Batter }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Parent Category!'

  Scenario: Update Category with Manager Access
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # update the category with valid data
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_product_category.graphql')
    And def variables = { categoryId:4, isActive:true, name:Idly Batter }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.updateCategory.category.name == 'Idly Batter'

  Scenario: Update Category with Admin Access
    # login as a admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # update the category with valid data
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_product_category.graphql')
    And def variables = { categoryId:4, isActive:true, name:Idly Batter }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.updateCategory.category.name == 'Idly Batter'
