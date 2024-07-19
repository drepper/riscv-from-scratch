# Schreiben Sie Ihren ersten RISC-V-Simulator

Author: Ulrich Drepper[drepper@akkadia.org](mailto:drepper@akkadia.org)[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Dieses Repository enthält die Anfänge eines ersten RISC-V-Simulators. Es ist nicht vollständig, es bietet nur eine
Startpunkt.  Die vorhandene Funktionalität implementiert das Kompilieren von Testfällen und das Laden dieser in die Simulation
Speicher und Übergabe der Kontrolle an einen vom Benutzer bereitgestellten Speicher**real**Simulator.

Die Aufgabe besteht darin, in der Klasse eine funktionale Simulation zu schreiben`MySimulator`im`myriscv.py`Datei.  Eine Simulation
Objekt basierend auf der Klasse wird erstellt und das`run()`Methode wird aufgerufen.`step()`ist erhältlich als
Alternative zum Single-Stepping, diese Methode wird hier jedoch nicht verwendet.

Die Simulation betrifft nur den Userspace-Teil der RISC-V ISA.  Das heißt, sobald das Programm das verwendet`ecall`Anweisung kann die Simulation gestoppt werden.  Dies ist das erwartete Verhalten für die Programme in[Testsuite](https://github.com/riscv/riscv-tests.git).

## Vorbereitungen

Um Ihre Änderungen übernehmen zu können, müssen Sie einen Fork dieses Repositorys erstellen und ihn lokal klonen.
Gehen Sie zum Projekt[Seite des Repositorys](https://github.com/drepper/riscv-from-scratch)auf GitHub und klicken Sie auf den „Fork“
Taste.  Dann lokal in einer Shell in einem Verzeichnis ausführen, das für den Quellcode gedacht ist:

```bash
git clone --recurse-submodules https://github.com/<your-username>/riscv-from-scratch.git
```

Hier`<your-username>`ist Ihr GitHub-Benutzername.  Dadurch wird eine lokale Kopie des Repositorys erstellt und auch alles abgerufen
Submodule.

Außerdem muss die RISC-V-Toolchain auf unserem System installiert sein.  Der folgende Befehl sollte das tun
auf einem Fedora-System:

```bash
sudo dnf install gcc-c++-riscv64-linux-gnu
```

## Fehlende Bits

Der gesamte zusätzliche Code geht in die`myriscv.py`Datei.  Der vorhandene Code ist nur ein Ausgangspunkt.  Natürlich
Darf jeder den neuen Code in mehrere neue Dateien aufteilen?  Stellen Sie einfach sicher, dass alles korrekt geladen wird.

Der`CPUState` class has three methods that need to be implemented for the testing framework to assess the result
of the simulation:

-   `get_register(reg)`: Gibt den Wert eines Registers mit dem Namen zurück`reg`.  Beachten Sie, dass RISC-V-Ganzzahlregister mehrere haben
    Namen.  Alle sollten unterstützt werden, aber das Framework verwendet`a0`,`a7`, Und`gp`.
-   `is_ecall()`: Gibt zurück, ob die letzte ausgeführte Anweisung eine war`ecall`.  Simulation eines`ecall`Anweisung
    sollte die Simulation stoppen und die Implementierung sollte zu diesem Zeitpunkt feststellen können, ob`ecall`War
    die letzte auszuführende Anweisung.
-   `__str__()`: Gibt eine Zeichenfolgendarstellung des CPU-Status zurück.  Dies ist nützlich für das Debuggen mithilfe von Einzelschritten
    und nach jeder Anweisung den Zustand der CPU betrachten.

## Verwendung

Die RISC-V ISA-Testsuite deckt alle grundlegenden Anweisungen auf ziemlich gründliche Weise ab.  Die Tests sind weiter
gruppiert nach der Erweiterung der ISA, die sie eingeführt hat.  Die Grundtests finden Sie im`i`Erweiterung und sie
sollten zunächst implementiert und getestet werden.

| Name | Beschreibung |
  \+:----:|:----------- |
  \|`i`| Grundlegende Anweisungen |
  \|`m`| Multiplikation und Division |
  \|`a`| Atomanweisungen |
  \|`f`| Gleitkomma mit einfacher Genauigkeit |
  \|`d`| Gleitkomma mit doppelter Genauigkeit |
  \|`c`| Komprimierte Anleitung |
  \|`zba`| Anweisungen zur Adressgenerierung |
  \|`zbb`| Grundlegende Anweisungen zur Bitmanipulation |
  \|`zbc`| Anleitung zur Carryless-Multiplikation |
  \|`zbs`| Einzelbit-Anweisungen |
  \|`zfh`| Gleitkommaanweisungen mit halber Genauigkeit |

Alle außer dem`i`Die Erweiterung ist optional.  Zusätzliche Anweisungen sollten möglicherweise in der Reihenfolge ausgeführt werden, in der sie ausgeführt werden
erscheinen in der Tabelle, dies ist jedoch nicht unbedingt erforderlich.  Es gibt einige Abhängigkeiten zwischen Erweiterungen (z. B.`d`Und`zfh`hängen davon ab`f`Erweiterung), aber ansonsten sollte sich jeder frei fühlen, das Problem so anzugehen, wie er möchte.

Alle verfügbaren Tests für die implementierten Erweiterungen sollten ausgeführt werden, um sicherzustellen, dass die Implementierung tatsächlich erfolgt
richtig.  Alle Tests können im 32-Bit- oder 64-Bit-Modus ausgeführt werden.

Um einen einzelnen Test auszuführen, verwenden Sie:

```bash
./run_riscv_test.py 64 i add
```

Sobald die Simulation abgeschlossen ist, wird der aktuelle Zustand der CPU untersucht, um festzustellen, ob der Test bestanden wurde oder
fehlgeschlagen.

## Erste Schritte

Wie fange ich an, fragen Sie sich?

Ein guter Ausgangspunkt ist die Wikipedia-Seite auf[Unterrichtszyklus](https://en.wikipedia.org/wiki/Instruction_cycle).
Es erklärt die Grundschleife einer einfachen CPU-Implementierung.  Die meisten CPUs folgen heutzutage grundsätzlich diesem Muster
auf viel komplexere und verworrenere und parallelere Weise.

Als nächstes ist es notwendig, die Grundlagen des RISC-V-Befehlssatzes zu kennen.  Band 1 des[RISC-V-Befehlssatzhandbuch](https://riscv.org/specifications/)ist hier revelent.  Wir beschäftigen uns (noch) nicht mit der Systemprogrammierung, also
Band 2 kann vorerst ignoriert werden.

Nach der Lektüre von Kapitel 1 ist es, wie oben erläutert, am besten, mit der Implementierung und dem Testen zu beginnen`i`Verlängerung
wird in Kapitel 2 erklärt. Die 64-Bit-Variante wird in Kapitel 7 erklärt. Es könnte sinnvoll sein, das zu implementieren`i`Zuerst die Erweiterung für beide Größen, bevor Sie mit den anderen Erweiterungen fortfahren.  Der Grund dafür ist, dass dies eine ergibt
Gelegenheit zu lernen, wie man die Implementierung für diese Breite vereinheitlicht.  Den Code einlesen`pysim_riscv.py`Du
kann sehen, dass die`Simulation`Das Objekt hat einen Member namens`xlen` which is the common name used throughout the ISA
manual to differentiate between 32-bit and 64-bit variants.  Use this member variable instead of any hardcoded
values in your code.

Der`c`Die Erweiterung eröffnet eine neue Dimension.  Es ermöglicht das Komprimieren (daher`c`Erweiterung) der Binärcode von
Kodierung häufig verwendeter Anweisungen mit nur 16 Bit.  Dies führt zu einer Komplexität der Anweisungen
Die Ausrichtung auf 32-Bit-Adressen ist nicht mehr garantiert.  In diesem reinen Python ist das kein großes Problem
Implementierung, aber eine effiziente Implementierung unter Verwendung einer Hardwarebeschreibungssprache ist kompliziert
wie Verilog oder VHDL (oder sogar höhere Sprachen wie Chisel oder NMigen).

## Programmierstil

Der vorhandene Code verwendet Codeanmerkungen.  Sie tun zur Ausführungszeit nichts anderes als statische Analysatoren, einschließlich
Diejenigen, die implizit von IDEs wie VsCodium ausgeführt werden, können die Informationen nutzen und sofortiges Feedback geben.
Es wird dringend empfohlen, diese Praxis weiterhin zu befolgen.

Zusätzlich kann der Stil mit überprüft werden

```bash
pylint --rcfile pylint.conf run_riscv_test.py
```

und ähnlich für die anderen Python-Dateien.  Der ausgewählte Stil ist voreingenommen und jeder sollte sich dazu frei fühlen
Passen Sie es wie gewünscht an.

## Was kommt als nächstes?

Die Implementierung dieses Simulators vermittelt ein gutes Verständnis der RISC-V ISA und führt Sie auch in die ein
Grundsätze der Unterrichtsausführung.  Dies kann dann verwendet werden, um dieselbe CPU mithilfe eines HDL zu implementieren, oder vielleicht,
um den Aufwand zu verringern, in NMigen, das ebenfalls auf Python basiert.  Ein NMigen-Design kann auf einem FPGA ausgeführt werden und könnte
theoretisch sogar zu ASICs synthetisiert werden.

Eine andere Richtung wäre die Implementierung eines einfachen Compilers, der RISC-V-Code aus einer Hochsprache generiert.
Dies ermöglicht es dann, den gesamten Schritt von höheren Programmiersprachen bis zu den darin enthaltenen Signalen zu sehen
CPU beim Ausführen der Anweisungen.  Dies kann dann dazu führen, dass über Optimierungen nachgedacht und diese umgesetzt werden
sowohl den generierten Code als auch die CPU-Implementierung selbst.

## Im Falle von Fehlern

Dateifehler/Probleme auf[GitHub](https://github.com/drepper/riscv-from-scrath/issues).
