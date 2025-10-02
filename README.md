# DNS Records Collector

Ce script Python permet de récupérer différents types de records DNS pour une liste de domaines et d'afficher les résultats sous forme de tableau en ligne de commande, ainsi que de générer un fichier CSV.

## Fonctionnalités

- Interrogation des records : `A`, `AAAA`, `CNAME`, `MX`, `TXT` (configurable). 
- Affichage clair en CLI avec couleurs grâce à [Rich](https://github.com/Textualize/rich).  
- Export CSV avec tous les résultats. 
- Traitement parallèle configurable pour accélérer les requêtes. 
- Gestion des timeouts et erreurs de requêtes DNS.  
- Statistiques finales (nombre de domaines avec chaque type de record). 

## Prérequis

- Python 3.8+.  
- [dig](https://linux.die.net/man/1/dig) installé (fait partie du package `dnsutils` sur Linux). 
- Package Python `rich` :

```bash
pip install rich
````

## Utilisation
1.	Créez un fichier domains.txt avec un domaine par ligne :

    ```
    example.com
    google.com
    github.com
    ```

2.	Modifiez éventuellement les paramètres du script :

    ```
    # Nombre de threads pour le traitement parallèle
    workers = 5

    # Colonnes DNS à interroger
    columns_to_show = ["A", "AAAA", "CNAME", "MX", "TXT"]
    ````

3.	Lancez le script :

    ```
    python dns_collector.py
    ```

4.	Résultats :

	•	Tableau en CLI affichant les domaines et leurs records DNS.  
	•	Export CSV dns_records.csv avec les mêmes informations.  
	•	Statistiques récapitulatives à la fin.  

## Personnalisation

•	Pour afficher uniquement certains types de records, modifiez columns_to_show.  
•	Pour changer le nombre de threads, modifiez workers.  

## Exemple de sortie

| Domaine      | A Record        | AAAA Record   | CNAME Record | MX Record               | 
|--------------|-----------------|---------------|--------------|-------------------------|
| example.com  | 93.184.216.34   | -             | -            | 0 mx.example.com        |
| google.com   | 142.250.190.78  | 2607:f8b0:…   | -            | 10 aspmx.l.google.com   |


---

## Licence

Ce projet est libre, vous pouvez le modifier et l’utiliser à votre convenance.
