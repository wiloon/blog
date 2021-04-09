+++
author = "w1100n"
date = "2021-03-16 16:47:40" 
title = "cypress"

+++
### install cypress for project
    npm install --save-dev cypress
    # 执行cypress install, 把cypress安装到 ~/.cache/Cypress
    node_modules/cypress/bin/cypress install

### install mysql
    npm install mysql  --save-dev

### 配置mysql连接信息, 修改 cypress.json 成这样.
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
    const mysql = require('mysql')
    function queryTestDb (query, config) {
      const connection = mysql.createConnection(config.env.db)
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
    cy.visit('/', { timeout: 3000 })
    cy.get('[data-cy=user-name]').type('user0')
    cy.get('[data-cy=login]').click()
    cy.get('[data-cy=list]').find('tbody>tr').first().contains('td', 'id0')
