---
title: MySQL Error 1093 – Can’t specify target table for update in FROM clause
author: wiloon
type: post
date: 2015-08-06T11:22:19+00:00
url: /?p=8067
categories:
  - Uncategorized

---
http://stackoverflow.com/questions/45494/mysql-error-1093-cant-specify-target-table-for-update-in-from-clause



wrap the condition in one more select



<pre class="lang-sql prettyprint prettyprinted"><code>&lt;span class="kwd">DELETE&lt;/span> &lt;span class="kwd">FROM&lt;/span>&lt;span class="pln"> story_category
&lt;/span>&lt;span class="kwd">WHERE&lt;/span>&lt;span class="pln"> category_id &lt;/span>&lt;span class="kwd">NOT&lt;/span> &lt;span class="kwd">IN&lt;/span> &lt;span class="pun">(&lt;/span>
    &lt;span class="kwd">SELECT&lt;/span>&lt;span class="pln"> cid &lt;/span>&lt;span class="kwd">FROM&lt;/span> &lt;span class="pun">(&lt;/span>
        &lt;span class="kwd">SELECT&lt;/span> &lt;span class="kwd">DISTINCT&lt;/span>&lt;span class="pln"> category&lt;/span>&lt;span class="pun">.&lt;/span>&lt;span class="pln">id &lt;/span>&lt;span class="kwd">AS&lt;/span>&lt;span class="pln"> cid &lt;/span>&lt;span class="kwd">FROM&lt;/span>&lt;span class="pln"> category 
        &lt;/span>&lt;span class="kwd">INNER&lt;/span> &lt;span class="kwd">JOIN&lt;/span>&lt;span class="pln"> story_category &lt;/span>&lt;span class="kwd">ON&lt;/span>&lt;span class="pln"> category_id&lt;/span>&lt;span class="pun">=&lt;/span>&lt;span class="pln">category&lt;/span>&lt;span class="pun">.&lt;/span>&lt;span class="pln">id
    &lt;/span>&lt;span class="pun">)&lt;/span> &lt;span class="kwd">AS&lt;/span>&lt;span class="pln"> c
&lt;/span>&lt;span class="pun">)&lt;/span>```