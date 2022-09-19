@debug
Feature: Create and Update Price Group, Group Based Prices Test

  Background:
    * url 'http://localhost:8009/graphql/'
    * def token = ""

  Scenario: Create Price Group without Manager Access
    # Login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Create the Price Group
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_or_update_price_group.graphql')
    And def variables = { name:economy, groupBasedPrices:[{productSku:B001, sellingPrice:100}] }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Only MANAGER or ADMIN can Access!'

  Scenario: Create or Update Existing Price Group with Manager Access
    # Login as a manager or admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Create the Price Group
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_or_update_price_group.graphql')
    And def variables = { name:economy, groupBasedPrices:[{productSku:B001, sellingPrice:60.00, discountSellingPrice:12.00}] }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createUpdatePriceGroup.message == 'Added new Price Group successfully.'

  Scenario: Update Existing Price Group without Manager Access
    # Login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:newuser1, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Update the Price Group
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_or_update_price_group.graphql')
    And def variables = { name:economy, groupBasedPrices:[{productSku:B001, sellingPrice:60.00, discountSellingPrice:12.00}] }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == "Only MANAGER or ADMIN can Access!"

  Scenario: Create Group Based Prices with product's selling price lower than base price with Manager Access
    # Login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # When Product selling price is lower than base price
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_or_update_price_group.graphql')
    And def variables = { name:economy, groupBasedPrices:[{productSku:B001, sellingPrice:10.00, discountSellingPrice:12.00}] }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createUpdatePriceGroup.invalidSellingPrice == "product's selling price should not exceed MRP price and should not lower than base price for product B001"

  Scenario: Create Group Based Prices with product's selling price higher than base price with Manager Access
    # Login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:testuser, password:testuser}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # When Product selling price is higher than base price
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_or_update_price_group.graphql')
    And def variables = { name:economy, groupBasedPrices:[{productSku:B001, sellingPrice:1000.00, discountSellingPrice:12.00}] }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createUpdatePriceGroup.invalidSellingPrice == "product's selling price should not exceed MRP price and should not lower than base price for product B001"