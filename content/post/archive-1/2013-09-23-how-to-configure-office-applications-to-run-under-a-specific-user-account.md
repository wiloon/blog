---
title: How to configure Office applications to run under a specific user account
author: wiloon
type: post
date: 2013-09-23T02:23:23+00:00
url: /?p=5822
categories:
  - Uncategorized

---
This article was previously published under Q288367

<div>
  <h2>
    SUMMARY
  </h2>
  
  <p>
    We do not recommend or support automation to a Microsoft Office application from an unattended user account. For additional information on why Microsoft does not recommend automation under this context, click the following article number to view the article in the Microsoft Knowledge Base:<a href="http://support.microsoft.com/default.aspx?kbid=257757">257757</a> Considerations for server-side automation of Office
  </p>
  
  <p>
    If there is no choice but to automate Office from an unattended user account, the following steps can be used to configure the computer to run the Office application as a specific user, giving the application a fixed identity when it is started for Automation.
  </p>
</div>

<div>
  <h2>
    MORE INFORMATION
  </h2>
  
  <p>
    <strong>Caution</strong> Automation of any Office application from an unattended, non-interactive user account is risky and unstable. A single error in code or configuration can result in a dialog box that can cause the client process to stop responding (hang), that can corrupt data, or that can even crash the calling process (which could bring down your Web server if the client is ASP).
  </p>
  
  <p>
    <strong>Warning</strong> Office was not designed, and is not safe, for unattended execution on a server. Developers who use Office in this manner do so at their own risk.
  </p>
  
  <p>
    Regardless, it may be absolutely required to use Office in this manner. In these cases, special configuration must be done to avoid errors on Office startup. The steps in this article demonstrate how to configure Office to run as a specific user account when it is started for Automation.
  </p>
  
  <p>
    When you automate under a specific user account, you should be aware of the following problems:
  </p>
  
  <ul>
    <li>
      Any process that creates an Automation instance of the configured Office application creates the instance under the specific user account, allowing it to run with that user&#8217;s security credentials.
    </li>
    <li>
      Setting the Distributed Componenet Object Model (DCOM) settings to run as a specific user is global to the system. This setting affects all users and programs that automate the Office application on the system. Terminal Server clients may not be able to use Office appropriately. You should not use this setting and the steps in this article on an application Terminal Server.
    </li>
    <li>
      Component Object Model (COM) creates a unique WinStation for the new instance of the Office application. Any dialog boxes or warnings that may display do not appear on the interactive desktop. If you set the Visible flag for an application, the interactive user will not see that application. For more information about COM and WinStations, see the &#8220;References&#8221; section.
    </li>
    <li>
      When COM loads a server to run as a specific user account, the registry hive for that user is not loaded. Because the hive is not loaded for that user, the system .DEFAULT hive is used. Because Office has not been run under an account with this hive, you may receive dialog boxes that prompt you for input or the Office CD-ROMs to complete installation. The dialog boxes are not visible on the interactive desktop, so the application appears to stop responding (hang). The dialog boxes may time out and allow the process to continue, but after a noticeable delay in running the program. To work around this situation, install an NT service that runs under the same user account that is set for the DCOM setting. The NT Service Control Manager (SCM) loads the hive for that user when the service starts.
    </li>
  </ul>
  
  <p>
    Because the changes in DCOM are global, configuring Office in this manner can have negative side effects for other clients on the system that use Office. It is possible that another client application, or Terminal Server clients, will not be able to use the Office application after the settings are made. Consider carefully what impact this has to your server before you make any changes to the DCOM configuration settings.
  </p>
  
  <p>
    If the problems listed here are too great for your design, or cause other unidentified problems, it is possible to configure Office differently and still allow it to start from an unattended process or service.
  </p>
  
  <p>
    For additional information, click the following article numbers to view the articles in the Microsoft Knowledge Base:<a href="http://theether.net/download/Microsoft/kb/288366.html">288366</a> How To Configure Office Applications to Run Under the Interactive User Account
  </p>
  
  <p>
    <a href="http://theether.net/download/Microsoft/kb/288368.html">288368</a> How To Configure Office Applications for Automation from a COM+/MTS Package
  </p>
  
  <h3>
    Configuring Office as a Specific User
  </h3>
  
  <p>
    To set up an Office Automation server under a specific user account, follow these steps:
  </p>
  
  <ol>
    <li>
      Log on to the computer as the Administrator and create a new user account that will automate Office. In our example, this account is named <strong>OfficeAutomationUser</strong>. Create a password for this user account, and select <strong>Never expire</strong> so that the password does not have to be changed.
    </li>
    <li>
      Add the <strong>OfficeAutomationUser</strong> account to the <strong>Administrators</strong> group.
    </li>
    <li>
      Log in to the computer as <strong>OfficeAutomationUser</strong> and install (or reinstall) Office using a complete install. For system robustness, it is recommended that you copy the contents of the Office CD-ROM to a local drive and install Office from this location.
    </li>
    <li>
      Start the Office application that you intend to automate. This forces the application to register itself.
    </li>
    <li>
      After the application is running, press ALT+F11 to load the Microsoft Visual Basic for Applications (VBA) editor. This forces VBA to initialize itself.
    </li>
    <li>
      Close the applications, including VBA.
    </li>
    <li>
      Click <strong>Start</strong>, click <strong>Run</strong>, and then type <kbd>DCOMCNFG</kbd>. Select the application that you want to automate. The application names are listed below:Microsoft Access 97/2002 &#8211; Microsoft Access Database<br /> Microsoft Access 2003 &#8211; Microsoft Office Access Application<br /> Microsoft Excel 97/2000/2002/2003 &#8211; Microsoft Excel Application<br /> Microsoft Word 97 &#8211; Microsoft Word Basic<br /> Microsoft Word 2000/2002/2003 &#8211; Microsoft Word Document</p> <p>
        Click <strong>Properties</strong> to open the property dialog box for this application.</li> 
        
        <li>
          Click the <strong>Security</strong> tab. Verify that <strong>Use Default Access Permissions</strong> and <strong>Use Default Launch Permissions</strong> are selected.
        </li>
        <li>
          Click the <strong>Identity</strong> tab. Select <strong>This User</strong> and type the username and password for <strong>OfficeAutomationUser</strong>.
        </li>
        <li>
          Click <strong>OK</strong> to close the property dialog box and return to the main applications list dialog box.
        </li>
        <li>
          In the DCOM Configuration dialog box, click the <strong>Default Security</strong> tab.
        </li>
        <li>
          Click <strong>Edit Defaults</strong> for access permissions. Verify that the following users are listed in the access permissions, or add the users if they are not listed:SYSTEM<br /> INTERACTIVE<br /> Everyone<br /> Administrators<br /> OfficeAutomationUser<br /> IUSR_<machinename><strong>*</strong><br /> IWAM_<machinename><strong>*</strong></p> <p>
            <strong>*</strong> These accounts exist only if Internet Information Server (IIS) is installed on the computer.</li> 
            
            <li>
              Make sure that each user is allowed access, and then click <strong>OK</strong>.
            </li>
            <li>
              Click <strong>Edit Defaults</strong> for launch permissions. Verify that the following users are listed in the launch permissions, or add the users if they are not listed:SYSTEM<br /> INTERACTIVE<br /> Everyone<br /> Administrators<br /> OfficeAutomationUser<br /> IUSR_<machinename><strong>*</strong><br /> IWAM_<machinename><strong>*</strong></p> <p>
                <strong>*</strong> These accounts exist only if IIS is installed on the computer.</li> 
                
                <li>
                  Make sure that each user is allowed access, and then click <strong>OK</strong>.
                </li>
                <li>
                  Click <strong>OK</strong> to close DCOMCNFG.
                </li>
                <li>
                  Start <strong>REGEDIT</strong> and then verify that the following keys and string values exist for the Office application that you want to automate:<strong>Microsoft Access 2000/2002/2003:</strong><br /> Key: HKEY_CLASSES_ROOTAppIDMSACCESS.EXE<br /> AppID: {73A4C9C1-D68D-11D0-98BF-00A0C90DC8D9}</p> <p>
                    <strong>Microsoft Access 97:</strong><br /> Key: HKEY_CLASSES_ROOTAppIDMSACCESS.EXE<br /> AppID: {8CC49940-3146-11CF-97A1-00AA00424A9F}
                  </p>
                  
                  <p>
                    <strong>Microsoft Excel 97/2000/2002/2003:</strong><br /> Key: HKEY_CLASSES_ROOTAppIDEXCEL.EXE<br /> AppID: {00020812-0000-0000-C000-000000000046}
                  </p>
                  
                  <p>
                    <strong>Microsoft Word 97/2000/2002/2003:</strong><br /> Key: HKEY_CLASSES_ROOTAppIDWINWORD.EXE<br /> AppID: {00020906-0000-0000-C000-000000000046}
                  </p>
                  
                  <p>
                    If these keys do not exist, you can create them by running the following .reg file on your system:
                  </p>
                  
                  <pre>REGEDIT4

[HKEY_CLASSES_ROOTAppIDWINWORD.EXE]
"AppID"="{00020906-0000-0000-C000-000000000046}"

[HKEY_CLASSES_ROOTAppIDEXCEL.EXE]
"AppID"="{00020812-0000-0000-C000-000000000046}"

[HKEY_CLASSES_ROOTAppIDMSACCESS.EXE]
"AppID"="{73A4C9C1-D68D-11D0-98BF-00A0C90DC8D9}"</pre>
                  
                  <p>
                    <strong>Note</strong> The sample .reg file is for Access 2000, Access 2002, or Office Access 2003. If you are using Access 97, change the AppID key to:
                  </p>
                  
                  <pre>"AppID"="{8CC49940-3146-11CF-97A1-00AA00424A9F}"</pre>
                </li>
                
                <li>
                  To avoid registry conflicts, install and run an NT service. Set the identity of the service to run as <strong>OfficeAutomationUser</strong>, and select <strong>Automatic</strong> as the startup type. For more information on creating a sample Visual C++ NT Service, see the following Microsoft Developer Network (MSDN) Web site:Creating a Simple Win32 Service in C++<br /> <a href="http://msdn.microsoft.com/library/default.asp?url=/library/en-us/dndllpro/html/msdn_ntservic.asp" target="_top">http://msdn.microsoft.com/library/default.asp?url=/library/en-us/dndllpro/html/msdn_ntservic.asp</a>
                </li>
                <li>
                  Restart the system. This is required.
                </li></ol> </div> 
                
                <div>
                  <h2>
                    REFERENCES
                  </h2>
                  
                  <p>
                    For additional information, click the following article numbers to view the articles in the Microsoft Knowledge Base:<a href="http://support.microsoft.com/default.aspx?kbid=169321">169321</a> COM servers activation and NT Windows stations
                  </p>
                  
                  <p>
                    <a href="http://theether.net/download/Microsoft/kb/158508.html">158508</a> COM security frequently asked questions
                  </p>
                  
                  <p>
                    <a href="http://support.microsoft.com/default.aspx?kbid=184291">184291</a> COM objects fail to print when called from ASP
                  </p>
                  
                  <p>
                    For more information about automation from Internet scripts, visit the following Microsoft Web site:Office Automation With Internet Scripting<br /> <a href="http://support.microsoft.com/default.aspx?scid=%2fsupport%2fofficedev%2fInetASP.asp" target="_top">http://support.microsoft.com/support/officedev/InetASP.asp</a>
                  </p>
                  
                  <p>
                    <a href="http://theether.net/download/Microsoft/kb/288367.html">http://theether.net/download/Microsoft/kb/288367.html</a>
                  </p>
                </div>