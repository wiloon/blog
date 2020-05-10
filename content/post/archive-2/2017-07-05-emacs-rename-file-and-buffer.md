---
title: emacs rename file and buffer
author: wiloon
type: post
date: 2017-07-05T04:26:54+00:00
url: /?p=10783
categories:
  - Uncategorized

---
https://stackoverflow.com/questions/384284/how-do-i-rename-an-open-file-in-emacs

;; source: http://steve.yegge.googlepages.com/my-dot-emacs-file
  
(defun rename-file-and-buffer (new-name)
    
&#8220;Renames both current buffer and file it&#8217;s visiting to NEW-NAME.&#8221;
    
(interactive &#8220;sNew name: &#8220;)
    
(let ((name (buffer-name))
          
(filename (buffer-file-name)))
      
(if (not filename)
          
(message &#8220;Buffer &#8216;%s&#8217; is not visiting a file!&#8221; name)
        
(if (get-buffer new-name)
            
(message &#8220;A buffer named &#8216;%s&#8217; already exists!&#8221; new-name)
          
(progn
            
(rename-file filename new-name 1)
            
(rename-buffer new-name)
            
(set-visited-file-name new-name)
            
(set-buffer-modified-p nil))))))