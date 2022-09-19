@debug
Feature: Create Order Test

  Background:
    * url 'http://localhost:8009/graphql/'
    * def token = ""

  Scenario: Create Order without Login
    # Create product
    Given def query = read('create_order.graphql')
    And def variables = { data:{shopId:U2hvcFR5cGU6MQ==, orderItems:[{productId:U2hvcFR5cGU6MQ==, quantity:1}] } }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'You do not have permission to perform this action'

  Scenario: Create Order with Invalid shop
    # Login as a Sales Executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Create Order with Invalid Shop Id
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_order.graphql')
    And def variables = { data:{shopId:U2hvcFR5cGU6Mg==, orderItems:[{productId:U2hvcFR5cGU6MQ==, quantity:1}] } }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Shop does not exist'

  Scenario: Create Order with Valid data
    # Login as a Manager
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token

    # Create order with Valid details
    Given def query = read('create_order.graphql')
    And def variables = { data: { shopId:U2hvcFR5cGU6MQ==, orderItems:[{productId:UmVhbFByb2R1Y3RUeXBlOjEx, quantity:1 }] } }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createOrder.message == 'Order Created Successfully!'


#    # Create product with Invalid product type
#    * def token = response.data.tokenAuth.token
#    * header Authorization = "JWT"+" "+token
#    Given def query = read('create_product.graphql')
#    And def variables = { sku: D001, name:dosa batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50, parentId:1, categoryId:3, productTypeId:6565}
#    And request {query:'#(query)',variables:"#(variables)"}
#    When method post
#    Then status 200
#    Then match response.errors[0].message == 'Invalid ProductType!'
#
#  Scenario: Create Product that already existing with Manager Access
#    # Login as a manager
#    Given path '/'
#    Given def query = read('../accounts/login.graphql')
#    And def variables = {username:testuser, password:testuser}
#    And request {query:'#(query)',variables:"#(variables)"}
#    When method post
#    Then status 200
#
#    # Create the product that already exists
#    * def token = response.data.tokenAuth.token
#    * header Authorization = "JWT"+" "+token
#    Given def query = read('create_product.graphql')
#    And def variables = { sku: D002, name:Dosa Batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50 }
#    And request {query:'#(query)',variables:"#(variables)"}
#    When method post
#    Then status 200
#    Then match response.data.createProduct.message == 'Product - D002 already Exists. Please Change SKU and Try Again!'
#
#  Scenario: Create Product with valid data with Manager Access
#    # login as a manager
#    Given path '/'
#    Given def query = read('../accounts/login.graphql')
#    And def variables = {username:testuser, password:testuser}
#    And request {query:'#(query)',variables:"#(variables)"}
#    When method post
#    Then status 200
#
#    # create product with valid data
#    * def token = response.data.tokenAuth.token
#    * header Authorization = "JWT"+" "+token
#    Given def query = read('create_product.graphql')
#    And def variables = { sku: D003, name:dosa batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50 }
#    And request {query:'#(query)',variables:"#(variables)"}
#    When method post
#    Then status 200
#    Then match response.data.createProduct.product.name == 'dosa batter'
#
#  Scenario: Create Product with valid data with Admin Access
#    # login as a Admin
#    Given path '/'
#    Given def query = read('../accounts/login.graphql')
#    And def variables = {username:root, password:root}
#    And request {query:'#(query)',variables:"#(variables)"}
#    When method post
#    Then status 200
#
#    # Create Product with valid data
#    * def token = response.data.tokenAuth.token
#    * header Authorization = "JWT"+" "+token
#    Given def query = read('create_product.graphql')
#    And def variables = { sku: D004, name:Dosa Batter, basePrice:30.00, unit:PACKET, mrpPrice:35.00, sellingPrice:32.00, shelfLife:3, weight:50 }
#    And request {query:'#(query)',variables:"#(variables)"}
#    When method post
#    Then status 200
#    Then match response.data.createProduct.product.name == 'Dosa Batter'



