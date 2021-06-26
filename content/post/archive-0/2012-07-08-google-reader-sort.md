---
title: google reader sort
author: "-"
type: post
date: 2012-07-08T14:40:49+00:00
url: /?p=3821
categories:
  - Uncategorized

---
<http://stackoverflow.com/questions/4428117/google-reader-api-sortid-and-firstitemmsec>

When a user subscribes to a feed, the most recent 10 items in it (or items in the past 30 days, whichever results in fewer items) are considered unread for that user. The timestamp (in milliseconds since epoch) of the oldest item that should be considered unread is stored in firstotemmsec. When requesting unread items from a feed, Reader passes in max(now - 30 days, firstitemmsec) as the "ot" (oldest timestamp acceptable) parameter, so that the backend doesn't look any further than that for older items.

sortid is used to maintain custom subscription/folder ordering. In the<a href="http://www.google.com/reader/api/0/preference/stream/list" rel="nofollow">http://www.google.com/reader/api/0/preference/stream/list</a> API response there is an "ordering" pref, which is composed of concatenated sortids of the items in that folder (items that are in that folder but don't appear in the "ordering" list are appended to the end).

For example, I have a "tech" folder that has 3 subscriptions in it, MacRumors, Ars Technica, and Hacker News. It has an "ordering" pref of "B2E0248117996C269955C28D". Sort IDs are 8 characters each, so this can be split to the sort IDs "B2E02481", "17996C26", and "9955C28D". If you maintain a map from sort ID to subscription, you can look up those IDs in it to know what order to display them in.