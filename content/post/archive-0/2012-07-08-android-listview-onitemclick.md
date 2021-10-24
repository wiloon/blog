---
title: android listview onitemclick
author: "-"
type: post
date: 2012-07-08T14:49:54+00:00
url: /?p=3823
categories:
  - Uncategorized

---
## android listview onitemclick
> public class ListHymnsCategories extends Activity {
> 
> private ListView listCats;
  
> private String catsName[]={"敬拜‧讚美","祈禱‧感恩","教導‧生活","見証‧委身", "團契‧佈道"};
> 
> @Override
  
> public void onCreate(Bundle savedInstanceState) {
  
> super.onCreate(savedInstanceState);
  
> setContentView(R.layout.main);
> 
> listCats=(ListView)findViewById(R.id.HymnsCatsListView);
  
> listCats.setAdapter(new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1 , catsName));
  
> listCats.setTextFilterEnabled(true);
  
> listCats.setOnItemClickListener(new OnItemClickListener() {
  
> public void onItemClick(AdapterView<?> a, View v, int position, long id) {
  
> //做你想做的
  
> }
  
> });
> 
> }//public void onCreate
> 
> }