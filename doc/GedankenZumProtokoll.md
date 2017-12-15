# Vector CAN Aufgbabe Gedanken
Auch wenn CAN ein Master Multicast System ist, sollte das Protokoll als Client Server Kommunikation umgesetzt werden.
Hierbei ist die HMI-SG der Server und die A-SG die Clients.

Beim HMI-SG kann davon ausgegangen werden, dass es mehrer A-SG zu gleichen Zeit abhandeln kann (genügend Rechenleistung).

Als Server ist es sinnvoll für die Kommunikation mit einem A-SG einen Thread zu starten.

Klar ist, die Identität des Senders wird über das entsprechende Feld im CAN-Frame festgelegt.

Die könnte so ablaufen (Server HMI-SG: S, A-SG: C):
- S erhält die Anfrage (oder Anfänglichen Teil der Anfrage) von C
- S antwortet C mit einem ACK, dass er die Anfrage erhalten hat und nun bearbeiten wird (hierdurch wird C auf Zuhören geschalten)
- (optional weiterer Thread) S wartet auf die Restlichen Teile der Anfrage (falls vorhanden) und bestätigt diese mit einem ACK
- S bearbeitet die Anfrage
- S sendet die Antwort und wartet hierbei auf eine ACK von C für jedes Frame der Antwort


Hierdurch wird eine Unicast verbindung innerhalb eines Multicast netzwerks umgesetzt.
Der unicast Anteil ist rein logisch.
Die Nachrichten werden weiterhin multicast verschickt
Zu diesem Thema gibt es besitmmt eine menge literatur:
-> Forschen
- Doch nicht wie angenommen.


Auch Server und Client State Machines sollte ich mir anschauen.

Wie kann Sender und Empfänger der Unicast Kommunikation festgestellt werden.

Für den Broadcast-Teil ist nur der Sender wichtig.
Welche Bits können verwendet werden?
