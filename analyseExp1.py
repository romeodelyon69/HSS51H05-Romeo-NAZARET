import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


DATA_FOLDER = 'data'
FILE_PATTERN = os.path.join(DATA_FOLDER, "Experience1-b*.xpd")

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

        # Filtrer commentaires et lignes vides
        content_lines = [line.strip() for line in lines if not line.startswith('#') and line.strip()]
        
        # Ignorer la première ligne (header subject_id)
        if len(content_lines) > 1:
            data_rows = content_lines[1:]
        else:
            return []

        for row in data_rows:
            parts = row.split(',')
            # On a besoin d'au moins 10 colonnes
            if len(parts) >= 10:
                try:
                    
                    # Col 2 (Index 1) : Numéro de la forme
                    shape_id = parts[1] 
                    # Col 4 (Index 3) : Condition ('same', 'same_topo', 'diff_topo' ou 'default')
                    condition = parts[3] 
                    # Col 8 (Index 8) : Temps de réponse
                    rt = float(parts[8])
                    # Col 9 (Index 9) : Précision (0 ou 1)
                    acc = int(parts[9])
                    raw_data.append({
                        'ShapeID': shape_id,   # Identifiant de la forme
                        'Condition': condition,
                        'RT': rt,
                        'Accuracy': acc
                    })
                except ValueError:
                    continue
    except Exception as e:
        print(f"Erreur lecture {filepath}: {e}")
        
    return raw_data

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
    
    df['Condition_Label'] = df['Condition'].map({
        'diff_topo': 'Topologie\nDifférente',
        'same_topo': 'Même\nTopologie',
    })
    
    subset = df[df['Condition'].isin(['diff_topo', 'same_topo'])].copy()
    
    shape_means = subset.groupby(['ShapeID', 'Condition_Label'])[['Accuracy', 'RT']].mean().reset_index()
    

    # --- GRAPHIQUE ---
    plt.figure(figsize=(8, 6))
    
    order = ['Même\nTopologie', 'Topologie\nDifférente']
    
    pivot = shape_means.pivot(index='ShapeID', columns='Condition_Label', values='RT')
    
    if all(col in pivot.columns for col in order):
        for idx, row in pivot.iterrows():
            # On trace la ligne
            plt.plot([0, 1], [row[order[0]], row[order[1]]], 
                     color='gray', alpha=0.6, linewidth=1.5, zorder=1)

    x_positions = [0, 1]
    for condition_idx, condition in enumerate(order):
        condition_data = shape_means[shape_means['Condition_Label'] == condition]
        rt_values = condition_data['RT'].values
        x_vals = [condition_idx] * len(rt_values)
        plt.scatter(x_vals, rt_values, color='black', s=80, zorder=2)

    plt.title("Performance par Forme (Item Analysis)", fontweight='bold')
    plt.ylabel("Temps de Réponse Moyen (ms)")
    plt.xlabel("")
    plt.xticks([0, 1], order)
    plt.ylim(0, shape_means['RT'].max() + 500)
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()

    print("\n--- RÉSULTATS PAR FORME ---")
    print(pivot)

else:
    print("Aucune donnée chargée.")