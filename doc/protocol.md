# HMI-Protocol
Lang: German

## Annahmen
Der CAN-Bus ist für die Vorliegende Anwendung reserviert.
Es werden daher keine kritischen Daten über den CAN-Bus gesendet (Steuerung des Motors/ Bremssystem).
Die Nutzereingaben sind nicht größer als 1 KB.  
Die Nutzereingaben sind nicht endlich, eingeben wie Adressen (Navigation) können vom Nutzer beliebig eingegeben werden.

## Physikalische Verbindung: 
Das Protokoll ist CAN-Bus basiert, daher wird die Kommunikation über einen
CAN-BUS realisiert. 

## Datenflusskontrolle (Handshake):
Empfangene Pakete werden mit der ACK Flag bestätigt.
Das SG speichert empfangene Daten bis zu ihrer verarbeitung ab.
Mit einem Filter entscheidet ein SG, ob es ein Frame zwischenspeichert oder verwirft.
Die Nachrichten sind über die ´arbitration_id´ geknnzeichnet und werden über diese den SGs zugeordnet.  

Das HMI antwortet einem SG indem es im Bereich dessen arbitration_id Antwortet.  

Für eine Anfrage des A-SG wird ein Handshake zwischen dem HMI-SG und dem A-SG durchgeführt.  
Mit diesem Handshake einigen sich beide Seiten darauf, dass das HMI-SG sich nun um die Anfrage des 
A-SG kümmern wird.

Im Rahmen einer solchen Request-Response-Session nimmt das HMI-SG nur noch Frames des an der Session beteiligten A-SGs an.  
Hierdurch wird der Zugriff auf das HMI-SG geregelt.


## Vereinbarung der verschiedenen Verbindungscharakteristiken
Die Verbindung enthält nur Multicast-Pakete (da CAN).
Die Empfänger filtern selbständig nach den für sie relevanten Paketen.
CAN 2.0A 11 bit Identifier bietet 2^11 unterschiedliche Nachrichten.
Wird als ausreichendangesehen, sollten mehr unterschiedliche Nachrichten benötigt werden kann
auf CAN 2.0B gewechselt werden (hängt von der Anzahl der Geräte ab).  

Die Request-Codes sind beiden Parteien zu beginn bekannt und konstant.  

(optional) Es ist vordefiniert, über welchen Nachrichten-Identifier das HMI-SG dem entsprechendem A-SG antwortet.


## Wie eine Botschaft beginnt und endet
Das Protokoll basiert auf CAN.
Eine Botschaft wird innerhalb einer Response-Reply-Session übertragen.
Diese Beginnt mit einem Handshake auf Anfrage des A-SGs und endet nach dem erfolgreichen
versenden der Antwort/Reply durch das HMI-SG.


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

Welchem Typ ein Frame angehört steht in den ersten 4 Bits der Payload.
Vereinfacht können auch das erste Byte für den Typen angeben, es werden jedoch nur 4 Bits benötigt.
Danach kommt ein byte lang die Frame-ID welche bei der Bestätigung durch ein ACK angegeben wird.  
Die Frame-ID gibt zudem die Reihenfolge an, in der die Pakete versendet wurden.
Im Falle des DATA-Frames wird die Frame-ID zu einer Sequenz-Nummer die verwendet wird, um die Reiehnfolge der 
Datenpakte separat betrachten zu können.
Nachfolgend wird der Aufbau der Payload beschrieben.

#### REQUEST-Frame:
Hier werden dei restlichen bytes der payload für den eindeutigen Request-Code verwendet.
Dieser ist in Vorfeld beiden Parteien bekannt und gibt dem HMI-SG an, welche Eingabe vom Nutzer werwartet wird.
#### REQUEST_ACK-Frame:
Nach dem Frame-Typ Feld wird die Frame-ID des erhaltennen Pakets hochgezählt und dahinter geschrieben.
In einem weiterem Byte kann der Timeout für das A-SG übergeben werden.
Das A-SG wartet diesen Zeitraum ab, bevor es die Verbindung als verloren ansieht.
Diese Zeitraum sollte an die Bearbeitungsdauer der Anfrage angepasst werden.
Wird kein Timeout angegeben, wartet das A-SG blockierend, bis zur Antwort.
#### ACK-Frame:
Enthält neben dem Frame-Typ die Frame-ID des Frames, dessen Empfang bestätigt wurde.

#### RESPONSE_INFO-Frame:
Neben Frame-Typ und Frame-ID wird hier die Anzahl der in der vom HMI-SG zum A-SG zu sendenden DATA-Frames an.
Hierdruch kann sich das A-SG auf den empfang dieser Daten einstellen.
Für große Datenmengen kann hier auch angegben werden, wieviele DATA-Frames auf einmal durch nur eine ACK-Bestätigt werden können.
Mit solchen großen Datenmengen ist aber bei den Nutzereingaben über Wahltasten nicht zu rechnen.

#### DATA-Frame:
Neben Frame-Typ wird die Sequenz-Nummer angegeben, diese ist ein Byte lang.
Hinter der Seguenz-Nummer können die restlichen 5 Bytes für Daten verwendet werden.
Soll eine Checksum eingesetzt werden, so befinden sich im 3ten byte keine Daten sondern die Checksum.
Diese besteht aus der Summer der restlichen Datenbytes modulo 256.
Durch das Sequenz-Feld können maximal 255 Data-Frames an das A-SG geschickt werden.
Mit checksum sind das 1020 Bytes und damit genug für die textbasierten Nutzer-Eingaben.
Müssen mehr Daten versendet werden, kann dies durch Bündelnung von Frames unter einer ACK erfolgen.
Siehe ISO 15765-2.
#### FIN-Frame:
Enthält Frame-Typ und Frame-ID.


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
