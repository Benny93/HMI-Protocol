# Fallaufgabe Vector Notizen

## Controller Area Network (CAN)

CAN-Kommunikation
ungerichtet.
Frames (w’ pakete)
alle SG erhalten Frames und filtern relevante Frames heruas


## Steuergerät SG

Randbedingungen
CAN-Bus
mehrere Applikations-SG
Ein Human Machine Interaction-SG (HMI-SG)

HMI-SG: Display mit Eingabetasten

Applikations-SG: Anwendung, benötigt User Input (z.B. für navigation)

Alle A-SG nutzen das HMI-SG zur Interaktion mit dem Fahrer

Alle A-SG können gleichzeitig Anfragen an das HMI-SG senden

-> schreit nach Queue (consumer producer)

## Aufgabe: 
- Protokoll entwerfen: HMI-Protokoll auf CAN-Basis
- Ermöglicht die quasi gleichzeitige Kommunikation zwischen A-SG und HMI-SG
- Zuordnung der Botschaften zum korrekten A-SG sicherstellen (jede Antwort des Fahrers muss der richtigen Frage eines A-SG zugeordnet werden)
- Zugriff auf HMI-SG regeln: Es kann immer nur die Anfrage eines A-SG zu einer Zeit beantwortet werden

## Untersuchung von CAN

In CAN gibt es Collisionserkennung z.b. CSMA.
hierbei wird ein priorisiertes Paket bevorzugt.
-> Sollte nur für wichtige Application-SG verwendet werden und A-SGs die gerade die Frage des Fahrers beantworten

Sortierung der Multicast Pakete:
Ist eine Sortierung der Pakete notwendig?
Eigentlich nicht, es soll zwar quasi gleichzeitig kommuniziert werden, es gibt aber keiner Reihenfolge wer nach wem
-> Die aufgabe umfasst keine Priorisierung

Identifikation: Für die korrekte Zuordnung müssen Pakete identifiziert werden können
-> CAN bietet ein Identifier Feld

Niedrige ID bdeutet hohe priorität.
Das HMI hat vorrang, sollte also eine niedrigere ID haben als die anderen Geräte.

## Was gehört alles in ein Protokoll?
- Feststellen der zugrundeliegenden physikalischen Verbindung (z. B. LAN oder W-LAN) oder der Existenz des anderen Endpunkts der Verbindung
- Datenflusskontrolle (Handshaking)
- Vereinbarung der verschiedenen Verbindungscharakteristiken
- Wie eine Botschaft beginnt und endet
- Wie eine Botschaft formatiert ist
- Was mit beschädigten oder falsch formatierten Botschaften getan wird (Fehlerkorrekturverfahren)
- Wie unerwarteter Verlust der Verbindung festgestellt wird und was dann zu geschehen hat
- Beendigung der Verbindung

## Weitere Gedanken
Fallaufgabe Vector Protokoll work in progress

Protokolle werden als finite state machines (FSM), also als endliche Automaten modelliert.
-> Popovic, M. (2016). Communication protocol engineering. CRC press.

What must be done?
-> Grob Beschrieben durch Aufgabenstellung
How can the solution be verified?
Testsuite for the finite statemachines

### Protokoll

Fragen:

Physikalische Verbindung:
Das Protokoll ist CAN-Bus basiert, daher wird die Kommunikation über einen CAN-BUS realisiert.

Datenflusskontrolle (Handshake):
Der Multicastansatz erfordert keinen Handshake, allerdings werden Nachrichten gefiltert und müssen dem Absender eindeutig zugeordnet werden können.

Das HMI-SG:
Das HMI-SG besitzt eine Nachrichten-Queue Q.
In Q werden alle über den Bus ankommenden Pakete abgelegt.
Dies verhindert vorerst, dass Pakete verloren gehen, auf die das HMI-SG nicht direkt antworten kann (zeitlich).

Exception:
Läuft der Speicher der Queue voll, werden die ältesten Pakete (da FIFO also HEAD der Queue) gedroppt.
Dabei sollte der Sender dieser Pakete über den Drop informiert werden.

