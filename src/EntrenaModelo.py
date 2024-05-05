import joblib
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# Cargar el archivo Excel con las descripciones procesadas
current_directory = os.path.dirname(__file__)
preprocessed_excel_path = os.path.join(current_directory, '..', 'dataset', 'games_processed.xlsx')
df = pd.read_excel(preprocessed_excel_path)

# Eliminar filas con valores np.nan
df = df.dropna(subset=["Descripción procesada"])

# Obtener las descripciones procesadas
descriptions = df["Descripción procesada"].values

# Vectorización de texto utilizando TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(descriptions)

# Entrenar el modelo de clustering (K-means)
num_clusters = 500  # Puedes ajustar este valor según tus necesidades
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Asignar etiquetas de cluster a cada descripción
df["Cluster"] = kmeans.labels_

# Calcular el coeficiente de silueta para evaluar la calidad del clustering
silhouette_avg = silhouette_score(X, kmeans.labels_)
print(f"Coeficiente de silueta: {silhouette_avg}")

joblib.dump(vectorizer, 'vectorizer.pkl')
joblib.dump(kmeans, 'kmeans.pkl')
# Reducción de dimensionalidad con PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X.toarray())

# Graficar los clusters
plt.figure(figsize=(10, 8))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans.labels_, cmap='viridis', s=50, alpha=0.5)
plt.title('Visualización de Clusters')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.colorbar(label='Cluster')
plt.grid(True)
plt.show()

# Guardar el DataFrame con las etiquetas de cluster
clustered_excel_path = os.path.join(current_directory, '..', 'dataset', 'games_clustered.xlsx')
df.to_excel(clustered_excel_path, index=False)
