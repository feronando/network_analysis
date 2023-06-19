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

wikispeedia_network = Network(height="600px", directed=True, width="100%", font_color="black", notebook=True, cdn_resources='remote')

for row in df_articles.iterrows():
  wikispeedia_network.add_node(unquote(row[1]["article"]))
for row in df_links.iterrows():
  wikispeedia_network.add_edge(unquote(row[1]["linkSource"]), unquote(row[1]["linkTarget"]))

adj_list = wikispeedia_network.get_adj_list()
for node in wikispeedia_network.nodes:
  node["title"] = "Links: " + " || ".join(adj_list[node["id"]])
  # node["degree"] = nx.degree(G, node["id"])
  # node["in_degree"] = G.in_degree(node["id"])
  # node["out_degree"] = G.out_degree(node["id"])

wikispeedia_network.show_buttons(filter_=['physics'])
wikispeedia_network.show('wikispeedia.html')

with open("wikispeedia.html", 'r', encoding='utf-8') as html_file:  
  source_code = html_file.read()
  components.html(source_code, height = 1200,width=1000)
