Feature: Account registry

Scenario: User is able to create 2 accounts
  Given Account registry is empty
  When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
  And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
  Then Number of accounts in registry equals: "2"
  And Account with pesel "89092909246" exists in registry
  And Account with pesel "79101011234" exists in registry

Scenario: User is able to update surname of already created account
  Given Account registry is empty
  And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
  When I update "surname" of account with pesel: "95092909876" to "filatov"
  Then Account with pesel "95092909876" has "surname" equal to "filatov"

Scenario: User is able to update name of already created account
  Given Account registry is empty
  And I create an account using name: "adam", last name: "kowalski", pesel: "90010112345"
  When I update "name" of account with pesel: "90010112345" to "jan"
  Then Account with pesel "90010112345" has "name" equal to "jan"

Scenario: Created account has all fields correctly set
  Given Account registry is empty
  When I create an account using name: "ola", last name: "nowak", pesel: "99020222222"
  Then Account with pesel "99020222222" has "name" equal to "ola"
  And Account with pesel "99020222222" has "surname" equal to "nowak"

Scenario: User is able to delete created account
  Given Account registry is empty
  And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
  When I delete account with pesel: "01092909876"
  Then Account with pesel "01092909876" does not exist in registry
  And Number of accounts in registry equals: "0"

Scenario: User is able to perform an incoming transfer
  Given Account registry is empty
  And I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"
  When I perform an "incoming" transfer of "100" to account with pesel: "12345678901"
  Then Account with pesel "12345678901" has "balance" equal to "100"

Scenario: User is able to perform an outgoing transfer
  Given Account registry is empty
  And I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"
  And I perform an "incoming" transfer of "100" to account with pesel: "12345678901"
  When I perform an "outgoing" transfer of "40" to account with pesel: "12345678901"
  Then Account with pesel "12345678901" has "balance" equal to "60"

Scenario: User is able to perform an express transfer with fee
  Given Account registry is empty
  And I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"
  And I perform an "incoming" transfer of "100" to account with pesel: "12345678901"
  When I perform an "express" transfer of "50" to account with pesel: "12345678901"
  Then Account with pesel "12345678901" has "balance" equal to "49"