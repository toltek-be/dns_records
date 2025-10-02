import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.table import Table
from rich.console import Console
import csv

# fichiers
filename = "domains.txt"
output_csv = "dns_records.csv"

# Nombre de workers pour le traitement en parallèle
workers = 5

# Colonnes DNS à interroger et afficher
# ["A", "AAAA", "CNAME", "MX", "TXT"]
columns_to_show = ["A", "AAAA", "CNAME", "TXT"] 

def get_dns_records(domain, record_type):
    """Retourne une liste des records pour un type donné"""
    try:
        result = subprocess.run(
            ["dig", "+short", domain, record_type],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return lines if lines else ["-"]
    except subprocess.TimeoutExpired:
        return ["Timeout"]
    except subprocess.CalledProcessError:
        return ["Erreur"]

def process_domain(domain):
    """Récupère les records sélectionnés pour un domaine"""
    row = [domain]  # première colonne = domaine
    for record_type in columns_to_show:
        records = ", ".join(get_dns_records(domain, record_type))
        row.append(records or "-")
    return row

def main():
    console = Console()
    table = Table(title="DNS Records")

    # colonnes
    table.add_column("Domaine", style="cyan", no_wrap=True)
    for record_type in columns_to_show:
        style = "green" if record_type=="A" else \
                "magenta" if record_type=="AAAA" else \
                "yellow" if record_type=="CNAME" else \
                "blue" if record_type=="MX" else \
                "bright_blue"
        table.add_column(f"{record_type} Record", style=style)

    # lecture des domaines
    with open(filename) as f:
        domains = [line.strip() for line in f if line.strip()]

    results = []

    # traitement en parallèle
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_domain = {executor.submit(process_domain, d): d for d in domains}
        for future in as_completed(future_to_domain):
            row = future.result()
            table.add_row(*row)
            results.append(row)

    console.print(table)

    # export CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Domaine"] + [f"{col} Record" for col in columns_to_show])
        writer.writerows(results)

    # résumé statistique
    total = len(results)
    console.print("\n📊 Résumé statistique :", style="bold yellow")
    console.print(f"Total domaines : {total}")
    for i, col in enumerate(columns_to_show, start=1):
        count = sum(1 for r in results if r[i] != "-")
        console.print(f"Domaines avec {col} record : {count}")
    console.print(f"\n✅ Export CSV terminé : {output_csv}", style="bold green")

if __name__ == "__main__":
    main()