from pyvis.network import Network
import networkx as nx
import pandas as pd
from IPython.display import display, HTML
import matplotlib.pyplot as plt
import nxviz as nv
import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import unquote

st.title('Wikispeedia Network')

df_articles = pd.read_csv('https://raw.githubusercontent.com/feronando/network_analysis/main/wikispeedia_paths-and-graph/articles.tsv', skiprows=11, names=["article"])
df_links = pd.read_csv('https://raw.githubusercontent.com/feronando/network_analysis/main/wikispeedia_paths-and-graph/links.tsv', encoding='utf-8', sep="\t", skiprows=12, names=["linkSource", "linkTarget"])

G = nx.DiGraph()
for row in df_articles.iterrows():
  G.add_node(unquote(row[1]["article"]), category=[])

for row in df_categories.iterrows():
  G.nodes[unquote(row[1]["article"])]["category"].append(unquote(row[1]["category"]))

for row in df_links.iterrows():
  G.add_edge(unquote(row[1]["linkSource"]), unquote(row[1]["linkTarget"]))

for n, d in G.nodes(data=True):
  G.nodes[n]["degree"] = nx.degree(G, n)
  G.nodes[n]["in_degree"] = G.in_degree(n)
  G.nodes[n]["out_degree"] = G.out_degree(n)

scc = list(nx.strongly_connected_components(G))
subgraph = G.subgraph(sorted(scc, key=lambda n : len(n), reverse=True)[0])

wikispeedia_network_subgraph = Network(height="600px", directed=True, width="100%", font_color="black", notebook=True, cdn_resources='remote')
wikispeedia_network_subgraph.from_nx(subgraph)

adj_list = wikispeedia_network_subgraph.get_adj_list()
for node in wikispeedia_network_subgraph.nodes:
  node["title"] = "Links: " + " || ".join(adj_list[node["id"]])
  # node["degree"] = nx.degree(G, node["id"])
  # node["in_degree"] = G.in_degree(node["id"])
  # node["out_degree"] = G.out_degree(node["id"])

wikispeedia_network_subgraph.show_buttons(filter_=['physics'])
wikispeedia_network_subgraph.show('wikispeedia_network_subgraph.html')

with open("wikispeedia_network_subgraph.html", 'r', encoding='utf-8') as html_file:  
  source_code = html_file.read()
  components.html(source_code, height = 1200,width=1000)
