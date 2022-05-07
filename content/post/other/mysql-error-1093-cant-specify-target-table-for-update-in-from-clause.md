---
title: MySQL Error 1093 – Can't specify target table for update in FROM clause
author: "-"
date: 2015-08-06T11:22:19+00:00
url: /?p=8067
categories:
  - Inbox
tags:
  - reprint
---
## MySQL Error 1093 – Can't specify target table for update in FROM clause
http://stackoverflow.com/questions/45494/MySQL-error-1093-cant-specify-target-table-for-update-in-from-clause


wrap the condition in one more select


DELETE FROM story_category
WHERE category_id NOT IN (
    SELECT cid FROM (
        SELECT DISTINCT category.id AS cid FROM category 
        INNER JOIN story_category ON category_id=category.id
    ) AS c
)```