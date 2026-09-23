# Roadmap und To-do

Stand: v1.0.0. Die folgenden Punkte beschreiben geplante Funktionen; sie sind noch nicht implementiert. Umfang und Reihenfolge können sich während der Entwicklung ändern.

## Nächster Schritt: Bonus-Grundsystem

- [ ] Bonusobjekte mit Position, Darstellung, Kollision mit dem Schiff und Bildschirmgrenzen einführen.
- [ ] Drops nach zerstörten Asteroiden mit konfigurierbarer Wahrscheinlichkeit und begrenzter Anzahl gleichzeitig sichtbarer Boni.
- [ ] Aktive Effekte und verbleibende Ladungen bzw. Laufzeiten im HUD anzeigen; beim Neustart zuverlässig zurücksetzen.
- [ ] Ablauf von Boni bei Pause, Levelwechsel, Tod und Fenstergrößenänderung festlegen und umsetzen.
- [ ] Kollisionen, Aufsammeln und Effektende gezielt testen.

## Erste Boni

### Bombe

- [ ] Als einsammelbare Ladung verfügbar machen und eine eigene Auslösetaste festlegen (Vorschlag: `B`).
- [ ] Eine klar sichtbare Explosion mit einstellbarem Radius und einmaliger Auslösung umsetzen.
- [ ] Getroffene Asteroiden über denselben Punkte- und Teilungsmechanismus wie Lasertreffer verarbeiten; Mehrfachtreffer derselben Explosion verhindern.
- [ ] Maximale Ladungen und Drop-Rate so abstimmen, dass Wellen weiterhin eine Herausforderung bleiben.

### Multishot / Splitshot

- [ ] Zeitlich begrenzten Effekt zum Einsammeln anbieten.
- [ ] Beim Schießen mehrere Projektile mit definiertem Winkelabstand erzeugen (Vorschlag: drei Schüsse: Mitte und ±15°).
- [ ] Geschossreichweite, Geschwindigkeit und Sound bei aktivem Effekt prüfen.
- [ ] Verhalten beim erneuten Einsammeln definieren (Vorschlag: Dauer erneuern, nicht unbegrenzt stapeln).

## Weitere mögliche Boni

- [ ] Schild mit begrenzter Dauer oder genau einem abgefangenen Treffer.
- [ ] Schnellfeuer mit Schussabstand und Begrenzung gleichzeitiger Projektile.
- [ ] Zusätzliche Lebenspunkte oder ein kontrollierter Respawn mit kurzer Unverwundbarkeit.

## Qualität und Feinschliff

- [ ] Spielparameter wie Drop-Raten, Effektdauer und Explosionradius zentral konfigurieren.
- [ ] Bonus-Sprites und Effektsounds ergänzen; Lesbarkeit bei verschiedenen Fenstergrößen prüfen.
- [ ] Ausgewählte Spielregeln automatisiert testen, insbesondere kombinierte Treffer und Levelabschluss.
- [ ] Abhängigkeiten und Start auf Windows, macOS und Linux prüfen; bei Bedarf ein ausführbares Paket erstellen.
