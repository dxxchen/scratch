import csv
import numpy as np
from k_means_constrained import KMeansConstrained

class Library:
    def __init__(self, name, library_system, latitude, longitude, address, city, zip_code, county, phone):
        self.name = name
        self.library_system = library_system
        self.latitude = float(latitude)  # Convert to float for calculations if needed
        self.longitude = float(longitude)
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.county = county
        self.phone = phone

    def __repr__(self):
        # For clear representation when printing the list
        return f"Library(name='{self.name}', city='{self.city}', ...)" 

def read_libraries_from_csv(filename):
    libraries = []
    with open(filename, 'r', newline='', encoding='utf-8') as file:  # Handle potential encoding issues
        reader = csv.DictReader(file) 
        for row in reader:
            library = Library(
                row['Name'], row['Library System'], row['Latitude'], row['Longitude'],
                row['Address'], row['City'], row['Zip Code'], row['County'], row['Phone']
            )
            libraries.append(library)
    return libraries

def calculate_centroids(libraries):
    centroids = {}
    for library in libraries:
        library_system = library.library_system
        if library_system not in centroids:
            centroids[library_system] = {'latitudes': [], 'longitudes': []}
        centroids[library_system]['latitudes'].append(library.latitude)
        centroids[library_system]['longitudes'].append(library.longitude)

    for library_system, data in centroids.items():
        mean_latitude = np.mean(data['latitudes'])
        mean_longitude = np.mean(data['longitudes'])
        centroids[library_system] = (mean_latitude, mean_longitude)
    return centroids

def cluster_library_systems(centroids, max_cluster_size=20):
    # Extract centroid coordinates
    coords = np.array(list(centroids.values()))

    # Determine the number of clusters
    num_clusters = min(len(coords), len(coords) // max_cluster_size + 1)

    # Apply k-means clustering
    kmeans = KMeansConstrained(n_clusters=num_clusters,size_max=max_cluster_size)
    labels = kmeans.fit_predict(coords)

    # Create the clusters
    clusters = {}
    for i, library_system in enumerate(centroids.keys()):
        cluster_id = labels[i]
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(library_system)

    return clusters

def output_clusters_to_csv(clusters, libraries, output_dir='cluster_outputs'):
    import os
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist
    
    for cluster_id, library_systems in clusters.items():
        filename = os.path.join(output_dir, f'cluster_{cluster_id}.csv')
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            titlenames = ['Name', 'Library System', 'Latitude', 'Longitude', 'Address', 'City', 'Zip Code', 'County', 'Phone']
            fieldnames = ['name', 'library_system', 'latitude', 'longitude', 'address', 'city', 'zip_code', 'county', 'phone']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for library in libraries:
                if library.library_system in library_systems:
                    writer.writerow(library.__dict__)
# Example usage
filename = 'libraries.csv'  # Replace with your actual CSV filename
libraries = read_libraries_from_csv(filename)
centroids = calculate_centroids(libraries)
clusters = cluster_library_systems(centroids)

output_clusters_to_csv(clusters, libraries)

# print(libraries)  # Print the list of Library objects
# print(centroids)
# print("Clustered library systems:")
# for cluster_id, library_systems in clusters.items():
#     print(f"Cluster {cluster_id}: {library_systems}")  
