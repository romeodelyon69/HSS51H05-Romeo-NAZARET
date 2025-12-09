import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# =============================================================================
# 1. CONFIGURATION
# =============================================================================

DATA_FOLDER = 'data'
FILE_PATTERN = os.path.join(DATA_FOLDER, "Experience2*.xpd")

# =============================================================================
# 2. FONCTIONS DE LECTURE
# =============================================================================

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
            # On a besoin d'au moins 9 colonnes
            if len(parts) >= 9:
                try:
                    
                    # Col 2 (Index 1) : Numéro de la forme
                    shape_id = parts[1] 
                    # Col 4 (Index 3) : Condition ('same', 'same_topo', 'diff_topo' ou 'default')
                    condition = parts[3] 
                    # Col 8 (Index 7) : Temps de réponse
                    rt = float(parts[7])
                    # Col 9 (Index 8) : Précision (0 ou 1)
                    acc = int(parts[8])
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



# =============================================================================
# 3. ANALYSE ET GRAPHIQUE
# =============================================================================

# Chargement
all_files = glob.glob(FILE_PATTERN)
print(f"Fichiers trouvés : {len(all_files)}")

full_data = []
for f in all_files:
    full_data.extend(parse_custom_xpd(f))

df = pd.DataFrame(full_data)

if not df.empty:
    print(f"Total essais : {len(df)}")
    print(f"Formes identifiées : {df['ShapeID'].unique()}")
    
    # Filtrage RT
    df = df[df['RT'] <= 10000]
    
    # Renommage des conditions pour l'affichage
    # Note: 'default' correspond généralement à la condition 'same' (identique)
    # ou 'diff_topo' selon comment le fichier est généré.
    # Dans votre fichier exemple: 
    # 'default' est utilisé pour l'objet identique (réponse s)
    # 'diff_topo' pour topologie différente (réponse d)
    # 'same_topo' pour même topologie (réponse d)
    
    df['Condition_Label'] = df['Condition'].map({
        'diff_topo_rel': 'Topologie\nDifférente',
        'same_topo_rel': 'Même\nTopologie',
        # On peut ignorer 'default'/'same' car ce n'est pas la comparaison d'intérêt
        # mais on le laisse au cas où vous voudriez vérifier
    })

    # Sélection des conditions d'intérêt (Comparaison Topologique)
    subset = df[df['Condition'].isin(['diff_topo_rel', 'same_topo_rel'])].copy()

    # --- AGRÉGATION PAR FORME (ITEM ANALYSIS) ---
    # Au lieu de grouper par 'Subject', on groupe par 'ShapeID'
    # On calcule la moyenne de précision et de temps de réponse pour chaque forme à travers tous les sujets
    shape_means = subset.groupby(['ShapeID', 'Condition_Label'])[['Accuracy', 'RT']].mean().reset_index()

    # --- GRAPHIQUES RT & ACCURACY CÔTE À CÔTE ---
    order = ['Même\nTopologie', 'Topologie\nDifférente']
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # --- RT (gauche) ---
    ax_rt = axes[0]
    pivot_rt = shape_means.pivot(index='ShapeID', columns='Condition_Label', values='RT')
    print("pivot_rt:", pivot_rt)
    if all(col in pivot_rt.columns for col in order):
        for _, row in pivot_rt.iterrows():
            ax_rt.plot([0, 1], [row[order[0]], row[order[1]]], color='gray', alpha=0.6, linewidth=1.5, zorder=1)
    for condition_idx, condition in enumerate(order):
        condition_data = shape_means[shape_means['Condition_Label'] == condition]
        rt_values = condition_data['RT'].values
        x_vals = [condition_idx] * len(rt_values)
        ax_rt.scatter(x_vals, rt_values, color='black', s=80, zorder=2)
    ax_rt.set_title("Temps de réponse", fontweight='bold')
    ax_rt.set_ylabel("RT moyen (ms)")
    ax_rt.set_xticks([0, 1], order)
    ax_rt.set_ylim(0, shape_means['RT'].max() + 500)
    ax_rt.grid(True, alpha=0.3, axis='y')

    # --- ACCURACY (droite) ---
    ax_acc = axes[1]
    pivot_acc = shape_means.pivot(index='ShapeID', columns='Condition_Label', values='Accuracy')
    if all(col in pivot_acc.columns for col in order):
        for _, row in pivot_acc.iterrows():
            ax_acc.plot([0, 1], [row[order[0]], row[order[1]]], color='gray', alpha=0.6, linewidth=1.5, zorder=1)
    for condition_idx, condition in enumerate(order):
        condition_data = shape_means[shape_means['Condition_Label'] == condition]
        acc_values = condition_data['Accuracy'].values
        x_vals = [condition_idx] * len(acc_values)
        ax_acc.scatter(x_vals, acc_values, color='black', s=80, zorder=2)
    ax_acc.set_title("Précision", fontweight='bold')
    ax_acc.set_ylabel("Accuracy moyenne")
    ax_acc.set_xticks([0, 1], order)
    ax_acc.set_ylim(0, 1.05)
    ax_acc.grid(True, alpha=0.3, axis='y')

    fig.suptitle("Performance par Forme (Item Analysis)", fontweight='bold')
    fig.tight_layout()
    plt.show()

    # --- STATISTIQUES ---
    print("\n--- RÉSULTATS PAR FORME ---")
    print(pivot_acc)
    print(pivot_rt)

else:
    print("Aucune donnée chargée.")