# Taktische-Zeichen-drawio
Bibliotheken für draw.io mit taktischen Zeichen des Bevölkerungsschutzes.

Das Auswahl und Gruppierung der taktischen Zeichen orientiert sich an dem [Empfehlungen für Taktische Zeichen im Bevölkerungsschutz des BBK](http://www.bbk.bund.de/SharedDocs/Downloads/BBK/DE/FIS/DownloadsRechtundVorschriften/Volltext_Fw_Dv/SKK_DV_102_2012.html)

![Vorschau](https://github.com/MartinBoehmer/Taktische-Zeichen-drawio/raw/master/preview.PNG)

## Nutzung
Die Bibliotheken können mit der ![öffentlichen Variante von draw.io](https://www.draw.io/) und dem ![draw.io Confluence Plugin](https://marketplace.atlassian.com/plugins/com.mxgraph.confluence.plugins.diagramly/server/overview) verwendet werden.

### draw.io
Die Bibliotheken können auf zwei Wege eingebunden werden:
- per URL der Bibliotheksdateien aus diesem Projekt (Unterordner libs)
- durch Hochladen einer lokalen (und ggf. angepassen) Kopie der Bibliotheksdateien

Das Vorgehen ist simpel:
1. draw.io öffnen
2. File -> Open Library from -> URL / Device

### draw.io Confluence Plugin
1. Bibliotheksdateien (Unterordner libs) herunterladen
2. draw.io-Zeichnung im Bearbeitungsmodus öffnen
3. File -> New library
4. Import
5. Eine heruntergeladene Bibliotheksdatei auswählen
6. Titel der Bibliothek anpassen
(im Feld "Filename", der Wert wird leider nicht aus dem Dateinamen der hochgeladenen Datei übernommen)
7. Speichern

## Fehlende Zeichen
Dieses Projekt nutzt die ![taktischen Zeichen von Jonas Köritz](https://github.com/jonas-koeritz/Taktische-Zeichen) und transformiert sie zu draw.io Bibliotheken. Fehlende Zeichen sollten daher dem referenzierten Projekt hinzugefügt werden. Details finden sich auf dessen Webseite.

## Anpassung & Generierung

### Setup
Um die Generierung der Bibliotheken selbstständig vorzunehmen und anzupassen, sind folgende Schritte erforderlich:
1. Clonen dieses Projektes
2. Clonen des Projektes mit den Symbolen:
Dafür kommen das ![Original-Projekt](https://github.com/jonas-koeritz/Taktische-Zeichen) oder ![der Fork](https://github.com/MartinBoehmer/Taktische-Zeichen) in Frage. Das Original-Projekt stellt den aktuellsten Entwicklungsstand der taktischen Zeichen dar. Daher kann es mitunter inkompatibel zum Stand dieses Projektes sein. Der Fork hingegen ist immer kompatibel zum Stand dieses Projektes.
3. Pfade konfigurieren:
Das Skript zur Generierung muss den Pfad zu dem Projekt mit dem Grafikdateien für die taktischen Zeichnen kennen. Dieser ist in der Datei `tz-drawio.ini` in der Property `images.basedir` festgelegt. Standardmäßig wird erwartet, dass sich die unter 1. und 2. geclonten Projekte "nebeneinander" in einem Ordner befinden. Also, z.B. `/home/jdoe/TZ/Taktische-Zeichen` und `/home/jdoe/TZ/Taktische-Zeichen-drawio`.
4. Generierung aufrufen:
`python generate-libs.py`

### Konfiguration
Die Auswahl, Gruppierung und Beschriftung der taktischen Zeichen und der Bibliotheken ist in der Datei `tz-drawio.ini` konfiguriert. Der erste Abschnitt `SETTINGS` steuert die Generierung. Alle weiteren Abschnitte werden als Bibliothek interpretiert. Ein solcher Abschnitt besteht aus dem relativen Pfad der SVG-Datei als Schlüssel und der Beschriftung des Zeichens als Wert. Der Name des Abschnitts wird als Titel und Dateiname der Bibliothek übernommen.

## Lizenz / License

Copyright 2017 Martin Böhmer

Licensed under the Apache License, Version 2.0 (the "License"); you may not use these files except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
