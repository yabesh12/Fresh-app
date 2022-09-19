

@debug
Feature: View All Products Test

  Background:
       * url 'http://localhost:8009/graphql/'
       * def token = ""

  Scenario: View all products without login
    Given path '/'
    Given def query = read('get_all_products.graphql')
    And request {query: '#(query)'}
    When method post
    Then status 200
    Then match response.errors[0].message == 'You do not have permission to perform this action'

  Scenario: View all products with login
    # login
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:defaultuser3, password:test}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Get all products
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('get_all_products.graphql')
    And request {query:'#(query)'}
    When method post
    Then status 200
    Then match response.data.allProducts[0].name == 'Dosa Batter'

