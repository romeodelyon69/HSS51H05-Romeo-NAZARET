import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


DATA_FOLDER = 'data'
FILE_PATTERN = os.path.join(DATA_FOLDER, "Experience3*.xpd")

def parse_custom_xpd(filepath):
    """
    Lit le fichier selon vos spécifications :
    - Ignore #
    - Ignore la ligne de header
    - Colonne 2 (Index 1) : SetID (Forme)
    - Colonne 4 (Index 3) : Condition
    - Colonne 8 (Index 8) : RT
    - Colonne 9 (Index 9) : Accuracy
    """
    raw_data = []
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        content_lines = [line.strip() for line in lines if not line.startswith('#') and line.strip()]
        
        if len(content_lines) > 1:
            data_rows = content_lines[1:]
        else:
            return []

        for row in data_rows:
            parts = row.split(',')
            if len(parts) >= 10:
                try:
                    
                    # Col 3 (Index 2) : Numéro de la forme
                    shape_id = parts[2] 
                    # Col 4 (Index 3) : Nombre de formes à gauche
                    nbLeftShape = int(parts[3]) 
                    # Col 5 (Index 4) : Nombre de formes à droite
                    nbRightShape = int(parts[4])
                    # #Col 6 : (Index 5) : LeftTopology
                    left_topo = parts[5]
                    # #Col 7 : (Index 6) : RightTopology
                    right_topo = parts[6]
                    # Col 9(Index 8) : Temps de réponse
                    rt = float(parts[8])
                    # Col 10(Index 9) : A choisi le côté complexe
                    choseComplex = int(parts[9])
                    # Col 11 (Index 10) : Précision (0 ou 1 et -1 si =, les deux réponses sont ok)
                    acc = int(parts[10])
                    raw_data.append({
                        'ShapeID': shape_id,   # Identifiant de la forme
                        'nbLeftShape': nbLeftShape,
                        'nbRightShape': nbRightShape,
                        'left_topo': left_topo,
                        'right_topo': right_topo,
                        'choseComplex': choseComplex,
                        'RT': rt,
                        'Accuracy': acc
                    })
                except ValueError:
                    continue
    except Exception as e:
        print(f"Erreur lecture {filepath}: {e}")
        
    return raw_data

# =============================================================================
# 3. ANALYSE ET GRAPHIQUE
# =============================================================================

all_files = glob.glob(FILE_PATTERN)
print(f"Fichiers trouvés : {len(all_files)}")

full_data = []
for f in all_files:
    full_data.extend(parse_custom_xpd(f))

df = pd.DataFrame(full_data)

if not df.empty:
    print(f"Total essais : {len(df)}")
    print(f"Formes identifiées : {df['ShapeID'].unique()}")
    
    df = df[df['RT'] <= 10000]

    df['pair'] = df.apply(lambda r: tuple(sorted([r['nbLeftShape'], r['nbRightShape']])), axis=1)

    agg = df.groupby('pair')['choseComplex'].mean().reset_index()
    agg['Pourcentage_Complex'] = agg['choseComplex'] * 100

    print("\n--- Pourcentage de choix du côté complexe par paire (ordre ignoré) ---")
    print(agg[['pair', 'Pourcentage_Complex']])

    print("df head:", df.head())

    fig, ax = plt.subplots(figsize=(8, 5))
    x_positions = range(len(agg))
    labels = [f"{a}-{b}" for a, b in agg['pair']]
    ax.bar(x_positions, agg['Pourcentage_Complex'], color='steelblue')

    ax.axhline(50, color='red', linestyle='--', linewidth=1.5, label='Réalité 50%')
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(labels)
    ax.set_ylabel("% choix du côté complexe (Topologie en T)")
    ax.set_xlabel("Paire (nb gauche - nb droite, ordre ignoré)")
    ax.set_ylim(0, 100)
    ax.set_title("Choix du côté complexe par paire de numerosité")
    ax.legend()
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.show()
    

else:
    print("Aucune donnée chargée.")