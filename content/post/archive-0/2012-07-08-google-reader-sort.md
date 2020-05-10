---
title: google reader sort
author: wiloon
type: post
date: 2012-07-08T14:40:49+00:00
url: /?p=3821
categories:
  - Uncategorized

---
<http://stackoverflow.com/questions/4428117/google-reader-api-sortid-and-firstitemmsec>

When a user subscribes to a feed, the most recent 10 items in it (or items in the past 30 days, whichever results in fewer items) are considered unread for that user. The timestamp (in milliseconds since epoch) of the oldest item that should be considered unread is stored in firstotemmsec. When requesting unread items from a feed, Reader passes in max(now &#8211; 30 days, firstitemmsec) as the &#8220;ot&#8221; (oldest timestamp acceptable) parameter, so that the backend doesn&#8217;t look any further than that for older items.

sortid is used to maintain custom subscription/folder ordering. In the<a href="http://www.google.com/reader/api/0/preference/stream/list" rel="nofollow">http://www.google.com/reader/api/0/preference/stream/list</a> API response there is an &#8220;ordering&#8221; pref, which is composed of concatenated sortids of the items in that folder (items that are in that folder but don&#8217;t appear in the &#8220;ordering&#8221; list are appended to the end).

For example, I have a &#8220;tech&#8221; folder that has 3 subscriptions in it, MacRumors, Ars Technica, and Hacker News. It has an &#8220;ordering&#8221; pref of &#8220;B2E0248117996C269955C28D&#8221;. Sort IDs are 8 characters each, so this can be split to the sort IDs &#8220;B2E02481&#8221;, &#8220;17996C26&#8221;, and &#8220;9955C28D&#8221;. If you maintain a map from sort ID to subscription, you can look up those IDs in it to know what order to display them in.