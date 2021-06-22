---
title: maven dependency version range
author: "-"
type: post
date: 2017-02-08T08:30:48+00:00
url: /?p=9758
categories:
  - Uncategorized

---
http://maven.apache.org/components/enforcer/enforcer-rules/versionRanges.html

## 

## Version Range Specification

The [RequireMavenVersion][1] and [RequireJavaVersion][2] rules use the [standard Maven version range syntax][3]{.externalLink} with one minor change for ease of use (denoted with *):

<table class="table table-striped" border="1">
  <tr class="a">
    <td align="center">
      Range
    </td>
    
    <td align="left">
      Meaning
    </td>
  </tr>
  
  <tr class="b">
    <td align="center">
      1.0
    </td>
    
    <td align="left">
      x >= 1.0 * The default Maven meaning for 1.0 is everything (,) but with 1.0 recommended. Obviously this doesn't work for enforcing versions here, so it has been redefined as a minimum version.
    </td>
  </tr>
  
  <tr class="a">
    <td align="center">
      (,1.0]
    </td>
    
    <td align="left">
      x <= 1.0
    </td>
  </tr>
  
  <tr class="b">
    <td align="center">
      (,1.0)
    </td>
    
    <td align="left">
      x < 1.0
    </td>
  </tr>
  
  <tr class="a">
    <td align="center">
      [1.0]
    </td>
    
    <td align="left">
      x == 1.0
    </td>
  </tr>
  
  <tr class="b">
    <td align="center">
      [1.0,)
    </td>
    
    <td align="left">
      x >= 1.0
    </td>
  </tr>
  
  <tr class="a">
    <td align="center">
      (1.0,)
    </td>
    
    <td align="left">
      x > 1.0
    </td>
  </tr>
  
  <tr class="b">
    <td align="center">
      (1.0,2.0)
    </td>
    
    <td align="left">
      1.0 < x < 2.0
    </td>
  </tr>
  
  <tr class="a">
    <td align="center">
      [1.0,2.0]
    </td>
    
    <td align="left">
      1.0 <= x <= 2.0
    </td>
  </tr>
  
  <tr class="b">
    <td align="center">
      (,1.0],[1.2,)
    </td>
    
    <td align="left">
      x <= 1.0 or x >= 1.2. Multiple sets are comma-separated
    </td>
  </tr>
  
  <tr class="a">
    <td align="center">
      (,1.1),(1.1,)
    </td>
    
    <td align="left">
      x != 1.1
    </td>
  </tr>
</table>

 [1]: http://maven.apache.org/components/enforcer/enforcer-rules/requireMavenVersion.html
 [2]: http://maven.apache.org/components/enforcer/enforcer-rules/requireJavaVersion.html
 [3]: http://docs.codehaus.org/display/MAVEN/Dependency+Mediation+and+Conflict+Resolution#DependencyMediationandConflictResolution-DependencyVersionRanges