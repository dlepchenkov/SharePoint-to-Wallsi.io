# SharePoint-to-Wallsi.io
The process of automatically publishing ads from Power App to Walls.io using Power Automate, OneDrive, and a Python script on a virtual machine connected to Azure.
> Dieses Dokument beschreibt den Prozess der automatischen Posten von Anzeigen aus Power App in [Walls.io](http://walls.io/) unter Verwendung von Power Automate, OneDrive und einem Python-Skript auf einer VM mit Azure-Verbindung.

Ziel: Beim Erstellen einer Anzeige in schwarzess Brett (Power App) soll eine automatische Veröffentlichung der Anzeige auf [Walls.io](http://walls.io/) erfolgen. 

So Sieht’s aus:
1. User erstellt eine Anzeige im Schwarzess Brett (Microsoft Power App) 
2. Anzeige ist automatisch im SharePoint List gespeichert
3. Power Automate Flow ist automatisch von Anzeige im List getriggert
4. Mit “Get attachments” sammelt attachments aus diese Anzeige
5. Mit “Get attachment content” und eine spezielle Formula (s. Foto) in file identifier wird nur das erstes Bild extrahiert
6. Erstellt “.png” File im OneDrive, im File Content ändert den Inhalt von Bits in Binärcode.
7. Erstellt eine .txt-Datei in OneDrive mit dem gewünschten Textinhalt aus Anzeige
8. Files befinden sich in eine OneDrive Directory
9. Python Script befindet sich in eine Windows VM. Um es Zugriff zu Onedrive zu geben, wird es mit dem Azure Verbunden. 
Logik des Skripts: Mithilfe von Azure Connection überprüft der Code zunächst den Ordner in OneDrive auf Dateien, deren Namen noch nicht in der CSV-Datei vorhanden sind. Er kompiliert die Daten und postet sie auf [Walls.io](http://walls.io/). 
10. Anzeige wird auf [Walls.io](http://Walls.io) gepostet
