---
title: 'How to: List Current Keyboard Shortcuts'
author: wiloon
type: post
date: 2013-08-08T08:28:29+00:00
url: /?p=5764
categories:
  - Uncategorized

---
<div>
  <p>
    Use this procedure to create a macro that generates a list of all the commands in the integrated development environment (IDE) and any shortcut keys mapped to those commands according to the current keyboard mapping scheme.
  </p>
  
  <p>
    Several keyboard mapping schemes are available in the IDE. You can change keyboard mapping schemes on the Keyboard page, under the Environment folder of theOptions dialog box. For more information, see <a href="http://msdn.microsoft.com/en-us/library/5zwses53(v=vs.100).aspx">How to: Work with Keyboard Shortcuts</a>.
  </p>
  
  <div>
    <table>
      <tr>
        <th>
          <img id="alert_note" title="Note" alt="Note" src="http://i.msdn.microsoft.com/areas/global/content/clear.gif" /><strong>Note</strong>
        </th>
      </tr>
      
      <tr>
        <td>
          The dialog boxes and menu commands you see might differ from those described in Help depending on your active settings or edition. To change your settings, clickImport and Export Settings on the Tools menu. For more information, see <a href="http://msdn.microsoft.com/en-us/library/zbhkx167(v=vs.100).aspx">Working with Settings</a>.
        </td>
      </tr>
    </table>
  </div>
</div>

### To list current keyboard shortcut mappings

<div>
  <ol>
    <li>
      On the Tools menu, point to Macros, and then click Macros IDE.
    </li>
    <li>
      In Project Explorer, double-click MyMacros.
    </li>
    <li>
      Right-click Module1 and then click Rename.
    </li>
    <li>
      Type KeyboardShortcuts as the new name for the module.
    </li>
    <li>
      Double-click KeyboardShortcuts to open the file in the editor.
    </li>
    <li>
      Paste the following code in the file after Public Module KeyboardShortcuts: <div id="code-snippet-1">
        <div>
        </div>
        
        <div>
          <div>
          </div>
          
          <div dir="ltr" id="CodeSnippetContainerCode_5caf603c-61bf-4bff-b2e9-fbb55e05b63f">
            <div>
              <pre>Sub GetAllCommands()

    Dim cmd As Command
    Dim ow As OutputWindow = DTE.Windows.Item(Constants.vsWindowKindOutput).Object
    Dim owp As OutputWindowPane
    Dim exists As Boolean
    Dim i As Integer
    Dim sArray() As String

    sArray = New String() {}
    i = 1
    exists = False

    For Each owp In ow.OutputWindowPanes
        If owp.Name = "Macro Output" Then
            exists = True
            Exit For
        End If
        i = i + 1
    Next

    If exists Then
        owp = ow.OutputWindowPanes.Item(i)
    Else
        owp = ow.OutputWindowPanes.Add("Macro Output")
    End If

    owp.Clear()

    ' Output 1 line per command
    For Each cmd In DTE.Commands
        Dim binding As Object
        Dim shortcuts As String
        shortcuts = ""

        For Each binding In cmd.Bindings
            Dim b As String
            b = binding
            If Not shortcuts = "" Then
                shortcuts += "--OR-- "
            End If
            shortcuts = shortcuts + b + " "
        Next

        shortcuts = shortcuts.Trim()

        If Not cmd.Name.Trim().Equals("") And Not shortcuts.Equals("") Then
            sArray.Resize(sArray, sArray.Length + 1)
            sArray(sArray.Length - 1) = cmd.Name + vbTab + shortcuts
        End If
    Next

    Array.Sort(sArray)
    owp.OutputString(String.Join(vbCrLf, sArray))

End Sub</pre>
            </div>
          </div>
        </div>
      </div>
    </li>
    
    <li>
      On the File menu, click Save MyMacros.
    </li>
    <li>
      Switch back to Visual Studio.
    </li>
    <li>
      On the Tools menu, point to Macros and then click Macro Explorer.
    </li>
    <li>
      Expand MyMacros and then expand KeyboardShortcuts.
    </li>
    <li>
      Right-click GetAllCommands and then click Run. <p>
        The macro generates a list of all possible commands in the IDE and any keyboard shortcut mappings these commands have in the current keyboard mapping scheme.</li> 
        
        <li>
          On the View menu, click Output. <p>
            Commands and their shortcut key combinations appear in the Output window. You can copy this information and paste it into another application, such as Microsoft Office Excel, for additional formatting and printing options.</li> </ol> 
            
            <p>
              <a href="http://msdn.microsoft.com/en-us/library/ms247076(v=VS.100).aspx">http://msdn.microsoft.com/en-us/library/ms247076(v=VS.100).aspx</a>
            </p></div>