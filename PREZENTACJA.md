# 🎮 Gra Czołgowa 2D - Tank Battle MVP
## Prezentacja Projektu

---

## 📋 Spis Treści

1. [Opis Projektu](#opis-projektu)
2. [Technologie](#technologie)
3. [Architektura Systemu](#architektura-systemu)
4. [Zaimplementowane Funkcjonalności](#zaimplementowane-funkcjonalności)
5. [Mechaniki Gry](#mechaniki-gry)
6. [Struktura Kodu](#struktura-kodu)
7. [Demo i Screenshoty](#demo-i-screenshoty)
8. [Roadmap Rozwoju](#roadmap-rozwoju)
9. [Wnioski](#wnioski)

---

## 🎯 Opis Projektu

**Tank Battle MVP** to klasyczna gra 2D inspirowana Battle City, stworzona w Python z wykorzystaniem Pygame.

### Cele Projektu:
- ✅ Stworzenie funkcjonalnego MVP gry czołgowej
- ✅ Implementacja podstawowych mechanik gameplay
- ✅ Modułowa architektura kodu
- ✅ System kolizji i fizyki pocisków
- ✅ Sztuczna inteligencja przeciwników

### Grupa Docelowa:
- Gracze retro
- Entuzjaści gier arcade
- Developerzy uczący się Pygame

---

## 💻 Technologie

### Główne Narzędzia:
```
🐍 Python 3.12
🎮 Pygame 2.6.1
🪟 Windows OS
```

### Biblioteki:
- **pygame** - silnik gry, grafika, dźwięk
- **random** - losowość AI i strzałów
- **sys** - zarządzanie systemem

### Środowisko:
- **IDE**: Visual Studio Code
- **Kontrola wersji**: Git
- **Python Environment**: venv

---

## 🏗️ Architektura Systemu

### Struktura Modułowa:

```
training/
│
├── main.py                 # Punkt wejścia aplikacji
├── game.py                 # Główna pętla gry
├── settings.py             # Konfiguracja i stałe
│
├── player.py               # Logika gracza
├── enemy.py                # AI przeciwników
├── bullet.py               # Pociski gracza
├── enemy_bullet.py         # Pociski wrogów
├── wall.py                 # System ścian
├── level.py                # Generator map
└── utils.py                # Funkcje pomocnicze
```

### Wzorce Projektowe:
- **Separation of Concerns** - każdy moduł ma jedną odpowiedzialność
- **Entity Component System** - obiekty gry jako encje
- **Game Loop Pattern** - klasyczna pętla gry (update → render)

---

## ✨ Zaimplementowane Funkcjonalności

### ✅ Faza 1 - Podstawy (UKOŃCZONE)
- [x] Gracz (zielony czołg) z ruchem w 4 kierunkach
- [x] Strzelanie pociskami (strzałka w górę)
- [x] Wrogowie (czerwone czołgi) z losowym ruchem
- [x] System kolizji (ściany, pociski)
- [x] Mapa z niezniszczalnymi ścianami (szare)

### ✅ Faza 2 - Rozbudowa (UKOŃCZONE)
- [x] **Strzelający wrogowie** - losowe interwały (60-120 klatek)
- [x] **Zniszczalne ściany** - system zdrowia (3 trafienia)
- [x] Wizualne rozróżnienie ścian (brązowe = zniszczalne)
- [x] Detekcja trafionych ścian
- [x] Usuwanie zniszczonych obiektów

### 🔄 Faza 3 - Planowane
- [ ] Power-upy (przyspieszenie, tarcza, multi-shot)
- [ ] Wiele map/poziomów
- [ ] Zaawansowane AI (pathfinding)
- [ ] Efekty dźwiękowe
- [ ] Menu główne i UI

---

## 🎮 Mechaniki Gry

### Sterowanie Gracza:
```
W / ↑         - Ruch w górę
S / ↓         - Ruch w dół
A / ←         - Ruch w lewo
D / →         - Ruch w prawo
SPACJA        - Strzał
ESC           - Wyjście
```

### System Strzelania:
- **Cooldown**: 20 klatek między strzałami
- **Prędkość pocisku**: 10 pikseli/klatkę
- **Kierunek**: Gracz - w górę, Wrogowie - w dół
- **Limit**: Nieograniczona ilość pocisków na ekranie

### System Ścian:

| Typ | Kolor | Zdrowie | Zniszczalność |
|-----|-------|---------|---------------|
| Granica | Szary (100,100,100) | ∞ | ❌ Nie |
| Wewnętrzna | Brązowy (150,75,0) | 3 HP | ✅ Tak |

### AI Przeciwników:
- **Ruch**: Losowy wybór kierunku co 60 klatek
- **Strzelanie**: Losowy interwał 60-120 klatek
- **Detekcja zablokowania**: Zmiana kierunku po 30 klatkach
- **Kolizje**: Odbicie od ścian i innych czołgów

---

## 🧩 Struktura Kodu

### Główne Klasy:

#### 🎮 **Game** (game.py)
```python
class Game:
    - __init__()        # Inicjalizacja gry
    - run()             # Główna pętla
    - update()          # Aktualizacja stanu
    - render()          # Renderowanie grafiki
    - handle_events()   # Obsługa inputu
```

#### 👤 **Player** (player.py)
```python
class Player:
    - handle_input()    # Sterowanie WSAD
    - shoot()           # Tworzenie pocisków
    - update()          # Aktualizacja stanu
    - render()          # Rysowanie czołgu
```

#### 👾 **Enemy** (enemy.py)
```python
class Enemy:
    - move()            # Losowy ruch
    - shoot()           # Strzelanie co 60-120 klatek
    - change_direction()# Zmiana kierunku AI
    - update()          # Aktualizacja stanu
```

#### 🧱 **Wall** (wall.py)
```python
class Wall:
    - __init__(destructible, health)
    - take_damage()     # Redukcja HP
    - render()          # Rysowanie z kolorem
```

---

## 📸 Demo i Screenshoty

### Widok Rozgrywki:

```
╔════════════════════════════════════╗
║ ████████████████████████████████  ║
║ █     👾        👾        👾    █  ║
║ █  ▓▓▓  ▓▓▓  ▓▓▓  ▓▓▓  ▓▓▓    █  ║
║ █                               █  ║
║ █  ▓▓▓  ▓▓▓  ▓▓▓  ▓▓▓  ▓▓▓    █  ║
║ █                               █  ║
║ █  ▓▓▓  ▓▓▓  ▓▓▓  ▓▓▓  ▓▓▓    █  ║
║ █                               █  ║
║ █            🟢 (gracz)         █  ║
║ ████████████████████████████████  ║
╚════════════════════════════════════╝

Legenda:
🟢 - Gracz (zielony czołg)
👾 - Wrogowie (czerwone czołgi)
█  - Niezniszczalne ściany (szare)
▓  - Zniszczalne ściany (brązowe, 3 HP)
```

### Statystyki Mapy:
- **Rozmiar**: 800x600 pikseli (20x15 kafelków)
- **Rozmiar kafelka**: 40x40 pikseli
- **Liczba wrogów**: 10
- **Liczba ścian**: ~90 (granice + wewnętrzne)

---

## 🚀 Roadmap Rozwoju

### Faza 3 - Power-upy (Q4 2025)
- [ ] Speed Boost - zwiększenie prędkości
- [ ] Shield - tarcza na 3 trafienia
- [ ] Multi-Shot - strzał w 3 kierunkach
- [ ] Rapid Fire - zmniejszenie cooldownu

### Faza 4 - Progression (Q1 2026)
- [ ] System poziomów (1-10)
- [ ] Zwiększająca się trudność
- [ ] Boss fights co 5 poziomów
- [ ] Zapisywanie postępów

### Faza 5 - Polish (Q2 2026)
- [ ] Efekty dźwiękowe (strzały, wybuchy)
- [ ] Muzyka w tle
- [ ] Animacje zniszczeń
- [ ] Particle effects
- [ ] Menu główne z opcjami

### Faza 6 - Multiplayer (Q3 2026)
- [ ] Tryb 2 graczy (local)
- [ ] Co-op mode
- [ ] Competitive mode
- [ ] Online leaderboards

---

## 📊 Metryki Projektu

### Linie Kodu:
```
player.py        : ~120 linii
enemy.py         : ~150 linii
game.py          : ~130 linii
bullet.py        : ~60 linii
enemy_bullet.py  : ~60 linii
wall.py          : ~50 linii
level.py         : ~80 linii
settings.py      : ~30 linii
utils.py         : ~20 linii
─────────────────────────
TOTAL            : ~700 linii
```

### Złożoność:
- **Moduły**: 9
- **Klasy**: 7
- **Funkcje**: ~40
- **Stałe konfiguracyjne**: 15+

---

## 🐛 Rozwiązane Problemy

### Problem 1: Pociski Niewidoczne
**Symptom**: Pociski gracza znikały natychmiast po wystrzeleniu

**Przyczyna**: Podwójna aktualizacja w `game.py` - pociski były aktualizowane 2x na klatkę

**Rozwiązanie**: 
```python
# USUNIĘTO duplikat:
# for bullet in self.player.bullets[:]:
#     bullet.update(self.walls)
```

### Problem 2: Ściany Się Nie Niszczyły
**Symptom**: Trafienia w ściany nie powodowały ich zniszczenia

**Przyczyna**: Modyfikacja listy `walls` podczas iteracji + brak propagacji zmian

**Rozwiązanie**:
1. Zmiana zwracanej wartości z `bool` na `tuple(bool, Wall)`
2. Zbieranie ścian do usunięcia w `walls_to_remove[]`
3. Usuwanie po zakończeniu iteracji

### Problem 3: Gracz Nie Może Się Ruszyć
**Symptom**: Gracz zablokowany we wszystkich kierunkach

**Przyczyna**: Spawn position (y=540) + wysokość (40) = 580 > dolna ściana (560)

**Rozwiązanie**:
```python
# Zmiana z:
Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)  # y=540
# Na:
Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100) # y=500
```

---

## 🎓 Wnioski i Lekcje

### Sukcesy ✅
1. **Modułowa architektura** - łatwe dodawanie nowych funkcji
2. **System kolizji** - precyzyjny i wydajny
3. **Debug logging** - szybkie wykrywanie błędów
4. **Iteracyjny rozwój** - MVP → Faza 1 → Faza 2

### Wyzwania 🎯
1. **Synchronizacja stanu** - propagacja zmian między modułami
2. **Lifecycle management** - prawidłowe usuwanie obiektów
3. **Collision detection** - optymalizacja dla wielu obiektów
4. **AI behavior** - balans między prostotą a inteligencją

### Best Practices 📚
1. **Zawsze testuj po małych zmianach**
2. **Używaj debug logów liberalnie**
3. **Nie modyfikuj list podczas iteracji**
4. **Validuj pozycje spawn przed utworzeniem encji**
5. **Rozdziel logikę od renderowania**

---

## 🔮 Przyszłe Kierunki

### Krótkoterminowe (1-3 miesiące)
- Dodanie efektów dźwiękowych
- Implementacja power-upów
- System punktacji i high scores
- Menu główne

### Średnioterminowe (3-6 miesięcy)
- Wiele poziomów
- Zaawansowane AI (A* pathfinding)
- Animacje i particle effects
- Boss fights

### Długoterminowe (6-12 miesięcy)
- Tryb multiplayer (local + online)
- Campaign mode z fabułą
- Level editor
- Steam release

---

## 👥 Zespół i Kontakt

### Developer:
- **Łukasz Kamiński** - Full Stack Developer

### Stack:
- Python 3.12
- Pygame 2.6.1
- VS Code
- Git

### Repozytorium:
```
📂 c:\Users\lukasz.kaminski\OneDrive - Accenture\
   Documents\Projects\work\Twillio\training\
```

---

## 📝 Licencja i Użycie

### Licencja: MIT
- ✅ Użytek komercyjny
- ✅ Modyfikacje
- ✅ Dystrybucja
- ✅ Użytek prywatny

### Wymagania:
- Zachowanie informacji o licencji
- Brak gwarancji

---

## 🙏 Podziękowania

- **Pygame Community** - za świetną dokumentację
- **Battle City (1985)** - za inspirację
- **Accenture** - za wsparcie projektowe

---

## 📞 Q&A

### Często Zadawane Pytania:

**Q: Jak uruchomić grę?**
```bash
python main.py
```

**Q: Jakie są wymagania systemowe?**
- Python 3.12+
- Pygame 2.6.1+
- 50 MB RAM
- Dowolny procesor z 2010+

**Q: Czy będzie wersja mobilna?**
Obecnie nie, ale jest to rozważane w przyszłości.

**Q: Jak dodać własne mapy?**
Edytuj tablicę w `level.py` - używaj:
- `0` = pusta przestrzeń
- `1` = niezniszczalna ściana
- `2` = zniszczalna ściana

---

## 🎬 Dziękuję za Uwagę!

### Kontakt:
📧 lukasz.kaminski@accenture.com
💼 LinkedIn: [Łukasz Kamiński]
🐙 GitHub: [Projekt Tank Battle]

---

### Pytania?

