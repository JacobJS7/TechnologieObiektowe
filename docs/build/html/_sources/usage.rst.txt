Użytkowanie
===========

Uruchamianie aplikacji
----------------------

1. Po sklonowaniu możesz uruchomić aplikację:

.. code-block:: bash

   python src/main.py

Podstawowe operacje
-------------------

Importowanie danych GPS
~~~~~~~~~~~~~~~~~~~~~~

- Kliknij "Plik" → "Importuj"
- Wybierz plik z danymi GPS zapisany przez dedykowane urządzenie

Wyświetlanie danych
~~~~~~~~~~~~~~~~~~~

- Mapa wyświetli Twoją trasę z kolorami w zależności od prędkości:

  - Zielone odcinki: Prędkość w normie
  - Czerwone odcinki: Prędkość przekroczona   

- Kliknij na punkty w lewym panelu, aby zobaczyć szczegóły
- Dolny panel pokazuje szczegóły wybranego punktu

Generowanie wykresów
~~~~~~~~~~~~~~~~~~~~

- Kliknij menu "Wykresy" i wybierz jeden z dostępnych wykresów:

  - "Wykres prędkości" - wykres prędkości
  - "Wykres wysokości npm" - wykres wysokości
  - "Wykres dokładności HDOP" - wykres dokładności HDOP
  - "Wykres ilości satelit" - wykres liczby satelitów
  - "Wykres napięcia baterii" - wykres napięcia baterii

Eksport mapy
~~~~~~~~~~~~

- Kliknij "Plik" → "Eksportuj"
- Wybierz lokalizację do zapisania pliku HTML

Format danych
-------------

Aplikacja oczekuje danych GPS w plikach tekstowych w następującym formacie rozdzielanym średnikami:

.. code-block::

   time;date;latitude;longitude;altitude;course;speed;satellites;hdop;voltage

Gdzie:

- ``time``: Czas rejestracji punktu GPS
- ``date``: Data rejestracji punktu GPS
- ``latitude``, ``longitude``: Współrzędne geograficzne
- ``altitude``: Wysokość nad poziomem morza w metrach
- ``course``: Kierunek w stopniach
- ``speed``: Prędkość w km/h
- ``satellites``: Liczba połączonych satelitów
- ``hdop``: Wskaźnik dokładności HDOP
- ``voltage``: Napięcie baterii w mV