@debug
Feature: Apply Wallet Amount Test

  Background:
    * url 'http://localhost:8009/graphql/'
    * def token = ""

  Scenario: Apply Wallet Amount without Login
    # Apply Wallet Amount
    Given def query = read('apply_wallet_amount.graphql')
    And def variables = { orderId:T3JkZXJOb2RlOjI4, shopId:U2hvcFR5cGU6MQ==, amount:10.00 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'You do not have permission to perform this action'

  Scenario: Apply Wallet Amount for Invalid order ID
    # Login as a Sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Apply Wallet Amount with valid data
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('apply_wallet_amount.graphql')
    And def variables = { orderId:T3JkZXJOb2RlOjI4, shopId:U2hvcFR5cGU6MQ==, amount:10.00 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.applyWalletAmount.message == 'Wallet Amount Applied Successfully!'



