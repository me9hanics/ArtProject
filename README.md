
<div class="cell markdown">

# Network of Painters: building a dataset from paintings datasets, then creating links

The aim of this project is to create a dataset of painters from datasets
such as WikiArt and Art500k, combining features, extending missing data
of painters with web scraping through Google and Wiki API, and then
creating links between painters based on similarity of style,
geographical and social interaction.

Note: One long-term goal would be to create a JSON file that contains
all combined hierarchically. For example, a level in the structure could
be art movement, inside it, are artists with some base data like
birthplace, year of birth and death and other geographical data, inside
it are paintings with all contained data (even better would be including
eras of painters in their substructure, and inside them the paintings).
Then we could use this to create a network of art movements, artists,
and paintings.

NEXT STEPS:<br> -Add "Places" for Art500k datasets (+change
datasets_notebook save.csv loads)<br> -Add aliases for painters in
Art500k datasets<br> -Combine the datasets on authors<br>

FURTHER STEPS: <br> -Define connections between painters<br> -Create a
network of painters<br> -Analyze the network<br>

![image](https://github.com/me9hanics/ArtProject/assets/82604073/039688be-16f0-4432-bae2-acba9688914b)

![image](https://github.com/me9hanics/ArtProject/assets/82604073/585fd608-79c3-4313-8eaf-5c6cc1ebb082)


# The main datasets used (paintings datasets):

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

``` python
wa_paintings = pd.read_csv('datasets/wikiart_paintings_refined.csv')
print("Length:", len(wa_paintings))
wa_paintings.head() #Consider dropping style: "Unknown" 
```

<div class="output stream stdout">

    Length: 175313

</div>

<div class="output execute_result" execution_count="3">

              artist                           style               genre            movement                                               tags  
    0  Andrei Rublev  Moscow school of icon painting  religious painting       0  Byzantine Art  ['Christianity', 'saints-and-apostles', 'angel...  
    1  Andrei Rublev  Moscow school of icon painting  religious painting       1  Byzantine Art  ['Christianity', 'Old-Testament', 'Daniel', 'p...  
    2  Andrei Rublev  Moscow school of icon painting           miniature       2  Byzantine Art  ['Christianity', 'saints-and-apostles', 'Khitr...  
    3  Andrei Rublev  Moscow school of icon painting  religious painting       3  Byzantine Art  ['Christianity', 'saints-and-apostles', 'St.-L...  
    4  Andrei Rublev  Moscow school of icon painting           miniature       4  Byzantine Art  ['Christianity', 'arts-and-crafts', 'saints-an... 

</div>

</div>

<div class="cell markdown">

Load the grouped data: artists grouped by style

</div>

<div class="cell code" execution_count="11">

``` python
wa_grouped = pd.read_csv('datasets/wikiart_artists_styles_grouped.csv')
print("Length:", len(wa_grouped), "\n", "Number of groups with only 1 count:", len(wa_grouped[wa_grouped['count']==min(wa_grouped['count'])]))
wa_grouped[wa_grouped['artist'].str.contains("Monet")].sort_values(by=['count'], ascending=False)
```

<div class="output stream stdout">

    Length: 7647 
     Number of groups with only 1 count: 1115

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

    C:\Users\hanic\AppData\Local\Temp\ipykernel_18740\2660317568.py:1: DtypeWarning: Columns (2,4,5,6,8,9,11,13,14) have mixed types. Specify dtype option on import or set low_memory=False.
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

There needs to be further work done as seen.

</div>

<div class="cell markdown">

Second dataset: from Rasta <br>
<https://github.com/nphilou/rasta/tree/d22b34d5ac1aee9c1f80b4a73ad6792fd465c605/data/art500k>

</div>

<div class="cell code" execution_count="31">

``` python
rasta = pd.read_table('datasets/originals/art500k_rasta370k.txt', header=0, engine='python', sep='\t|\s{4,}');
rasta[0:5]
```

<div class="output stream stderr">

    <>:1: SyntaxWarning: invalid escape sequence '\s'
    <>:1: SyntaxWarning: invalid escape sequence '\s'
    C:\Users\hanic\AppData\Local\Temp\ipykernel_18740\3524387221.py:1: SyntaxWarning: invalid escape sequence '\s'
      rasta = pd.read_table('datasets/originals/art500k_rasta370k.txt', header=0, engine='python', sep='\t|\s{4,}');

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