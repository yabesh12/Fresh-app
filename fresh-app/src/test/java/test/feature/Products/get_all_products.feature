

@debug
Feature: View All Products Test

  Background:
    * url 'http://localhost:8009/graphql/'
    * call read('login.feature') { token: '#(token)' }

  Scenario: View all products without login
    Given path '/'
    Given def query = read('get_all_products.graphql')
    And request {query: '#(query)'}
    When method post
    Then status 200
    Then match response.errors[0].message == 'You do not have permission to perform this action'

  Scenario: View all products with login
      Given path '/'
      * header Authorization = "JWT"+" "+token
      Then print token
      Given def query = read('get_all_products.graphql')
      And request {query:'#(query)'}
      When method post
      Then status 200
      Then match response.data.allProducts[1].name == 'Batter'

