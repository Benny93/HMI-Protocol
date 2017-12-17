# HMI-Protocol
Lang: German

## Annahmen
Der CAN-Bus ist für die Vorliegende Anwendung reserviert.
Es werden daher keine kritischen Daten über den CAN-Bus gesendet (Steuerung des Motors/ Bremssystem)

## Physikalische Verbindung: 
Das Protokoll ist CAN-Bus basiert, daher wird die Kommunikation über einen
CAN-BUS realisiert. 

## Datenflusskontrolle (Handshake):
Empfangene Pakete werden mit der ACK Flag bestätigt.
Das SG speichert empfangene Daten bis zu ihrer verarbeitung ab.
Mit einem Filter entscheidet ein SG, ob es ein Frame zwischenspeichert oder Verwirft
Die Nachrichten sind über die ´arbitration_id´ geknnzeichnet und werden über diese den SGs zugeordnet.

Das HMI antwortet einem SG indem es im Bereich dessen arbitration_id Antwortet.
Für die arbitration_id s gibt es masken.
Diese Verhalten sich vergleichbar mit den Masken von IP-Adressen.
Die Aufteilung der Topics geschickt folglich über die Masken.
Das Problem hierbei: Masken mit Hohen Werten werden sehr niedrig priorisiert.
Die Maske für die Antworten des HMI ist daher so zu wählen, dass dessen arbitration_id möglichst niedrig bleibt.

Für eine Anfrage des A-SG wird ein Handshake zwischen dem HMI-SG und dem A-SG durchgeführt.
Mit diesem Handshake einigen sich ebide Seiten darauf, dass das HMI-SG sich nun um die Anfrage des 
A-SG kümmern wird.




## Vereinbarung der verschiedenen Verbindungscharakteristiken
Die Verbindung enthält nur Multicast-Pakete (da CAN).
Die Empfänger filtern selbständig nach den für sie relevanten Paketen.
CAN 2.0A 11 bit Identifier bietet 2^11 unterschiedliche Nachrichten.
Wird als ausreichendangesehen, sollten mehr unterschiedliche Nachrichten benötigt werden kann
auf CAN 2.0B gewechselt werden (hängt von der Anzahl der Geräte ab).


## Wie eine Botschaft beginnt und endet
Das Protokoll basiert auf CAN.
![CAN Frame Wiki](https://de.wikipedia.org/wiki/Controller_Area_Network#/media/File:CAN-Bus-frame_in_base_format_without_stuffbits.svg)
Die Botschaften bestehen daher aus Frames.
Start und Entsprechend den durch CAN vorgegeben Aufbau.


## Wie eine Botschaft formatiert ist
Die Botschaften bestehen aus CAN-Frames.
Die arbitrations id gibt dabei an, welches A-SG die Nachricht gesendet hat.
Bei einer Anfrage aktiviert das A-SG einen Filter und hört somit nur noch auf CAN-Frames die
vom HMI-SG direkt an das A-SG gerichtet sind.  
Die arbitrations-id sind also vergleichbar mit Topics in Publish-Subscribe-Nachrichten.  
Um einem A-SG direkt zu antworten, wählt das HMI-SG die arbutrations-id, folglich die Topic, auf die das A-SG hört.  
Hierdurch hören A-SGs nur auf Antworten, die auch für sie bestimmt sind.  
Die Zuordnung der arbitration-ids zu den A-SGs wird im Vorfeld festgelegt.
Optional kann das A-SG auch die arbitration-id von der es eine Antwort erwartet in der Anfrage bekannt geben.
Dies ermöglicht ein dynamisches Einstellen der arbitration-id der Antwort.  
Die Masken der Filter haben für dieses Protokoll keine relevanz.  
Die arbitration-ids der HMI-SG-Antworten werden auf niedrigere Werde gelegt, da der CAN-Bus niedrige Identifier bevorzugt.
Hierdurch wird eine effiziente Antwortzeit des HMI-SG unterstützt.  
### Frame typen

Es gibt 6 Typen von Frames.
- REQUEST: Enthält die Anfrage in Form eines fordefinierten Anfragecodes
- REQUEST_ACK: HMI-SG nimmmt die Anfrage an und wird diese bearbeiten
- ACK: Bestätigt den Erhalt eines DATA, REQUEST_ACK oder FIN-Pakets
- RESPONSE_INFO: Gibt Informationen darüber, wieviele DATA-Frames übertragen werden und gibt einen Timeout an.
- DATA: Enthält die Antwort des Nutzers
- FIN: Markiert das Ende einer HMI-Antwort



## Was mit beschädigten oder falsch formatierten Botschaften getan wird (Fehlerkorrekturverfahren)
Die Payload eines DATA-Frames kann mit einer ein byte großen Checksum versehen werden.
Diese wird aus der Summe der Datenbytes modulo 256 berechnet.
Errechnet sich die Prüfsumme nicht aus den Empfangen Daten, wird kein ACK vom A-SG versendet.
Das HMI-SG läuft daraufhin in einen Timout für das ACK und Sendet das Paket erneut.
Wie oft das HMI-SG erneut sendet ist konfigurationsabhängig.
Nach zu vielen Fehlübertragungen bricht das HMI-SG die Datenübertragung ab und wartet auf neue Anfragen durch A-SGs.
In diesem Fall wird von einem defektem A-SG ausgegangen. 
Das A-SG läuft ebenfalls in ein Timeout und wird seine Anfrage erneut stellen.
Hierdurch tritt es wieder in Konkurrenz mit den anderen A-SG, wodurch diese eine Chance auf die Bearbeitung ihrer Anfrage erhalten.


## Wie unerwarteter Verlust der Verbindung festgestellt wird und was dann zu geschehen hat
Der Verlust der Verbindung wird durch das verstreichen eines Timeouts festgestellt.
Hier wird davon ausgegangen, dass die A-SGs nur nach erfolreicher Kommunikation ihre Arbeit fortsetzen können.
Wird eine Anfrage nicht durch ein Request-ACK-bestätigt, versucht das A-SG nach einem Timeout die Request erneut zu stellen.
Dies verhindert, dass das A-SG auf unbestimmte Zeit blockiert wird.
Zudem ermöglicht die erneute Anfrage an das HMI-SG die Chance auf einen neuen Verbindungsaufbau.

Innerhalb einer Verbindung besteht auch die Option die Timeouts zu deaktivieren.
In diesem Fall sind die A-SGs blockiert, während diese auf eine Antwort des HMI-SGs warten.

## Beendigung der Verbindung
Die Antworten des HMI-SGs bestehen aus einem oder mehreren Frames.
Das HMI-SG beendet die Verbindung, sobald es für jedes zu sende Frame eine bestätigung des A-SG erhält.
Zum Beenden der Verbindung sendet das HMI-SG ein FIN-Frame.
Wird dieses vom A-SG bestätigt, wissen beide Seiten, dass die Verbindung nun beendet ist.
Das HMI-SG nimmt nun wieder neue Anfragen entgegen.  

Der HMI-SG hat die möglichkeit, bei einem zu langen Timeout des A-SGs die Verbinung zu beenden.
Dazu wartet das HMI-SG nicht mehr weiter, sondern nimmt wieder neue Anfragen entgegen.  

Auch das A-SG kann die Verbindung beenden, wenn es zu einem Timeout kommt.  
Hierzu versucht es die Anfrage von Neuem zu senden.
Das HMI-SG wird ebenfalls in einen Timeout laufen und somit wieder neue Anfragen Annehmen.  

Die bei Verlust der Verbindung wird folglich durch einen Timeout in den Ursprungszustand zurückgekehrt, 
so lange, bis die Anfrage erfolreich war.
Nach der Annahme, dass das A-SG die Antwort auf die Anfrage benötigt um weiterarbeiten zu können, ist diese Maßenahme sinnvoll.  
