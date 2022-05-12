---
title: Java HTTP Helper
author: lcf
date: 2012-09-26T07:20:19+00:00
url: /?p=4321
categories:
  - Java
tags:$
  - reprint
---
## Java HTTP Helper
```java

import javax.net.ssl.SSLContext;
  
import javax.net.ssl.TrustManager;
  
import javax.net.ssl.X509TrustManager;

import org.apache.http.HttpEntity;
  
import org.apache.http.HttpHost;
  
import org.apache.http.HttpRequest;
  
import org.apache.http.HttpResponse;
  
import org.apache.http.StatusLine;
  
import org.apache.http.auth.AuthScope;
  
import org.apache.http.auth.UsernamePasswordCredentials;
  
import org.apache.http.client.AuthCache;
  
import org.apache.http.client.methods.HttpGet;
  
import org.apache.http.client.methods.HttpPost;
  
import org.apache.http.client.protocol.ClientContext;
  
import org.apache.http.conn.ClientConnectionManager;
  
import org.apache.http.conn.params.ConnRoutePNames;
  
import org.apache.http.conn.scheme.Scheme;
  
import org.apache.http.conn.scheme.SchemeRegistry;
  
import org.apache.http.conn.ssl.SSLSocketFactory;
  
import org.apache.http.entity.BasicHttpEntity;
  
import org.apache.http.entity.StringEntity;
  
import org.apache.http.impl.auth.BasicScheme;
  
import org.apache.http.impl.client.BasicAuthCache;
  
import org.apache.http.impl.client.DefaultHttpClient;
  
import org.apache.http.impl.conn.tsccm.ThreadSafeClientConnManager;
  
import org.apache.http.protocol.BasicHttpContext;
  
import org.apache.http.util.EntityUtils;
  
public class HttpHelper {

/*\* The Constant MAX_NUMBER_OF_CONNECTIONS. */
   
private static final int MAX_NUMBER_OF_CONNECTIONS = 200;

/*\* The http client. */
   
private DefaultHttpClient httpClient;

/*\* The http context. */
   
private BasicHttpContext httpContext;

/*\* The target host. */
   
private HttpHost targetHost;

/*\* The proxy host. */
   
private HttpHost proxyHost;
   
/*\* The X509TrustManager. */
   
protected static X509TrustManager tm = new X509TrustManager() {
   
public void checkClientTrusted(X509Certificate[] xcs, String string)
   
throws CertificateException {
   
}

public void checkServerTrusted(X509Certificate[] xcs, String string)
   
throws CertificateException {
   
}

public X509Certificate[] getAcceptedIssuers() {
   
return null;
   
}
   
};

protected String execute(HttpRequest request) throws Exception {
  
// logger.debug("executing request: " + request.getRequestLine());
  
// logger.debug("via proxy: " + getProxyHost());
  
// logger.debug("to target: " + getTargetHost());
   
StringBuffer resXML = new StringBuffer();

// Send request
   
DefaultHttpClient httpClient = getHttpClient();
   
HttpResponse response = httpClient.execute(getTargetHost(),
   
request, getHttpContext());

// Get response
   
HttpEntity entity = response.getEntity();
   
StatusLine statusLine = response.getStatusLine();
  
// logger.debug("Response code: " + statusLine);
   
int httpStatus = statusLine.getStatusCode();
   
if (httpStatus >= 200 && httpStatus <= 207) {

// Get response XML
   
InputStream is = entity.getContent();
   
BufferedReader br = new BufferedReader(new InputStreamReader(is));
   
String line = null;
   
while ((line = br.readLine()) != null) {
   
resXML.append(line);
   
}
   
EntityUtils.consume(entity);

} else {
   
// Http access error
   
throw new Exception(statusLine.toString());
   
}

return resXML.toString();
   
}

/**
   
* Gets the target host.
   
*
   
* @return the target host
   
*/
   
protected HttpHost getTargetHost() {
   
if (targetHost == null) {
   
targetHost = new HttpHost(getTargetHost(), getTargetPort(),
   
getProtocol());
   
}
   
return targetHost;
   
}

/**
   
* Gets the proxy host.
   
*
   
* @return the proxy host
   
*/
   
protected HttpHost getProxyHost() {
   
if (proxyHost == null) {
   
proxyHost = new HttpHost(getProxyHost(),
   
getProxyPort());
   
}
   
return proxyHost;
   
}

/**
   
* Gets the http context.
   
*
   
* @return the http context
   
*/
   
@SuppressWarnings("static-access")
   
protected BasicHttpContext getHttpContext() {
   
if (httpContext == null) {

// Create AuthCache instance
   
AuthCache authCache = new BasicAuthCache();

// Generate BASIC scheme object and add it to the local
   
BasicScheme basicAuth = new BasicScheme();
   
basicAuth.authenticate(
   
new UsernamePasswordCredentials(getUserName(),
   
getPassword()), "UTF-8", true);
   
authCache.put(getTargetHost(), basicAuth);

// Add AuthCache to the execution context
   
httpContext = new BasicHttpContext();
   
httpContext.setAttribute(ClientContext.AUTH_CACHE, authCache);
   
}
   
return httpContext;
   
}

/**
   
* Gets the http client.
   
*
   
* @return the http client
   
* @throws NoSuchAlgorithmException the no such algorithm exception
   
* @throws KeyManagementException the key management exception
   
*/
   
@SuppressWarnings("deprecation")
   
protected DefaultHttpClient getHttpClient() throws NoSuchAlgorithmException,
   
KeyManagementException {

if (httpClient == null) {
   
ThreadSafeClientConnManager cm =new ThreadSafeClientConnManager();
   
cm.setMaxTotal(MAX_NUMBER_OF_CONNECTIONS);
   
httpClient = new DefaultHttpClient(cm);
   
if (isProxyEnabled()) {
   
httpClient.getParams().setParameter(
   
ConnRoutePNames.DEFAULT_PROXY, getProxyHost());
   
}

String protocol = getProtocol();
   
if ("HTTPS".equalsIgnoreCase(protocol)) {
   
SSLContext ctx = SSLContext.getInstance("TLS");
   
ctx.init(null, new TrustManager[] { tm }, null);
   
SSLSocketFactory ssf = new SSLSocketFactory(ctx,
   
SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER);
   
ClientConnectionManager ccm = httpClient.getConnectionManager();
   
SchemeRegistry sr = ccm.getSchemeRegistry();
   
sr.register(new Scheme(protocol, ssf, getTargetPort()));
   
httpClient = new DefaultHttpClient(ccm, httpClient.getParams());
   
}
   
httpClient.getCredentialsProvider().setCredentials(
   
AuthScope.ANY,
   
new UsernamePasswordCredentials(getUserName(),
   
getPassword()));
   
}

return httpClient;
   
}

/**
   
* Shuts down this httpClient connection manager and releases allocated resources.
   
* This includes closing all connections, whether they are currently
   
* used or not.
   
*/
   
public void shutdown(){
   
if (httpClient == null) {
   
httpClient.getConnectionManager().shutdown();
   
}
   
}

}

```