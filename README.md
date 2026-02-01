# 

Autó típusok alap adatait feldolgozó oldal

## Fő funkciók

-  **Lokális adatbázisban tárol néhány (~40) autó adatot**
-  **Kódban előre megadva kilistáz 15 autó mellyek adatait megjeleníti egy táblázatban.**
-  **Eme adatokhoz lehet hozzáadni továbbá törölni belőlük.**
-  **Tartozik a megjelenített adatokhoz egy grafikon is melyben hengerűrtalom szerint lehet megtekinteni az autókat.**
-  **Az oldal alján egy újdonságokat megjelenítő szekcióban a motor1.com oldal legfrissebb hírei tekinhetők meg**

## Telepítés és futtatás
### Virtuális környezet létrehozása
``` bash
CREATE_venv.bat
```
> [!NOTE]
> Ez a script létrehoz egy venvet majd telepíti a kelő függőségeket.

### Futtatás

1. Backend
``` bash
START_backend.bat
```
> [!NOTE]
> Elindít egy Uvicorn szervert ami a FastAPI működéséhez kell.

2. Frontend
``` bash
START_frontend.bat
```
> [!NOTE]
> Elindít egy Streamlit webes felületet.

## Használt technológiák

-   **Python 3**
-   **FastAPI** -- REST backend
-   **Uvicorn** -- ASGI szerver
-   **Streamlit** -- frontend webes felület
-   **requests + BeautifulSoup** -- web scraping
-   **SqLite** -- Adatbázis
