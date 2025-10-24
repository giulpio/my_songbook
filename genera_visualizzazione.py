import os
import webbrowser

# Directory di partenza (la cartella in cui viene eseguito lo script)
cartella_radice = '.' 
# Nome del file HTML da creare
nome_file_html = 'indice_accordi.html'

def genera_html():
    """Genera la stringa HTML completa del repertorio."""
    
    # Dizionario per memorizzare la struttura: Artista -> Lista di (Nome Canzone, Contenuto 1, Contenuto 2, Contenuto 3)
    repertorio = {}
    
    # 1. Attraversare le cartelle e leggere i file, splittando il contenuto
    for root, dirs, files in os.walk(cartella_radice):
        if root == cartella_radice:
            continue
            
        nome_artista = os.path.basename(root)
        canzoni_artista = []
        
        for nome_file in files:
            if nome_file.lower().endswith('.txt'):
                nome_canzone = os.path.splitext(nome_file)[0]
                percorso_file = os.path.join(root, nome_file)
                
                try:
                    with open(percorso_file, 'r', encoding='utf-8') as f:
                        contenuto_completo = f.read()
                    
                    # Suddividi il contenuto in righe
                    righe = contenuto_completo.splitlines()
                    
                    # Calcola i punti di divisione per 3 colonne (circa 1/3 e 2/3 delle righe)
                    lunghezza_totale = len(righe)
                    punto_di_divisione_1 = lunghezza_totale // 3
                    punto_di_divisione_2 = (lunghezza_totale * 2) // 3
                    
                    # Ricomponi le tre colonne
                    colonna_1 = '\n'.join(righe[:punto_di_divisione_1])
                    colonna_2 = '\n'.join(righe[punto_di_divisione_1:punto_di_divisione_2])
                    colonna_3 = '\n'.join(righe[punto_di_divisione_2:])
                    
                    # Salviamo i tre contenuti separati
                    canzoni_artista.append((nome_canzone, colonna_1, colonna_2, colonna_3))
                except Exception as e:
                    print(f"Errore nella lettura del file {percorso_file}: {e}")
        
        if canzoni_artista:
            repertorio[nome_artista] = sorted(canzoni_artista) 
            
    # 2. Generare la parte del corpo HTML
    html_content = genera_intestazione_e_stile()
    
    artisti_ordinati = sorted(repertorio.keys())
    
    for artista in artisti_ordinati:
        html_content += f'<div class="artista">\n'
        html_content += f'<h2>{artista}</h2>\n'
        html_content += '<ul>\n'
        
        for nome_canzone, colonna_1, colonna_2, colonna_3 in repertorio[artista]: # AGGIUNTA colonna_3
            id_canzone = f"accordi-{artista.replace(' ', '_').replace('/', '')}-{nome_canzone.replace(' ', '_').replace('/', '')}"
            
            # Blocco Canzone
            html_content += f'<li class="canzone-container">\n'
            html_content += f'  <a class="canzone-link" onclick="toggleAccordi(\'{id_canzone}\')">{nome_canzone}</a>\n'
            
            # Contenitore degli accordi, ora con tre colonne interne
            html_content += f'  <div id="{id_canzone}" class="accordi-box">\n'
            html_content += f'    <div class="col-1"><pre>{colonna_1}</pre></div>\n'
            html_content += f'    <div class="col-2"><pre>{colonna_2}</pre></div>\n'
            html_content += f'    <div class="col-3"><pre>{colonna_3}</pre></div>\n' # NUOVA COLONNA
            html_content += f'  </div>\n'
            
            html_content += '</li>\n'
            
        html_content += '</ul>\n'
        html_content += '</div>\n'
        
    # 3. Aggiungere lo script JavaScript e chiudere l'HTML
    html_content += aggiungi_script_js()
    html_content += "</body>\n</html>"

    return html_content

# --- Le funzioni genera_intestazione_e_stile, aggiungi_script_js, salva_e_apri_html sono definite sotto ---

def genera_intestazione_e_stile():
    """Restituisce l'intestazione HTML con CSS per il responsive design."""
    return """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Repertorio Accordi</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #f4f4f4; }
        h1 { color: #333; text-align: center; }
        .artista { 
            margin-bottom: 30px; 
            padding: 15px; 
            border: 1px solid #ddd; 
            border-radius: 8px; 
            background-color: #fff;
        }
        h2 { color: #555; border-bottom: 2px solid #ccc; padding-bottom: 5px; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 10px 0; }
        .canzone-link { 
            text-decoration: none; 
            color: #007bff; 
            font-weight: bold; 
            cursor: pointer;
            display: block;
        }
        .canzone-link:hover { text-decoration: underline; color: #0056b3; }
        .accordi-box {
            border: 1px dashed #ccc;
            padding: 10px;
            margin-top: 5px;
            background-color: #f9f9f9;
            display: none; /* Inizialmente nascosto */
            overflow: auto; 
        }
        /* Stile di base per le colonne (100% di larghezza per schermi piccoli) */
        .col-1, .col-2, .col-3 {
            padding: 0 10px;
            box-sizing: border-box;
            width: 100%; 
            float: none; 
            min-height: 1px; /* Per gestire i margini vuoti */
        }
        pre {
            white-space: pre-wrap;
            font-family: monospace;
            margin: 0;
            font-size: 0.9em;
        }
        
        /* === MEDIA QUERY per schermi Medi (es. tablet orizzontale) === */
        /* Su schermi medi, usiamo 2 colonne */
        @media (min-width: 768px) {
            .col-1, .col-2 {
                width: 50%; 
                float: left;
            }
            .col-3 {
                width: 100%; /* La terza colonna va sotto */
                float: none;
            }
            /* Separatori per 2 colonne */
            .col-1 { border-right: 1px dotted #ddd; }
            .col-2 { border-right: none; }
        }

        /* === MEDIA QUERY per schermi Grandi (es. desktop) === */
        /* Su schermi molto grandi, usiamo 3 colonne */
        @media (min-width: 1200px) {
            .col-1, .col-2, .col-3 {
                width: 33.33%; /* Suddividi in tre colonne */
                float: left; /* Metti uno accanto all'altro */
            }
            /* Separatori per 3 colonne */
            .col-1, .col-2 { border-right: 1px dotted #ddd; }
            .col-3 { border-right: none; }
        }
    </style>
</head>
<body>
    <h1>Repertorio Accordi</h1>
"""

def aggiungi_script_js():
    """Restituisce lo script JavaScript per la funzionalità toggle."""
    return """
    <script>
        function toggleAccordi(id) {
            var box = document.getElementById(id);
            if (box.style.display === 'none' || box.style.display === '') {
                box.style.display = 'block';
            } else {
                box.style.display = 'none';
            }
        }
    </script>
"""

def salva_e_apri_html(contenuto_html):
    """Salva il contenuto HTML in un file e lo apre nel browser."""
    try:
        with open(nome_file_html, 'w', encoding='utf-8') as f:
            f.write(contenuto_html)
            
        print(f"File '{nome_file_html}' creato con successo.")
        
        # Apri il file nel browser predefinito
        webbrowser.open(f'file://{os.path.realpath(nome_file_html)}')
        
    except Exception as e:
        print(f"Errore durante la scrittura o apertura del file: {e}")

if __name__ == "__main__":
    contenuto_html_finale = genera_html()
    salva_e_apri_html(contenuto_html_finale)