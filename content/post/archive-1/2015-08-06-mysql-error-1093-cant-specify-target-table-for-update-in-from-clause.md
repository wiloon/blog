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



<pre class="lang-sql prettyprint prettyprinted"><code><span class="kwd">DELETE</span> <span class="kwd">FROM</span><span class="pln"> story_category
</span><span class="kwd">WHERE</span><span class="pln"> category_id </span><span class="kwd">NOT</span> <span class="kwd">IN</span> <span class="pun">(</span>
    <span class="kwd">SELECT</span><span class="pln"> cid </span><span class="kwd">FROM</span> <span class="pun">(</span>
        <span class="kwd">SELECT</span> <span class="kwd">DISTINCT</span><span class="pln"> category</span><span class="pun">.</span><span class="pln">id </span><span class="kwd">AS</span><span class="pln"> cid </span><span class="kwd">FROM</span><span class="pln"> category 
        </span><span class="kwd">INNER</span> <span class="kwd">JOIN</span><span class="pln"> story_category </span><span class="kwd">ON</span><span class="pln"> category_id</span><span class="pun">=</span><span class="pln">category</span><span class="pun">.</span><span class="pln">id
    </span><span class="pun">)</span> <span class="kwd">AS</span><span class="pln"> c
</span><span class="pun">)</span>```