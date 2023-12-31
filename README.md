
<div class="cell markdown">

# Networks of Painters: Creating links between painters, styles, and art movements based on the PainterPalette dataset

This project aims to understand the connections between painters and art styles. Originally, this included creating a painter dataset, but this evolved into a seperate project called [PainterPalette](https://github.com/me9hanics/PainterPalette). These notebooks use the PainterPalette dataset, creating links between painters based on similarity of style, geographical and social interaction, and also connections between styles and movements.

There have been multiple networks created by us of painters (based on being at the same places at the same time+nationality, additionally style similarity, or who influenced whom networks). We also created a network of styles and movements.

Some visualizations of the resulting networks:

* Time-and-place network:<br>

![image](https://github.com/me9hanics/ArtProject/assets/82604073/7690b7fc-b46e-4e27-ae98-7aa8bc046dc5)

This was turned into a dynamic network and time passes along the horizontal axis, painters are aligned according to their birth year. This network was built by creating connections between painters if they painted at the same places roughly at the same time, filtering just for strong connections.

* Movement network:<br>

![image](https://github.com/me9hanics/ArtProject/assets/82604073/039688be-16f0-4432-bae2-acba9688914b)

* InfluencedOn network:<br>

![image](https://github.com/me9hanics/ArtProject/assets/82604073/fe2c11b3-0386-4655-857e-37e0632aa6d9)

* A map of most common styles in the dataset in different countries:<br>

![image](https://github.com/me9hanics/ArtProject/assets/82604073/e56890d3-95f0-4b34-899f-60d9d7500cc8)

* 3D plot of painters-styles-movements:<br>

![image](https://github.com/me9hanics/ArtProject/assets/82604073/585fd608-79c3-4313-8eaf-5c6cc1ebb082)

* Time-and-place network without reordering nodes based on time:<br>

![image](https://github.com/me9hanics/ArtProject/assets/82604073/9eb4be59-245d-4cdb-a210-7c6c5ada3c5b)

(One can see the clusters of movements despite not connecting painters based on style similarities.)

# Dataset:

We created our own dataset called Painter Palette: a dataset with ~2500 painters (so far), data on their styles, movements, nationality, birthyear, first and last year of painting in the Art500k dataset, birthplace, places of their paintings, influences, friends and coworkers, teachers. It's created by assembling data from paintings from the Art500k dataset, and data from paintings from the WikiArt dataset, with some manual additions. This dataset is available in the [PainterPalette](https://github.com/me9hanics/PainterPalette) repository.

</div>

<div class="cell markdown">

## WikiArt data


<div class="cell code" execution_count="21">

``` python
import pandas as pd
import numpy as np
```

</div>

</div>

<div class="cell markdown">

Load the cleaned paintings data

</div>

<div class="cell code" execution_count="3">

</div>

<div class="output execute_result" execution_count="11">

                  style        artist       movement  count
    2963  Impressionism  Claude Monet  Impressionism   1341
    5468        Realism  Claude Monet  Impressionism     12
    7042        Unknown  Claude Monet  Impressionism     12
    462     Academicism  Claude Monet  Impressionism      1
    3339       Japonism  Claude Monet  Impressionism      1

</div>

</div>

<div class="cell markdown">

## Art500K

</div>

<div class="cell markdown">

First dataset (from official website)

</div>

<div class="cell code" execution_count="23">

``` python
art500k = pd.read_csv('datasets/art500k_cleaned.csv')
art500k[0:6]
```

<div class="output stream stderr">

      art500k = pd.read_csv('datasets/art500k_cleaned.csv')

</div>

<div class="output execute_result" execution_count="23">

           author_name                                      painting_name Genre      Style Nationality PaintingSchool ArtMovement           Date Influencedby        Influencedon  Tag Pupils                                         Location        Teachers FriendsandCoworkers      Teachers FriendsandCoworkers 
    0  Gustave Courbet                Woman With A Parrot##AAHozJAL0gqXcA   NaN      NaN         NaN            NaN         NaN            NaN          NaN                   NaN  NaN    NaN                    in a settlement in Palestine in the middle east                     NaN              NaN            NaN
    1    Auguste Rodin         La Tentation Saint Antoine##WAGC82imJTDyIg   NaN      NaN         NaN            NaN         NaN            NaN          NaN      
    2      Frida Kahlo   Retrato De Alejandro Gómez Arias##0QFuguLe4xyN_A   NaN      NaN         NaN            NaN         NaN            NaN          NaN 
    3           Banksy           The Wall Banksy Balloons##FgHoVE-hmt6DBQ   NaN      NaN         NaN            NaN         NaN            NaN          NaN 
    4         El Greco                     The Visitation##HQEQ_qXDtRrzkA   NaN      NaN         NaN            NaN         NaN  ca. 1610-1614          NaN 
    5         El Greco  Madonna And Child With Saint Martina And Saint...   NaN      NaN         NaN            NaN         NaN            NaN          NaN 


</div>

</div>

<div class="cell code" execution_count="30">

``` python
art500k_artists = pd.read_csv('save.csv')
art500k_artists[0:10]
```

<div class="output execute_result" execution_count="30">

                artist    Nationality                      PaintingSchool                                               ArtMovement                                              Influencedby                                              Influencedon                Pupils                                Teachers                                       FriendsandCoworkers  FirstYear  LastYear         Places  
    0  Gustave Courbet         French                                 NaN                                            {Realism:272},         Rembrandt,Caravaggio,Diego Velazquez,Peter Pau...         Edouard Manet,Claude Monet,Pierre-Auguste Reno...                   NaN                                     NaN                                                       NaN     1830.0    1877.0            NaN  
    1    Auguste Rodin         French                                 NaN                        {Modern art:3},{Impressionism:91},                                   Michelangelo,Donatello,         Georgia O'Keeffe,Man Ray,Aristide Maillol,Olex...  Constantin Brancusi,                                     NaN                                                       NaN     1865.0    1985.0            NaN  
    2      Frida Kahlo        Mexican                                 NaN                  {Naïve Art (Primitivism),Surrealism:99},         Amedeo Modigliani,Diego Rivera,Jose Clemente O...               Judy Chicago,Georgia O'Keeffe,Feminist Art,                   NaN                                     NaN                                                       NaN     1922.0    1954.0            NaN  
    3           Banksy            NaN                                 NaN                                                       NaN                                                       NaN                                                       NaN                   NaN                                     NaN                                                       NaN     2011.0    2011.0            NaN  
    4         El Greco  Spanish,Greek                       Cretan School         {Spanish Renaissance:1},{Renaissance:2},{Manne...                                            Byzantine Art,         Expressionism,Cubism,Eugene Delacroix,Edouard ...                   NaN                                 Titian,                                            Giulio Clovio,     1568.0    1614.0            NaN  
    5     Diego Rivera        Mexican  Mexican Mural Renaissance,La Ruche                            {Social Realism,Muralism:146},                             Marc Chagall,Robert Delaunay,                          Frida Kahlo,Pedro Coronel,Vlady,                   NaN                                     NaN         Amedeo Modigliani,Saturnino Herran,Roberto Mon...     1904.0    1956.0            NaN  
    6     Claude Monet         French                                 NaN                      {Modern art:3},{Impressionism:1340},         Gustave Courbet,Charles-Francois Daubigny,John...         Childe Hassam,Robert Delaunay,Wassily Kandinsk...                   NaN           Eugene Boudin,Charles Gleyre,         Alfred Sisley,Pierre-Auguste Renoir,Camille Pi...     1858.0    1926.0            NaN  
    7   Francisco Goya        Spanish                                 NaN                                        {Romanticism:391},                           Albrecht Durer,Diego Velazquez,         Pablo Picasso,Chaim Soutine,Roberto Montenegro...                   NaN         José Luzán,Anton Raphael Mengs,                                                       NaN     1760.0    1828.0            NaN  
    8     Edvard Munch      Norwegian     Berlin Secession,Degenerate art                            {Symbolism,Expressionism:188},         Paul Gauguin,Vincent van Gogh,Henri de Toulous...         Egon Schiele,Wassily Kandinsky,Ernst Ludwig Ki...                   NaN                            Leon Bonnat,                                               Franz Marc,     1881.0    1944.0            NaN  
    9    Édouard Manet            NaN                                 NaN                                                       NaN                                                       NaN                                                       NaN                   NaN                                     NaN                                                       NaN     1858.0    1882.0            NaN  


</div>

</div>


<div class="cell markdown">

Every painting either has East or West origin (or not given).

</div>

<div class="cell code" execution_count="32">

``` python
rasta_artists = pd.read_csv("save2.csv")
rasta_artists[0:10]
```

<div class="output execute_result" execution_count="32">

                                   artist origin school  art_movement  FirstYear         LastYear  Places  
    0                     Piero di Cosimo   West    NaN           NaN        NaN              NaN     NaN  
    1        Rembrandt Harmensz. van Rijn   West    NaN           NaN        NaN              NaN     NaN  
    2        Jacob Isaacksz. van Ruisdael   West    NaN           NaN        NaN              NaN     NaN  
    3  Francisco José de Goya y Lucientes   West    NaN           NaN        NaN              NaN     NaN  
    4                    Lucas van Leyden   West    NaN           NaN        NaN              NaN     NaN  
    5                    Abraham Roentgen   West    NaN           NaN        NaN              NaN     NaN  
    6                   Hendrick Avercamp   West    NaN           NaN        NaN              NaN     NaN  
    7                     Hans Bollongier   West    NaN           NaN        NaN              NaN     NaN  
    8                   Adriaen van Wesel   West    NaN           NaN        NaN              NaN     NaN  
    9       Jacob Cornelisz van Oostsanen   West    NaN           NaN        NaN              NaN     NaN  

</div>

</div>

<div class="cell markdown">

From this, we could create a network possibly.

<details><summary><u>Something further:</u></summary>
<p>

https://en.wikipedia.org/wiki/Renaissance (at the bottom)
https://en.wikipedia.org/wiki/Periods_in_Western_art_history
    
</p>
</details>

</div>

<div class="cell markdown">

### PageRank / Wiki Connections:

Pagerank and WikiLinks are good examples

Wiki Connections: full dataset
<http://www.iesl.cs.umass.edu/data/data-wiki-links>

smaller dataset: <https://snap.stanford.edu/data/wikispeedia.html>

</div>

<div class="cell markdown">

# Philosophy, Politics

<details><summary><u>Philosophy</u></summary>
<p>

## Philosopher's web: 

Only available after paying 10$ for pro user

## Philosophy data
https://philosophydata.com/phil_nlp.zip
Downloaded, but not used yet, as I see it is NLP data 
</p>
</details>

</div>

<div class="cell markdown">

## Network connection example: Six Degrees of Francis Bacon

Network of the people connected to Francis Bacon, sadly the people in
the set are mostly all born in the 16th century and are English so most
philosophers in this list are not super relevant, there is no Kant,
Nietzsche, etc. But good example of a network

<http://www.sixdegreesoffrancisbacon.com/?ids=10000473&min_confidence=60&type=network>

<details><summary><u>Code for obtaining graph</u></summary>
<p>
    
```python
import igraph as ig #To install: conda install -c conda-forge python-igraph  
people = pd.read_csv('datasets/SDFB_people_.csv')
relationships = pd.read_csv('datasets/SDFB_relationships_.csv')

#I used igraph, because it's faster than networkx, and graph-tool sucks on Windows
network = relationships.rename(columns={'id': 'relationship_id', }).drop(columns=['created_by', 'approved_by', 'citation'])
print(network.head(), '\n')
cols = network.columns.tolist()
cols = cols[1:3] + cols[0:1] + cols[3:]
network = network[cols]
network = network[network['person1_index'] != 10050190] #for some reason, there is no person with this id, I did a loop
# I used the documentation here: https://python.igraph.org/en/stable/generation.html#from-pandas-dataframe-s  this I followed
# this is important too: https://python.igraph.org/en/stable/api/igraph.Graph.html#DataFrame  
g = ig.Graph.DataFrame(network, directed=False, vertices=people[['id', 'display_name','historical_significance','birth_year','death_year']], use_vids=False)
print(g.summary().replace(',', '\n'))
```
    
</p>
</details>
<details><summary><u>Code for filtering</u></summary>
<p>
    
```python
filtered = g.vs.select(_degree = 0) #https://python.igraph.org/en/stable/tutorial.html#selecting-vertices-and-edges
g.delete_vertices(filtered)

import cairo #Needed for plotting #import cairocffi as cairo  # can do matplotlib too
#layout = g.layout(layout='auto')
#ig.plot(g, layout = layout) #ig.plot(g) #looks even worse

```
    
</p>
</details>
<details><summary><u>Code for obtaining graph</u></summary>
<p>
    
```python
layout = g.layout(layout='reingold_tilford_circular') #kamada_kawai requires too much computing, 'fruchterman_reingold' is too dense
visual_style = {}
visual_style["vertex_size"] = 5
visual_style["vertex_color"] = "blue"
visual_style['bbox'] = (900, 900)
visual_style["layout"] = layout
#ig.plot(g, **visual_style) #Commented out because it takes big memory
# Needs improvement, but it's a start
```
    
</p>
</details>

</div>

<div class="cell markdown">

# Other opportunities for networks:

<https://global.health/> they got nice data on diseases, probably
time-variant too

<details><summary><u>Monkeypox, ebola</u></summary>
<p>
    
```python
df3 = pd.read_csv('datasets/monkeypox.csv')
df4 = pd.read_csv('datasets/ebola.csv')
df4
```
    
</p>
</details>

## Modeling of Biological + Socio-tech systems (MOBS) Lab

<https://www.mobs-lab.org/>

</div>
