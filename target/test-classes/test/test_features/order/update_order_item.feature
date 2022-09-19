@debug
Feature: Update Order Item Test

  Background:
    * url 'http://localhost:8009/graphql/'
    * def token = ""

  Scenario: Update Order Item without Login
    # Update Order Item
    Given def query = read('update_order_item.graphql')
    And def variables = { orderId:T3JkZXJOb2RlOjIx, orderItem:{productId:UmVhbFByb2R1Y3RUeXBlOjEx, quantity:2}, shopId:U2hvcFR5cGU6MQ== }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'You do not have permission to perform this action'

  Scenario: Update Order Item with Invalid Order ID
    # Login as a Sales Executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Update Order Item with Invalid Order Id
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_order_item.graphql')
    And def variables = { orderId:T3JkZXJOb2RlOjIx, orderItem:{productId:T3JkZXJOb2RlOjIx, quantity:2}, shopId:U2hvcFR5cGU6MQ== }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.updateOrderItem.message == 'Product Does Not Exist'


  Scenario: Update Order Item with valid Data
    # Login as a Sales Executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Update Order Item with valid data
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('update_order_item.graphql')
    And def variables = { orderId:T3JkZXJOb2RlOjIx, orderItem:{productId:UmVhbFByb2R1Y3RUeXBlOjEx, quantity:3}, shopId:U2hvcFR5cGU6MQ== }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.updateOrderItem.message == 'Order Item Updated Successfully!'