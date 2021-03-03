import pickle

from rich.progress import track

from load_scholars import search_network, load

df = load()

total_connections = set()
for author in track(df.Name.values[10:16], total=6):
    conns = search_network(author)
    total_connections = total_connections | conns # merge sets

with open('connections.pkl', 'wb') as f:
    pickle.dump(total_connections, f)
