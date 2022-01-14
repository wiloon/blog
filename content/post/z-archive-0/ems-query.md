---
title: ems query
author: "-"
date: 2012-09-27T09:34:36+00:00
url: /?p=4345
categories:
  - Java

---
## ems query
public class EmsQuery {
  
static String separator = "#";
  
static String returnFlag = "n";

public static void main(String[] args) throws IOException, InterruptedException {
  
System.setProperty("http.proxyHost", "xxx.xxx.xxx.xxx");
  
System.setProperty("http.proxyPort", "80");
  
String filePath = "d:/100.txt";
  
File file = new File(filePath);
  
StringBuffer sb = new StringBuffer();
  
if (!file.exists()) {
  
file.createNewFile();
  
}
  
for (int id = 1082711; id < 1082911; id++) {
  
String emsId = "TX00" + id + "US";
  
String details = getEmsDetails(emsId);
  
sb.append(details);
  
Thread.sleep(1000);
  
}

BufferedWriter output = new BufferedWriter(new FileWriter(file));
  
output.write(sb.toString());
  
output.close();
  
}

public static String getEmsDetails(String emsId) {
  
String strUrl = "http://www.kuaidi100.com/query?type=ems&postid=" + emsId;
  
System.out.println(strUrl);
  
String content;
  
URL url = null;
  
String msg = null;
  
try {

url = new URL(strUrl);

HttpURLConnection conn = (HttpURLConnection) url.openConnection();

content = Utils.streamReader(conn.getInputStream(), "utf-8");
  
if (conn.getResponseCode() != 200) {
  
System.out.println("response > 200");
  
return "";
  
}
  
System.out.println(content);

JSONTokener jsonParser = new JSONTokener(content);
  
JSONObject obj = (JSONObject) jsonParser.nextValue();
  
String status = obj.getString("status");
  
if (!status.equals("200")) {
  
System.out.println("status!= 200");
  
return "";
  
}
  
JSONArray arr = obj.getJSONArray("data");
  
int size = arr.size();
  
StringBuffer sbRtn = new StringBuffer();
  
msg = emsId + separator + getEmsDetails(arr) + returnFlag;

} catch (Exception e) {
  
System.out.println(e);
  
msg = "";
  
}
  
return msg;
  
}

public static String getOneRecord(JSONArray arr, int index) {
  
JSONObject obj = arr.getJSONObject(index);
  
StringBuffer sbDt = new StringBuffer();
  
sbDt.append(obj.getString("time").trim());
  
String context = obj.getString("context");
  
if (context.indexOf(":") == 0) {
  
sbDt.append(context.substring(0, 3));
  
context = context.substring(4);
  
sbDt.insert(10, " ");
  
}
  
DateTime dateTime;
  
try {
  
dateTime = DateTimeFormat.forPattern("MM/dd/yyyy HH:mm").parseDateTime(sbDt.toString());
  
} catch (Exception e) {
  
dateTime = DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss").parseDateTime(sbDt.toString());
  
}

String strDt = dateTime.toString("yyyy-MM-dd HH:mm:ss");
  
return strDt + separator + context + separator;
  
}

public static String getEmsDetails(JSONArray arr) {
  
int size = arr.size();
  
StringBuffer sbRtn = new StringBuffer();
  
if (size > 2) {
  
sbRtn.append(getOneRecord(arr, size - 1));
  
sbRtn.append(getOneRecord(arr, size - 2));
  
sbRtn.append(getOneRecord(arr, 0));
  
} else if (size > 1) {
  
sbRtn.append(getOneRecord(arr, size - 1));
  
sbRtn.append(getOneRecord(arr, size - 2));
  
} else {
  
sbRtn.append(getOneRecord(arr, 0));
  
}
  
return sbRtn.toString();
  
}
  
}