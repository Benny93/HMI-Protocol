# Bilder Erklärung

## Test: Trennung der Anfragen durch die App-SGs
![2Apps10Req](2Apps10Req_EqualResponseTime.png)
Grafik zeigt, wie die Zugriffe auf das HMI-SG verteilt sind.  
Hierbei stellten die SG ihre 10 Anfragen direkt hintereinander.  
![2Apps10ReqNoSleep](2Apps10Req_NoSleepHmi.png)
Gleicher versuch ohne künstliche Bearbeitungszeit des HMI-SG durch Sleep  
![2Apps10Rq](2Apps10Req_Sleep3.png)
Hier haben die Apps nach jeder beantworteten Anfrage 1 Sekunde lang geschlafen.  
Hierdurch wird ein ineinandergreifen der Anfragen ermöglicht.  
Diese 1 Sekunde kann als Bearbeitungszeit der A-SG angesehen werden.  
![3Apps10Req](3Apps10Req.png)
3 Apps stellen zeitgleich eine Request.
Wird ihre Request beantwortet, schlafen sie 1 Sekunde.
Hierdruch können Anfragen überlappen.
Die Wahrscheinlichkeit einer Überlappung hängt vom Timeout der A-SG-Anfragen ab.
