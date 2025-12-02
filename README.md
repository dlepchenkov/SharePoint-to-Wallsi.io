# SharePoint-to-Wallsi.io
The process of automatically publishing ads from Power App to Walls.io using Power Automate, OneDrive, and a Python script on a virtual machine connected to Azure.
Objective: When creating an ad on the bulletin board (Power App), the ad should be automatically published on [Walls.io](http://walls.io/).

Here's how it works:
1. User creates an ad on the bulletin board (Microsoft Power App)
2. Ad is automatically saved in the SharePoint list
3. Power Automate Flow is automatically triggered by the notice in the list.
4. “Get attachments” collects attachments from this notice.
5. “Get attachment content” and a special formula in file identifier extract only the first image.
6. Creates a “.png” file in OneDrive, changes the content of bits in binary code in File Content.
7. Creates a .txt file in OneDrive with the desired text content from the display
8. Files are located in a OneDrive directory
9. Python script is located in a Windows VM. To give it access to OneDrive, it is connected to Azure.  (see the .py file in branch)
Logic of the script: Using Azure Connection, the code first checks the folder in OneDrive for files whose names are not yet in the CSV file. It compiles the data and posts it to [Walls.io]. 
10. Display is posted to [Walls.io]
