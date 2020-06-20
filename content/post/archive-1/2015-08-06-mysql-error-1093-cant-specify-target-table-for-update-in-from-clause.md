---
title: MySQL Error 1093 – Can't specify target table for update in FROM clause
author: wiloon
type: post
date: 2015-08-06T11:22:19+00:00
url: /?p=8067
categories:
  - Uncategorized

---
http://stackoverflow.com/questions/45494/mysql-error-1093-cant-specify-target-table-for-update-in-from-clause



wrap the condition in one more select



<pre class="lang-sql prettyprint prettyprinted"><code><span class="kwd">DELETE <span class="kwd">FROM<span class="pln"> story_category
<span class="kwd">WHERE<span class="pln"> category_id <span class="kwd">NOT <span class="kwd">IN <span class="pun">(
    <span class="kwd">SELECT<span class="pln"> cid <span class="kwd">FROM <span class="pun">(
        <span class="kwd">SELECT <span class="kwd">DISTINCT<span class="pln"> category<span class="pun">.<span class="pln">id <span class="kwd">AS<span class="pln"> cid <span class="kwd">FROM<span class="pln"> category 
        <span class="kwd">INNER <span class="kwd">JOIN<span class="pln"> story_category <span class="kwd">ON<span class="pln"> category_id<span class="pun">=<span class="pln">category<span class="pun">.<span class="pln">id
    <span class="pun">) <span class="kwd">AS<span class="pln"> c
<span class="pun">)```