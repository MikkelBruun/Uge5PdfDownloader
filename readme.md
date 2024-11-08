# PDF downloader

## Anvendelse

Scriptet kan lettest køres via:
`python downloadFromSheet.py`
Det antager at der i samme mappe ligger `GRI_2017_2020.xlsx`.
Resultatet vil være en ny mappe, `files`, hvor de downloadede filer ligger, samt et ny ark `GRI_2017_2020_Downloaded.xlsx`, hvor en ny kolonne "Downloaded" indikerer hvorvidt en fil er downloaded.

For flere muligheder læs scriptets "usage" besked ved at køre `python downloadFromSheet.py -h`.

Min anbefaling er at bruge `python downloadFromSheet.py -l -p`, da det gemmer ekstra information i `logs` mappen, uden at forstyrre brugeren yderligere.

## Ydeevne

### Update mode

Hvis der gives et ark som allerede har en kolonne ved navn "Downloaded" køres programmet i updatMode. Dvs at rækker med en "Downloaded" værdi på "success" bliver sprunget over, og det opdaterede data skrives direkte tilbage til input arket.

### Multithreading

Scriptet kører nu over flere tråde. Som udgangspunkt laver den så man tråde som python vurderer, baseret på maskinens cpu.

Rækkerne bliver behandlet af en threadpool, som derefter sætter dem sammen til en liste af resultater (Success/Error) som skrives til et excel ark.

Ydeevne kan måles med konsolflaget `-p`, som skriver tiderne ned i `logs/performance.log`. Nye resultater skrives på enden af filen, så man nemmere kan sammenligne flere eksekveringer over længere tid.
