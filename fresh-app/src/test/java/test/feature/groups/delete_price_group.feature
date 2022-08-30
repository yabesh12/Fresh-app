@debug
Feature: Delete Price Group Test

  Background:
    * url 'http://localhost:8009/graphql/'
    * def token = ""


  Scenario: Delete Invalid Price Group with Admin Access
    Given path '/'
    Given def query = read('login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_price_group.graphql')
    And def variables = { priceGroupId:5 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Price Group!'

  Scenario: Delete Price Group with Admin Access
    Given path '/'
    Given def query = read('login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_price_group.graphql')
    And def variables = { priceGroupId:1 }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.deletePriceGroup.message == 'Successfully deleted the Price Group.'