# HMI-Protocol
Lang: German

## Annahmen
Der CAN-Bus ist für die Vorliegende Anwendung reserviert.
Es werden daher keine Kritischen Daten über den CAN-Bus gesendet (Steuerung des Motors/ Bremssystem)

## Physikalische Verbindung: 
Das Protokoll ist CAN-Bus basiert, daher wird die Kommunikation über einen
AN-BUS realisiert. 

## Datenflusskontrolle (Handshake):
Empfangene Pakete werden mit der ACK Flag bestätigt.
Das SG speichert empfangene Daten bis zu ihrer verarbeitung ab.

## Vereinbarung der verschiedenen Verbindungscharakteristiken
Die Verbindung enthält nur Multicast-Pakete (da CAN).
Die Empfänger filtern selbständig nach den für sie relevanten Paketen.


## Wie eine Botschaft beginnt und endet
Das Protokoll basiert auf CAN.
![CAN Frame Wiki](https://de.wikipedia.org/wiki/Controller_Area_Network#/media/File:CAN-Bus-frame_in_base_format_without_stuffbits.svg)
Die Botschaften bestehen daher aus Frames.
Start und Entsprechend den durch CAN vorgegeben Aufbau.


## Wie eine Botschaft formatiert ist
Die Botschaft muss immer der Absender Enthalten.
Zusätzlich soll über den Absender festgestellt werden können, ob es sich um ein A-SG oder ein HMI-SG handelt.

Die Empfangsbestätigung erfolgt durch das CAN-Protokoll.
Hierbei setzten die CAN-Bus Knoten des ACK Bit auf high, sofern sie die Nachricht fehlerfrei erhalten haben.

Das HMI-SG hat eine höhere Prio als die A-SGs.
Daher wird ein niedriger Identifier vergeben.
Das bewirkt im CAN-Protokoll eine Bevorzugung des HMI-SG und sorgt so für eine möglichst schnelle Antwort des HMI-SG.
Die schnelle/effiziente Antwort ist wichtig, damit das HMI-SG die Anfragen anderer A-SG beantworten kann.


## Was mit beschädigten oder falsch formatierten Botschaften getan wird (Fehlerkorrekturverfahren)
Beschädigte Botschaften werden abgelehnt und dem Absender ein festgelegtes Fehlermeldungs-Frame zugeschickt.
Hierdurch erhält der Absender die Information, dass sein Paket nur beschädigt eingetroffen ist, und kann es erneut senden.
Die Fehlermeldung muss die ID des Frames enthalten, sodass der Sender weiß, um welches Frame es sich handelt.

## Wie unerwarteter Verlust der Verbindung festgestellt wird und was dann zu geschehen hat
Wird die Verbindung unerwartet beendet, beginnen die Instanzen ihre Kommunikation sofern möglich vom der letzen 
erfolgreichen Kommunikation aus erneut. 
Im Fall eines kompletten Verlustes der Frames, wird die Verbinung neu gestartet.

Die Instanzen sollen weiterarbeiten können, sobald sie sich wieder gegenseitig erreichen können.
Daher pausiert jede Instanz so lange, bis die Verbinung wieder aufgebaut werden konnte.

Hier wird davon ausgegangen, dass die Instanzen nur nach erfolreicher Kommunikation ihre Arbeit fortsetzen können.
Der Nachteil an diesem Ansatz ist, dass die Instanzen durch das Warten auf die Verbindung blockiert werden.

## Beendigung der Verbindung
Die Beendigung der Verbindung kann sowohl vom HMI-SG als auch vom A-SG ausgehen.
Hierbei wird ein vordefiniertes Frame mit Absender und Empfänger zum Beenden der Verbindung gesendet.
Der HMI-SG hat die möglichkeit, bei einem zu langen Timeout des A-SGs die Verbinung zu beenden.
Das A-SG beendet die verbindung, sobald es die im Moment erforderliche Kommunikation zum HMI-SG abgeschlossen hat.

