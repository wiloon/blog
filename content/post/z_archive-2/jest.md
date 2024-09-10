---
title: jest
author: "-"
date: 2018-02-07T05:23:31+00:00
url: jest
categories:
  - Javascript
tags:
  - reprint
  - remix
---
## jest

https://stackoverflow.com/questions/68956636/how-to-use-esm-tests-with-jest

## package.json

use es module

```json
{
  "type": "module",
  "devDependencies": {
    "jest": "^29.7.0"
  },
  "scripts": {
    "test": "node --experimental-vm-modules ./node_modules/.bin/jest"
  }
}

```

```Bash
# run all test
npm run test

# run one test
npm run test -- infoq.test.js
```