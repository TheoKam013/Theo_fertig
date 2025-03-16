
# Erforderliche Bibliotheken erneut importieren
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Datei erneut hochladen (da sie im Speicher verloren ging)
file_path = "data_clean/ufo_sightings_scrubbed_clean.csv"  # Ursprünglicher Upload-Pfad

# Datei einlesen und Spaltennamen bereinigen
df = pd.read_csv(file_path, low_memory=False)
df.columns = df.columns.str.strip()  # Entfernt überflüssige Leerzeichen aus Spaltennamen

# Umbenennen der Spalte "duration (seconds)" in "duration_seconds" für eine einfachere Handhabung
df.rename(columns={"duration (seconds)": "duration_seconds"}, inplace=True)

# Sicherstellen, dass die Spalte "duration_seconds" als ganze Zahl gespeichert wird
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce").fillna(0).astype(int)

# **Längste Sichtungen: Orte & Tageszeiten**
df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
df["hour"] = df["datetime"].dt.hour  # Uhrzeit extrahieren

# Top 100 längste Sichtungen
top_sightings = df.nlargest(100, "duration_seconds")[["city", "state", "country", "duration_seconds", "hour"]]

# Anzeigen 
print("\n Top 100 längste UFO-Sichtungen:")
print(top_sightings.to_string(index=False))

# Feinanpassung des Histogramms der Sichtungsdauer
plt.figure(figsize=(14, 8))  # Größere Abmessungen für vollständige Darstellung
ax = sns.histplot(df["duration_seconds"], bins=30, kde=False, color="royalblue")

# Werte auf die Balken schreiben mit 90° Drehung
for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.text(p.get_x() + p.get_width() / 2, height + 1, f'{int(height)}',
                ha='center', va='bottom', fontsize=10, color="black", fontweight="bold", rotation=90)

plt.xlim(0, df["duration_seconds"].max() + 1)  # Sicherstellen, dass Balken exakt auf 0 beginnen
plt.ylim(0, ax.get_ylim()[1] * 1.1)  # Y-Achsen-Skalierung für bessere Darstellung
plt.xlabel("Sichtungsdauer (Sekunden)")
plt.ylabel("Anzahl der Sichtungen")
plt.title("Verteilung der UFO-Sichtungsdauer")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", linewidth=0.7)
plt.tight_layout()  # Stellt sicher, dass nichts abgeschnitten wird
plt.savefig("histogram_sichtungsdauer.png")

# Feinanpassung des Balkendiagramms für Shapes
shape_durations = df.groupby("shape")["duration_seconds"].median().sort_values(ascending=False).reset_index()
plt.figure(figsize=(16, 10))  # Größer für vollständige Sichtbarkeit
ax = sns.barplot(data=shape_durations, x="shape", y="duration_seconds", palette="coolwarm")

# Werte auf die Balken schreiben mit 90° Drehung
for index, value in enumerate(shape_durations["duration_seconds"]):
    ax.text(index, value + 1, f"{int(value)} s", ha="center", va="bottom", rotation=90, fontsize=10, color="black")

plt.xticks(rotation=75, ha='right')
plt.xlabel("Shape")
plt.ylabel("Mittlere Sichtungsdauer (Sekunden)")
plt.title("Mittlere Sichtungsdauer pro Shape in Sekunden")
plt.grid(True, linestyle="--", linewidth=0.7)
plt.tight_layout()  # Stellt sicher, dass nichts abgeschnitten wird
plt.savefig("balkendiagramm_shapes.png")

# Feinanpassung der Tageszeit-Analyse
plt.figure(figsize=(14, 8))  # Größer für bessere Darstellung
ax = sns.histplot(df[df["duration_seconds"] > df["duration_seconds"].quantile(0.95)]["hour"], bins=24, kde=False, color="royalblue", discrete=True)

# Werte auf die Balken schreiben mit 90° Drehung
for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.text(p.get_x() + p.get_width() / 2, height + 1, f'{int(height)}',
                ha='center', va='bottom', fontsize=10, color="black", fontweight="bold", rotation=90)

plt.xlim(-0.5, 23.5)
plt.ylim(0, ax.get_ylim()[1] * 1.1)
plt.xlabel("Tageszeit (Stunde)")
plt.ylabel("Anzahl langer Sichtungen")
plt.title("Wann treten lange Sichtungen auf?")
plt.xticks(range(0, 24))
plt.grid(True, linestyle="--", linewidth=0.7)
plt.tight_layout()  # Stellt sicher, dass nichts abgeschnitten wird
plt.savefig("histogram_tageszeit.png")

# Bereinigte Datei speichern
df.to_csv(file_path, index=False)
print(f"✅ Datei erfolgreich gespeichert unter: {file_path}")
