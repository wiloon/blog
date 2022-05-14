---
author: "-"
date: "2021-03-16 16:47:40" 
title: "cypress"
categories:
  - inbox
tags:
  - reprint
---
## "cypress"
### install cypress for project
    npm install --save-dev cypress
    # 执行cypress install, 把cypress安装到 ~/.cache/Cypress
    node_modules/cypress/bin/cypress install

### install MySQL
    npm install MySQL  --save-dev

### 配置MySQL连接信息, 修改 cypress.json 成这样.
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

### 配置 tests/e2e/plugins/index.js
    const MySQL = require('MySQL')
    function queryTestDb (query, config) {
      const connection = MySQL.createConnection(config.env.db)
      connection.connect()
      return new Promise((resolve, reject) => {
        connection.query(query, (error, results) => {
          if (error) reject(error)
          else {
            connection.end()
            console.log(results)
            console.log('connected')
            return resolve(results)
          }
        })
      })
    }

    module.exports = (on, config) => {
      on('task', {
        log (message) {
          console.log(message)

          return null
        }
      })
      on('task', {
        queryDb: query => {
          return queryTestDb(query, config)
        }
      })
      return Object.assign({}, config, {
        fixturesFolder: 'tests/e2e/fixtures',
        integrationFolder: 'tests/e2e/specs',
        screenshotsFolder: 'tests/e2e/screenshots',
        videosFolder: 'tests/e2e/videos',
        supportFile: 'tests/e2e/support/index.js'
      })
    }

### command
#### timeout
    cy.visit('/', { timeout: 3000 })
#### type
    cy.get('[data-cy=user-name]').type('user0')
#### click
    cy.get('[data-cy=login]').click()
#### contains
    cy.get('[data-cy=list]').find('tbody>tr').first().contains('td', 'id0')
#### clear
    cy.get('[data-cy=plate]').clear()

#### 页面元素数量, 3个 text0 文字
    cy.contains('span', 'text0').should('have.length', 3)

#### 比较文本
    cy.get('[data-cy=foo]').should('have.text',"0")
    cy.get('[data-cy=foo]').should('not.have.text',"0")
### sql
    cy.task('queryDb', 'DELETE FROM `table0`').then(res => { cy.log(res) })
#### count
    cy.task('queryDb', 'SELECT COUNT(*) AS count FROM table0 WHERE field0=\'value0\'').then(res => {
      expect(res[0].count).to.equal(1)
    })

### 配置 NODE_ENV
```javascript
  "scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "test:unit": "vue-cli-service test:unit",
    "test:e2e": "NODE_ENV=development vue-cli-service test:e2e",
    "lint": "vue-cli-service lint"
  },

```