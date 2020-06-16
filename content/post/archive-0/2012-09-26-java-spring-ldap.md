---
title: Java Spring LDAP
author: lcf
type: post
date: 2012-09-26T06:59:29+00:00
url: /?p=4312
categories:
  - Java

---
[java]
  
import java.util.HashMap;
  
import java.util.Hashtable;
  
import java.util.List;
  
import java.util.Map;

import javax.naming.Context;
  
import javax.naming.directory.DirContext;
  
import javax.naming.directory.InitialDirContext;

import org.springframework.ldap.core.DirContextOperations;
  
import org.springframework.ldap.core.DistinguishedName;
  
import org.springframework.ldap.core.LdapTemplate;
  
import org.springframework.ldap.core.support.AbstractContextMapper;
  
import org.springframework.ldap.core.support.DirContextSource;
  
import org.springframework.ldap.support.LdapUtils;
  
/**
   
* This Service does user authentication with LDAP. It uses Spring to do the authentication
   
*
   
* A good chunk of the LDAP code is copy-paste from:
   
* http://static.springsource.organization/spring-ldap/docs/1.3.x/reference/pdf/spring-ldap-reference.pdf
   
*
   
*/
  
public class LDAPService {

private Map<String, String> ldapPropertiesMap=new HashMap<String, String>();

// LDAP Settings
   
public static final String LDAP\_PROVIDER\_URL = "ldap.provider.url";
   
public static final String LDAP\_SECURITY\_AUTHENTICATION = "ldap.security.authentication";
   
public static final String LDAP\_SECURITY\_PRINCIPAL = "ldap.security.principal";
   
public static final String LDAP\_SECURITY\_CREDENTIALS = "ldap.security.credentials";
   
public static final String LDAP\_ADMIN\_OU = "ldap.admin.ou";
   
public static final String LDAP\_USER\_OU = "ldap.user.ou";
   
public static final String LDAP\_USER\_FILTER = "ldap.user.filter";

private DirContextSource dirCtxSrc;
   
private String userAuthority;
   
private static final String ldapFactory = "com.sun.jndi.ldap.LdapCtxFactory";

private static final String DEFAULT\_USER\_FILTER = "uid";

public LDAPService() throws Exception {
   
ldapPropertiesMap.put(LDAP\_PROVIDER\_URL, "ldap://10.0.1.1:10389/ou=system");
   
ldapPropertiesMap.put(LDAP\_SECURITY\_AUTHENTICATION, "simple");
   
ldapPropertiesMap.put(LDAP\_SECURITY\_PRINCIPAL, "uid=admin,ou=system");
   
ldapPropertiesMap.put(LDAP\_SECURITY\_CREDENTIALS, "secret");
   
ldapPropertiesMap.put(LDAP\_ADMIN\_OU, "ou=admins,ou=system");
   
ldapPropertiesMap.put(LDAP\_USER\_OU, "ou=users,ou=system");
   
ldapPropertiesMap.put(LDAP\_USER\_FILTER, "uid=?");
   
this.init();
   
}

private void init() throws Exception {
   
Hashtable<String, String> env = new Hashtable<String, String>();

env.put(Context.INITIAL\_CONTEXT\_FACTORY, ldapFactory);
   
env.put(Context.PROVIDER\_URL, ldapPropertiesMap.get(LDAP\_PROVIDER_URL));
   
env.put(Context.SECURITY_AUTHENTICATION,
   
ldapPropertiesMap.get(LDAP\_SECURITY\_AUTHENTICATION));
   
env.put(Context.SECURITY_PRINCIPAL,
   
ldapPropertiesMap.get(LDAP\_SECURITY\_PRINCIPAL));
   
env.put(Context.SECURITY_CREDENTIALS,
   
ldapPropertiesMap.get(LDAP\_SECURITY\_CREDENTIALS));

dirCtxSrc = new DirContextSource();
   
dirCtxSrc.setBaseEnvironmentProperties(env);
   
dirCtxSrc.setUserDn(ldapPropertiesMap.get(LDAP\_SECURITY\_PRINCIPAL));
   
dirCtxSrc.setPassword(ldapPropertiesMap.get(LDAP\_SECURITY\_CREDENTIALS));
   
dirCtxSrc.setUrl(ldapPropertiesMap.get(LDAP\_PROVIDER\_URL));
   
dirCtxSrc.afterPropertiesSet();
   
}

/**
   
* Return user authority after authentication
   
*
   
* @return
   
*/
   
public String getUserAuthority() {
   
return userAuthority;
   
}

public boolean validateLoginCredentials(String username, String password)
   
throws Exception {
   
boolean result = false;

try {
   
String userDn = getDnForUser(username);
   
result = authenticate(userDn, password);

if (result) {
   
String adminGroup = ldapPropertiesMap.get(LDAP\_ADMIN\_OU);
   
String userGroup = ldapPropertiesMap.get(LDAP\_USER\_OU);
   
if (adminGroup != null
   
&& userDn.toLowerCase().endsWith(
   
adminGroup.toLowerCase())) {
   
this.userAuthority = adminGroup;
   
} else if (userGroup != null
   
&& userDn.toLowerCase().endsWith(
   
userGroup.toLowerCase())) {
   
this.userAuthority = userGroup;
   
} else {
   
logger.info(username
   
+ " is a valid user, but is not in the either the UserOU or AdminOU");
   
throw new RuntimeException(
   
"Could not locate Authority for User: &#8216;" + username
   
+ "&#8217; in LDAP");
   
}
   
}
   
return result;
   
} catch (Exception ex) {
   
logger.error("Exception during ldap authentication for User: &#8216;"
   
+ username + "&#8217;", ex);
   
throw ex;
   
}
   
}

/**
   
* This will find the distinguished name given a uid
   
*
   
* @param uid
   
* @return
   
*/
   
protected String getDnForUser(String uid) {
   
LdapTemplate ldapTemplate = new LdapTemplate(dirCtxSrc);

// Filter
   
String userFilter = ldapPropertiesMap.get(LDAP\_USER\_FILTER);
   
if (userFilter != null && !userFilter.isEmpty()) {
   
userFilter = userFilter.replaceAll("\?", uid);
   
} else {
   
userFilter = "(" + DEFAULT\_USER\_FILTER + "=" + uid + ")";
   
}
   
Logger.debug("LDAP USER Filter:" + userFilter);

// Filter f = new EqualsFilter("uid", uid);
   
List result = ldapTemplate.search(DistinguishedName.EMPTY_PATH,
   
userFilter, new AbstractContextMapper() {
   
protected Object doMapFromContext(DirContextOperations ctx) {
   
return ctx.getNameInNamespace();
   
}
   
});

if (result.size() != 1) {
   
throw new RuntimeException("User-&#8216;" + uid
   
+ "&#8217; not found in LDAP or not unique");
   
}
   
return (String) result.get(0);
   
}

/**
   
* This try to create a Context using the supplied username and password
   
*
   
* @param userDn
   
* @param password
   
* @return
   
*/
   
protected boolean authenticate(String userDn, String password)
   
throws Exception {
   
DirContext ctx = null;

Hashtable<String, String> env = new Hashtable<String, String>();

String providerUrl = (ldapPropertiesMap.get(LDAP\_PROVIDER\_URL));
   
String securityAuth = (ldapPropertiesMap
   
.get(LDAP\_SECURITY\_AUTHENTICATION));

env.put(Context.INITIAL\_CONTEXT\_FACTORY,
   
"com.sun.jndi.ldap.LdapCtxFactory");
   
env.put(Context.PROVIDER_URL, providerUrl);
   
env.put(Context.SECURITY_AUTHENTICATION, securityAuth);
   
env.put(Context.SECURITY_PRINCIPAL, userDn);
   
env.put(Context.SECURITY_CREDENTIALS, password);

try {
   
ctx = new InitialDirContext(env);
   
return true;
   
} catch (Exception e) {
   
// Context creation failed - authentication did not succeed
   
logger.error("Login failed for userDn-&#8216;" + userDn + "&#8217;",
   
e);
   
throw e;
   
} finally {
   
// It is imperative that the created DirContext instance is always
   
// closed
   
LdapUtils.closeContext(ctx);
   
}
   
}

public Map<String, String> getLdapPropertiesMap() {
   
return ldapPropertiesMap;
   
}

public void setLdapPropertiesMap(Map<String, String> ldapPropertiesMap) {
   
this.ldapPropertiesMap = ldapPropertiesMap;
   
}
  
}



[/java]