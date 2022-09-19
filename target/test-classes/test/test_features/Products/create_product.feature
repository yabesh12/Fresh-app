@debug
Feature: Create Product Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Create Product without Manager Access
    # Login as a Sales Executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Create product
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_product.graphql')
    And def variables = { sku: D001, name:dosa batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only MANAGER or ADMIN can Access!'

  Scenario: Create Product with Invalid parent Id with Manager Access
    # Login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Create Product with Invalid Parent Id
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_product.graphql')
    And def variables = { sku: D001, name:dosa batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50, parentId:433434 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Parent Product!'

  Scenario: Create Product with not existing category with Manager Access
    # Login as a Manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token

    # Create product with Invalid category
    Given def query = read('create_product.graphql')
    And def variables = { sku: D001, name:dosa batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50, parentId:1, categoryId:554}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Category!'

  Scenario: Create Product with not existing product type with Manager Access
    # Login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Create product with Invalid product type
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_product.graphql')
    And def variables = { sku: D001, name:dosa batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50, parentId:1, categoryId:3, productTypeId:6565}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid ProductType!'

  Scenario: Create Product that already existing with Manager Access
    # Login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Create the product that already exists
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_product.graphql')
    And def variables = { sku: D002, name:Dosa Batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createProduct.message == 'Product - D002 already Exists. Please Change SKU and Try Again!'

  Scenario: Create Product with valid data with Manager Access
    # login as a manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create product with valid data
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_product.graphql')
    And def variables = { sku: D003, name:dosa batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createProduct.product.name == 'dosa batter'

  Scenario: Create Product with valid data with Admin Access
    # login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Create Product with valid data
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_product.graphql')
    And def variables = { sku: D004, name:Dosa Batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createProduct.product.name == 'Dosa Batter'



