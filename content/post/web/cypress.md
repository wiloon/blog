+++
author = "w1100n"
date = "2021-03-16 16:47:40" 
title = "cypress"

+++

### cypress.json
```json
{
  "pluginsFile": "tests/e2e/plugins/index.js",
  "env": {
    "db": {
      "host": "192.168.1.xxx",
      "user": "user0",
      "password": "password0",
      "database": "database0"
    }
  }
}
```

### command
    cy.visit('/', { timeout: 3000 })
    cy.get('[data-cy=user-name]').type('user0')
    cy.get('[data-cy=login]').click()
    cy.get('[data-cy=list]').find('tbody>tr').first().contains('td', 'id0')
