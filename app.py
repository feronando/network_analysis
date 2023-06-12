from pyvis.network import Network
import networkx as nx
import pandas as pd
from IPython.display import display, HTML
import matplotlib.pyplot as plt
import nxviz as nv
import streamlit as st
import streamlit.components.v1 as components

st.title('The Marvel Universe Social Network')

df_edges = pd.read_csv('https://raw.githubusercontent.com/feronando/network_analysis/main/hero-network.csv')
G = nx.Graph()
for row in df_edges.iterrows():
  G.add_edge(row[1]["hero1"], row[1]["hero2"])

hero_network = Network(height="600px", width="100%", notebook=True, font_color="black", heading='Hero Network', cdn_resources='remote')
hero_network.from_nx(G)

adj_list = hero_network.get_adj_list()
for node in hero_network.nodes:
  node["title"] = " Neighbors:<br>" + "<br>".join(adj_list[node["id"]])
  node["value"] = len(adj_list[node["id"]])

hero_network.show_buttons(filter_=['physics'])
hero_network.show('hero_network.html')

with open("hero_network.html", 'r', encoding='utf-8') as html_file:  
  source_code = html_file.read()
  components.html(source_code, height = 1200,width=1000)
