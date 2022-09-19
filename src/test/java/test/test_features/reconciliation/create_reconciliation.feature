@debug
Feature: Create Product Test

Background:
     * url 'http://localhost:8009/graphql/'
     * def token = ""

  Scenario: Create Reconciliation without Login
    Given path '/'
    Given def query = read('create_reconciliation.graphql')
    And def variables = { productSku: D001, quantity:1, reconciliationProductType:CREDIT, reconciliationType:CREDIT, shopId:3 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'You do not have permission to perform this action'

  Scenario: Create Reconciliation without Sales Executive Access
    # login
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:deepsense, password:deepsense}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create reconciliation request
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_reconciliation.graphql')
     And def variables = { productSku: D001, quantity:1, reconciliationProductType:CREDIT, reconciliationType:CREDIT, shopId:3 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid SalesExecutive!'

  Scenario: Create Reconciliation with Invalid shop
    # login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create reconciliation with invalid shop
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_reconciliation.graphql')
     And def variables = { productSku: D001, quantity:1, reconciliationProductType:CREDIT, reconciliationType:CREDIT, shopId:30 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Shop!'


  Scenario: Create Reconciliation with Invalid product
    # Login as a sales executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # create reconciliation request with invalid product
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('create_reconciliation.graphql')
     And def variables = { productSku: D8881, quantity:1, reconciliationProductType:CREDIT, reconciliationType:CREDIT, shopId:1 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Product!'

  Scenario: Create Reconciliation with valid data when reconciliation type is CREDIT
    # Login as a Sales Executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token

    # Create Reconciliation request when reconciliation type is CREDIT
    Given def query = read('create_reconciliation.graphql')
    And def variables = { productSku: D001, quantity:1, reconciliationProductType:USABLE, reconciliationType:CREDIT, shopId:1 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createReconciliation.reconciliation.reconciliationType == 'CREDIT'

  Scenario: Create Reconciliation with valid data when reconciliation type is REFUND
    # Login as a Sales Executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token

    # Create Reconciliation request when reconciliation type is REFUND
    Given def query = read('create_reconciliation.graphql')
    And def variables = { productSku: D002, quantity:1, reconciliationProductType:USABLE, reconciliationType:REFUND, shopId:1 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createReconciliation.reconciliation.reconciliationType == 'REFUND'

  Scenario: Create Reconciliation with valid data when reconciliation product type is USABLE
    # Login as a Sales Executive
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token

    # Create Reconciliation request when reconciliation product type is USABLE
    Given def query = read('create_reconciliation.graphql')
    And def variables = { productSku: D002, quantity:1, reconciliationProductType:USABLE, reconciliationType:REFUND, shopId:1 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.createReconciliation.reconciliation.shop.name == 'test shop'

