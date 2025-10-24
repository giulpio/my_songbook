import os
import webbrowser

# Directory di partenza e nome file
cartella_radice = '.' 
nome_file_html = 'indice_accordi.html'

def genera_intestazione_e_stile():
    """Restituisce l'intestazione HTML con CSS per il responsive design e colonne dinamiche, inclusi stili tondi per il bottone."""
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
            display: none;
            position: relative; 
            padding-top: 35px; /* Spazio per il pulsante in alto */
        }
        
        /* STILE DEL PULSANTE DI CHIUSURA: ORA TONDO */
        .close-btn {
            position: absolute; 
            top: 5px;
            right: 5px;
            background: #e74c3c;
            color: white;
            border: none;
            cursor: pointer;
            
            /* Rende il pulsante tondo e quadrato */
            width: 30px;
            height: 30px;
            line-height: 1; /* Centra verticalmente la 'X' */
            border-radius: 50%; /* Rende il pulsante un cerchio perfetto */
            
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            padding: 0; /* Rimuove il padding predefinito */
            
            /* Assicura che la 'X' sia centrata (usando flexbox per maggiore compatibilità) */
            display: flex; 
            align-items: center; 
            justify-content: center;
            
            z-index: 10; 
        }
        .close-btn:hover {
            background: #c0392b;
        }
        
        pre {
            white-space: pre-wrap;
            font-family: monospace;
            margin: 0;
            font-size: 0.9em;
        }

        /* GESTIONE COLONNE RESPONSIVE CON CSS */
        @media (min-width: 768px) {
            .accordi-box {
                column-count: 2;
                column-gap: 20px;
                column-rule: 1px dotted #ddd;
            }
        }
        
        @media (min-width: 1200px) {
            .accordi-box {
                column-count: 3;
            }
        }
    </style>
</head>
<body>
    <h1>Repertorio Accordi</h1>
"""


def genera_html():
    """Genera la stringa HTML completa del repertorio."""
    
    # Dizionario per memorizzare la struttura: Artista -> Lista di (Nome Canzone, Contenuto Unico)
    repertorio = {}
    
    # 1. Attraversare le cartelle e leggere i file (contenuto non diviso)
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
                    
                    # Salviamo l'intero contenuto
                    canzoni_artista.append((nome_canzone, contenuto_completo))
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
        
        for nome_canzone, contenuto_unico in repertorio[artista]:
            id_canzone = f"accordi-{artista.replace(' ', '_').replace('/', '')}-{nome_canzone.replace(' ', '_').replace('/', '')}"
            
            # Blocco Canzone
            html_content += f'<li class="canzone-container">\n'
            html_content += f'  <a class="canzone-link" onclick="toggleAccordi(\'{id_canzone}\')">{nome_canzone}</a>\n'
            
            # Contenitore degli accordi
            html_content += f'  <div id="{id_canzone}" class="accordi-box">\n'
            
            # AGGIUNTA: Pulsante di chiusura "X" 
            # Il pulsante chiama la stessa funzione toggleAccordi con l'ID per chiudere il proprio box
            html_content += f'    <button class="close-btn" onclick="toggleAccordi(\'{id_canzone}\')">X</button>\n'
            
            html_content += f'    <pre>{contenuto_unico}</pre>\n'
            html_content += f'  </div>\n'
            
            html_content += '</li>\n'
            
        html_content += '</ul>\n'
        html_content += '</div>\n'
        
    # 3. Aggiungere lo script JavaScript e chiudere l'HTML
    html_content += aggiungi_script_js()
    html_content += "</body>\n</html>"

    return html_content

# Le funzioni aggiungi_script_js e salva_e_apri_html rimangono invariate.

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
        
        webbrowser.open(f'file://{os.path.realpath(nome_file_html)}')
        
    except Exception as e:
        print(f"Errore durante la scrittura o apertura del file: {e}")

if __name__ == "__main__":
    contenuto_html_finale = genera_html()
    salva_e_apri_html(contenuto_html_finale)