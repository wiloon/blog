---
title: 限定WordPress搜索范围
author: wiloon
type: post
date: 2012-02-25T02:53:09+00:00
url: /?p=2393
categories:
  - Wordpress

---
打开主题的 _functions.php_文件并粘贴下面的代码：

function SearchFilter($query) {
if ($query->is_search) {
$query->set('post_type', 'post');
}
return $query;
}

add_filter('pre_get_posts','SearchFilter');

通过设置 post_type来限定搜索范围为"Post".