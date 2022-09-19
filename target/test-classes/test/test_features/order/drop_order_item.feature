@debug
Feature: Drop Order Item Test

  Background:
    * url 'http://localhost:8009/graphql/'
    * def token = ""

  Scenario: Drop Order without Login
    # Drop Order Item
    Given def query = read('drop_order_item.graphql')
    And def variables = { orderId:T3JkZXJOb2RlOjIx, orderItemIds:[1] }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'You do not have permission to perform this action'

  Scenario: Drop the Invalid Order
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
    Given def query = read('drop_order_item.graphql')
    And def variables = { orderId:T3JkZXJOb2RlOjM1, orderItemIds:[1] }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.dropOrderItem.order.billedTo.name == 'test shop'


#  Scenario: Update Order Item with valid Data
#    # Login as a Sales Executive
#    Given path '/'
#    Given def query = read('../accounts/login.graphql')
#    And def variables = {username:defaultuser3, password:test}
#    And request {query:'#(query)',variables:"#(variables)"}
#    When method post
#    Then status 200
#
#    # Update Order Item with valid data
#    * def token = response.data.tokenAuth.token
#    * header Authorization = "JWT"+" "+token
#    Given def query = read('update_order_item.graphql')
#    And def variables = { orderId:T3JkZXJOb2RlOjIx, orderItem:{productId:UmVhbFByb2R1Y3RUeXBlOjEx, quantity:3}, shopId:U2hvcFR5cGU6MQ== }
#    And request {query:'#(query)',variables:"#(variables)"}
#    When method post
#    Then status 200
#    Then match response.data.updateOrderItem.message == 'Order Item Updated Successfully!'