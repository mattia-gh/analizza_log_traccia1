from griglia_di_liste_RO import Tabella2D_RO
import json
from datetime import datetime
import argparse

def count_idf_in_tabella2d_ro(t2d_ro_file: Tabella2D_RO, s) -> int:
    """ conta il numero di accessi di un utente in base all'identificativo """
    return t2d_ro_file.get_colonna(1).count(s)

def save_json_log_in_tabella2d_ro(json_file) -> Tabella2D_RO:
    """ funzione che permette di salvare i log in formato json in una tabella RO """
    #tenta di aprire il file in modalità lettura
    try:   
        fin = open(json_file, 'r')
        data = json.load(fin)
        fin.close()
        return Tabella2D_RO(data)
    
    #se il file non esiste ritorna una tabella vuota
    except FileNotFoundError:
        print(f"ERRORE: Il file '{json_file}' non è stato trovato.")
        return Tabella2D_RO([])
    
    #se il file non è un JSON valido ritorna una tabella vuota
    except json.JSONDecodeError as e:
        print(f"ERRORE: Il file '{json_file}' non è un JSON valido.")
        print(f"Dettaglio dell'errore: {e}")
        if fin:
            fin.close()
            print("Risorsa file chiusa dopo errore JSON.")
        return Tabella2D_RO([])

def save_tabella2d_ro_in_dict(t2d_ro_file: Tabella2D_RO) -> dict:
    """ la funzione permette di salvare da una tabella RO
        in un dizionario per ogni utente (avrà come key l'identificativo dell'utente):
        - data e ora del primo accesso (primo elemento)
        - data e ora dell'ultimo accesso (secondo elemento)
        - numero di accessi (terzo elemento) """
    new_dict = {}
    formato = "%d/%m/%Y %H:%M"                                   #formato data e ora coerente  
    for i in range(len(t2d_ro_file.get_colonna(0))):
        idf = t2d_ro_file.get_riga(i)[1]
        num_access = count_idf_in_tabella2d_ro(t2d_ro_file, idf) #conta il numero di accessi
        if idf not in new_dict.keys():                           #se l'dentificativo non è presente tra le chiavi del nuovo dizionario
                                                                 #vengono settati primo-ultimo e numeri accesso
            first_access = t2d_ro_file.get_riga(i)[0]
            last_access = t2d_ro_file.get_riga(i)[0]
            new_dict[idf] = [first_access, last_access ,num_access]
        else:                                                    #altrimenti viene effettuato un controllo solo su primo-ultimo accesso
            try:
                if datetime.strptime(str(t2d_ro_file.get_riga(i)[0]), formato)<datetime.strptime(new_dict[idf][0], formato):
                    new_dict[idf][0]=t2d_ro_file.get_riga(i)[0]
                if datetime.strptime(str(t2d_ro_file.get_riga(i)[0]), formato) > datetime.strptime(new_dict[idf][1], formato):
                    new_dict[idf][1] = t2d_ro_file.get_riga(i)[0]
            except ValueError as e:                              #se il formato non è valido stampo l'errore e salto alla riga successiva
                print(f"{i} - ERRORE: str:'{str(t2d_ro_file.get_riga(i)[0])}', dict:'{new_dict[idf][0]}' {e}")
                continue
    return new_dict

if __name__ == '__main__':
    # Inizializzazione del parser
    parser = argparse.ArgumentParser(description="Script per l'analisi del primo-ultimo e nuemeri di accesso.")
    # Definizione delle flag -i e -o
    # 'required=True' rende obbligatorio l'inserimento anche se sono flag
    parser.add_argument("-i", "--input", required=True, help="Percorso del file JSON di input")
    parser.add_argument("-o", "--output", required=True, help="Percorso del file JSON di output")
    args = parser.parse_args()
    input_file = args.input
    output_file = args.output
    t = save_json_log_in_tabella2d_ro(input_file)
    print("File salvato in una Tabella2D_RO\n--------")
    d = save_tabella2d_ro_in_dict(t)
    print("Tabella2D_RO salvata in una dizionario di liste con specifiche indicate\n--------")
    fout = open(output_file, 'w')
    json.dump(d, fout, indent=3)
    fout.close()
    print("Dizionario salvato in json")

    



