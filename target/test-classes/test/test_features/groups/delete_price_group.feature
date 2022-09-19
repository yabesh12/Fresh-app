@debug
Feature: Delete Price Group Test

  Background:
    * url 'http://localhost:8009/graphql/'
    * def token = ""


  Scenario: Delete Invalid Price Group with Admin Access
    # Login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the Invalid Price Group
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_price_group.graphql')
    And def variables = { priceGroupId:UHJpY2VHcm91cFR5cGU6MTY= }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.errors[0].message == 'Invalid Price Group!'

  Scenario: Delete Price Group with Admin Access
    # Login as a Admin
    Given path '/'
    Given def query = read('../accounts/login.graphql')
    And def variables = {username:root, password:root}
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200

    # Delete the valid Price Group
    * def token = response.data.tokenAuth.token
    * header Authorization = "JWT"+" "+token
    Given def query = read('delete_price_group.graphql')
    And def variables = { priceGroupId:UHJpY2VHcm91cFR5cGU6NA== }
    And request {query:'#(query)',variables:"#(variables)"}
    When method post
    Then status 200
    Then match response.data.deletePriceGroup.message == 'Successfully deleted the Price Group.'