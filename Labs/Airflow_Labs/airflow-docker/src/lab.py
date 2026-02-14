import pandas as pd
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from kneed import KneeLocator

def load_data(**kwargs):
    """
    Load data from CSV file and return it
    """
    print("Loading data...")
    
    # Load the iris dataset (you can replace with your own CSV)
    data = pd.read_csv('/opt/airflow/data/iris.csv')
    
    print(f"Data loaded successfully. Shape: {data.shape}")
    print(f"Columns: {data.columns.tolist()}")
    
    # Serialize and return data
    serialized_data = pickle.dumps(data)
    return serialized_data


def data_preprocessing(serialized_data, **kwargs):
    """
    Preprocess the data: deserialize, select features, and scale
    """
    print("Preprocessing data...")
    
    # Deserialize data
    data = pickle.loads(serialized_data)
    
    # Select only numeric columns (remove species/labels if present)
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    data_numeric = data[numeric_columns]
    
    print(f"Selected numeric columns: {numeric_columns.tolist()}")
    
    # Standardize the features
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_numeric)
    
    print("Data preprocessing completed")
    
    # Serialize and return
    serialized_preprocessed = pickle.dumps(data_scaled)
    return serialized_preprocessed


def build_save_model(serialized_data, filename, **kwargs):
    """
    Build K-Means models with different k values and save the best model
    Returns SSE values for elbow method
    """
    print("Building and saving model...")
    
    # Deserialize data
    data = pickle.loads(serialized_data)
    
    # Test different numbers of clusters (k)
    sse_values = []
    k_range = range(1, 11)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(data)
        sse_values.append(kmeans.inertia_)
        print(f"K={k}, SSE={kmeans.inertia_:.2f}")
    
    # Save a model with k=3 as default (you can change this)
    final_model = KMeans(n_clusters=3, random_state=42, n_init=10)
    final_model.fit(data)
    
    # Save the model to working_data directory
    model_path = f'/opt/airflow/working_data/{filename}'
    with open(model_path, 'wb') as f:
        pickle.dump(final_model, f)
    
    print(f"Model saved to {model_path}")
    
    # Return SSE values for elbow method
    serialized_sse = pickle.dumps(sse_values)
    return serialized_sse


def load_model_elbow(filename, serialized_sse, **kwargs):
    """
    Load the saved model and determine optimal number of clusters using elbow method
    """
    print("Loading model and finding optimal clusters...")
    
    # Load the model
    model_path = f'/opt/airflow/working_data/{filename}'
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print(f"Model loaded from {model_path}")
    print(f"Model has {model.n_clusters} clusters")
    
    # Deserialize SSE values
    sse_values = pickle.loads(serialized_sse)
    
    # Find the elbow point
    k_range = range(1, 11)
    kn = KneeLocator(k_range, sse_values, curve='convex', direction='decreasing')
    
    optimal_k = kn.elbow
    print(f"\nOptimal number of clusters (Elbow Method): {optimal_k}")
    print(f"SSE values: {sse_values}")
    
    result = {
        'optimal_k': optimal_k,
        'sse_values': sse_values,
        'model_clusters': model.n_clusters
    }
    
    print(f"\nResult: {result}")
    return result