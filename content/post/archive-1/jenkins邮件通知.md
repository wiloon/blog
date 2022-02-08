---
title: Jenkins邮件通知
author: "-"
date: 2013-09-04T11:37:36+00:00
url: /?p=5792
categories:
  - CI

tags:
  - reprint
---
## Jenkins邮件通知
#### 可用令牌

  * **${BUILD_LOG, _maxLines_, _escapeHtml_} -**显示最终构建日志。 
      * _maxLines_ – 显示该日志最多显示的行数，默认250行。
      * _escapeHtml_ -如果为true，格式化HTML。默认false。
  * **${BUILD_LOG_REGEX, _regex_, _linesBefore_, _linesAfter_, _maxMatches_,_showTruncatedLines_, _substText_, _escapeHtml_, _matchedLineHtmlStyle_} -**按正则表达式匹配显示构建日志的行数。 
      * _匹配符合该正则表达式的行数。参阅__java.util.regex.Pattern__，默认_"(?i)b(error|exception|fatal|fail(ed|ure)|un(defined|resolved))b"。
      * _linesBefore_ -包含在匹配行之前的行编号。行数会与当前的另一个行匹配或者_linesAfter__重叠，默认____。_
      * _linesAfter_ -包含在匹配行之后的行编号。行数会与当前的另一个行匹配或者_linesBefore__重叠，默认____。_
      * _maxMatches_ -匹配的最大数量，如果为0，则包含所有匹配。默认为0。
      * _showTruncatedLines_ -如果为true，包含[...truncated ### lines...]行。默认为true。
      * _substText_ -如果非空，把这部分文字插入该邮件，而不是整行。默认为空。
      * _escapeHtml_ -如果为true，格式化HTML。默认false。
      * _matchedLineHtmlStyle_ -如果非空，输出HTML。匹配的行数将变为 html escaped matched line 格式。默认为空。
  * **${BUILD_NUMBER} -**显示当前构建的编号。
  * **${BUILD_STATUS} -**显示当前构建的状态(失败、成功等等)
  * **${BUILD_URL} -**显示当前构建的URL地址。
  * **${CHANGES, _showPaths_, _format_, _pathFormat_} -**显示上一次构建之后的变化。 
      * _showPaths_ – 如果为 true,显示提交修改后的地址。默认false。
      * _format_ – 遍历提交信息，一个包含%X的字符串，其中%a表示作者，%d表示日期，%m表示消息，%p表示路径，%r表示版本。注意，并不是所有的版本系统都支持%d和%r。如果指定_showPaths_将被忽略_。默认_"[%a] %mn"。
      * _pathFormat_ -一个包含"%p"的字符串，用来标示怎么打印字符串。
  * **${CHANGES_SINCE_LAST_SUCCESS, _reverse_, _format_, _showPaths_, _changesFormat_,_pathFormat_} -**显示上一次成功构建之后的变化。 
      * _reverse_ -在顶部标示新近的构建。默认false。
      * _format_ -遍历构建信息，一个包含%X的字符串，其中%c为所有的改变，%n为构建编号。默认"Changes for Build #%nn%cn"。
      * _showPaths_, _changesFormat_, _pathFormat_ – 分别定义如${CHANGES}的_showPaths_、_format_和_pathFormat__参数。_
  * **${CHANGES_SINCE_LAST_UNSTABLE, _reverse_, _format_, _showPaths_,_changesFormat_, _pathFormat_} -**显示显示上一次不稳固或者成功的构建之后的变化。 
      * _reverse_ -在顶部标示新近的构建。默认false。
      * _format_ -遍历构建信息，一个包含%X的字符串，其中%c为所有的改变，%n为构建编号。默认"Changes for Build #%nn%cn"。
      * _showPaths_, _changesFormat_, _pathFormat_ -分别定义如${CHANGES}的_showPaths_、_format_和_pathFormat__参数。_
  * **${ENV, _var_} – **显示一个环境变量。 
      * _var_ – 显示该环境变量的名称。如果为空，显示所有，默认为空。
  * **${FAILED_TESTS} -**如果有失败的测试，显示这些失败的单元测试信息。
  * **${JENKINS_URL} -**显示Jenkins服务器的地址。(你能在"系统配置"页改变它)。
  * **${HUDSON_URL} -**不推荐，请使用$JENKINS_URL
  * **${PROJECT_NAME} -**显示项目的名称。
  * **${PROJECT_URL} -**显示项目的URL。
  * **${SVN_REVISION} -**显示SVN的版本号。
  * **${CAUSE} -**显示谁、通过什么渠道触发这次构建。
  * **${JELLY_SCRIPT, _template_} -**从一个Jelly脚本模板中自定义消息内容。有两种模板可供配置: HTML和TEXT。你可以在$JENKINS_HOME/email-templates下自定义替换它。当使用自动义模板时，"template"参数的名称不包含".jelly"。 
      * _template_ -模板名称，默认"html"。
  * **${FILE, _path_} -**包含一个指定文件的内容 
      * _path_ -文件路径，注意，是工作区目录的相对路径。
  * **${TEST_COUNTS, _var_} -**显示测试的数量。 
      * _var_ – 默认"total"。 
          * total -所有测试的数量。
          * fail -失败测试的数量。
          * skip -跳过测试的数量。

<http://www.juvenxu.com/2011/05/18/hudson-email-ext/>