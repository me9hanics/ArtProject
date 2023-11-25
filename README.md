---
jupyter:
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  language_info:
    codemirror_mode:
      name: ipython
      version: 3
    file_extension: .py
    mimetype: text/x-python
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
    version: 3.12.0
  nbformat: 4
  nbformat_minor: 4
---

<div class="cell markdown">

# Network of Painters: building a dataset from paintings datasets, then creating links

The aim of this project is to create a dataset of painters from datasets
such as WikiArt and Art500k, combining features, extending missing data
of painters with web scraping through Google and Wiki API, and then
creating links between painters based on similarity of style,
geographical and social interaction.

Note: One long-term goal would be to create a JSON file that contains
all combined hierarchically. For example, a level in the structure could
be art movement, inside it are artists with some base data like
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


</div>

<div class="cell code" execution_count="21">

``` python
import pandas as pd
import numpy as np
```

</div>

<div class="cell markdown">

<details><summary><u>National Gallery of Art  (US) dataset (unused) </u></summary>
<p>
    
```python

df1 = pd.read_csv('datasets/originals/nga_constituents.csv') # From their website
df1.head()

```
    
</p>
</details>

</div>

<div class="cell markdown">

## WikiArt data

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

              artist                           style               genre  \
    0  Andrei Rublev  Moscow school of icon painting  religious painting   
    1  Andrei Rublev  Moscow school of icon painting  religious painting   
    2  Andrei Rublev  Moscow school of icon painting           miniature   
    3  Andrei Rublev  Moscow school of icon painting  religious painting   
    4  Andrei Rublev  Moscow school of icon painting           miniature   

            movement                                               tags  
    0  Byzantine Art  ['Christianity', 'saints-and-apostles', 'angel...  
    1  Byzantine Art  ['Christianity', 'Old-Testament', 'Daniel', 'p...  
    2  Byzantine Art  ['Christianity', 'saints-and-apostles', 'Khitr...  
    3  Byzantine Art  ['Christianity', 'saints-and-apostles', 'St.-L...  
    4  Byzantine Art  ['Christianity', 'arts-and-crafts', 'saints-an...  

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

           author_name                                      painting_name Genre  \
    0  Gustave Courbet                Woman With A Parrot##AAHozJAL0gqXcA   NaN   
    1    Auguste Rodin         La Tentation Saint Antoine##WAGC82imJTDyIg   NaN   
    2      Frida Kahlo   Retrato De Alejandro Gómez Arias##0QFuguLe4xyN_A   NaN   
    3           Banksy           The Wall Banksy Balloons##FgHoVE-hmt6DBQ   NaN   
    4         El Greco                     The Visitation##HQEQ_qXDtRrzkA   NaN   
    5         El Greco  Madonna And Child With Saint Martina And Saint...   NaN   

      Style Nationality PaintingSchool ArtMovement           Date Influencedby  \
    0   NaN         NaN            NaN         NaN            NaN          NaN   
    1   NaN         NaN            NaN         NaN            NaN          NaN   
    2   NaN         NaN            NaN         NaN            NaN          NaN   
    3   NaN         NaN            NaN         NaN            NaN          NaN   
    4   NaN         NaN            NaN         NaN  ca. 1610-1614          NaN   
    5   NaN         NaN            NaN         NaN            NaN          NaN   

      Influencedon  Tag Pupils                                         Location  \
    0          NaN  NaN    NaN                                              NaN   
    1          NaN  NaN    NaN                                              NaN   
    2          NaN  NaN    NaN                                              NaN   
    3          NaN  NaN    NaN  in a settlement in Palestine in the middle east   
    4          NaN  NaN    NaN                                              NaN   
    5          NaN  NaN    NaN                                              NaN   

      Teachers FriendsandCoworkers  
    0      NaN                 NaN  
    1      NaN                 NaN  
    2      NaN                 NaN  
    3      NaN                 NaN  
    4      NaN                 NaN  
    5      NaN                 NaN  

</div>

</div>

<div class="cell code" execution_count="30">

``` python
art500k_artists = pd.read_csv('save.csv')
art500k_artists[0:10]
```

<div class="output execute_result" execution_count="30">

                artist    Nationality                      PaintingSchool  \
    0  Gustave Courbet         French                                 NaN   
    1    Auguste Rodin         French                                 NaN   
    2      Frida Kahlo        Mexican                                 NaN   
    3           Banksy            NaN                                 NaN   
    4         El Greco  Spanish,Greek                       Cretan School   
    5     Diego Rivera        Mexican  Mexican Mural Renaissance,La Ruche   
    6     Claude Monet         French                                 NaN   
    7   Francisco Goya        Spanish                                 NaN   
    8     Edvard Munch      Norwegian     Berlin Secession,Degenerate art   
    9    Édouard Manet            NaN                                 NaN   

                                             ArtMovement  \
    0                                     {Realism:272},   
    1                 {Modern art:3},{Impressionism:91},   
    2           {Naïve Art (Primitivism),Surrealism:99},   
    3                                                NaN   
    4  {Spanish Renaissance:1},{Renaissance:2},{Manne...   
    5                     {Social Realism,Muralism:146},   
    6               {Modern art:3},{Impressionism:1340},   
    7                                 {Romanticism:391},   
    8                     {Symbolism,Expressionism:188},   
    9                                                NaN   

                                            Influencedby  \
    0  Rembrandt,Caravaggio,Diego Velazquez,Peter Pau...   
    1                            Michelangelo,Donatello,   
    2  Amedeo Modigliani,Diego Rivera,Jose Clemente O...   
    3                                                NaN   
    4                                     Byzantine Art,   
    5                      Marc Chagall,Robert Delaunay,   
    6  Gustave Courbet,Charles-Francois Daubigny,John...   
    7                    Albrecht Durer,Diego Velazquez,   
    8  Paul Gauguin,Vincent van Gogh,Henri de Toulous...   
    9                                                NaN   

                                            Influencedon                Pupils  \
    0  Edouard Manet,Claude Monet,Pierre-Auguste Reno...                   NaN   
    1  Georgia O'Keeffe,Man Ray,Aristide Maillol,Olex...  Constantin Brancusi,   
    2        Judy Chicago,Georgia O'Keeffe,Feminist Art,                   NaN   
    3                                                NaN                   NaN   
    4  Expressionism,Cubism,Eugene Delacroix,Edouard ...                   NaN   
    5                   Frida Kahlo,Pedro Coronel,Vlady,                   NaN   
    6  Childe Hassam,Robert Delaunay,Wassily Kandinsk...                   NaN   
    7  Pablo Picasso,Chaim Soutine,Roberto Montenegro...                   NaN   
    8  Egon Schiele,Wassily Kandinsky,Ernst Ludwig Ki...                   NaN   
    9                                                NaN                   NaN   

                              Teachers  \
    0                              NaN   
    1                              NaN   
    2                              NaN   
    3                              NaN   
    4                          Titian,   
    5                              NaN   
    6    Eugene Boudin,Charles Gleyre,   
    7  José Luzán,Anton Raphael Mengs,   
    8                     Leon Bonnat,   
    9                              NaN   

                                     FriendsandCoworkers  FirstYear  LastYear  \
    0                                                NaN     1830.0    1877.0   
    1                                                NaN     1865.0    1985.0   
    2                                                NaN     1922.0    1954.0   
    3                                                NaN     2011.0    2011.0   
    4                                     Giulio Clovio,     1568.0    1614.0   
    5  Amedeo Modigliani,Saturnino Herran,Roberto Mon...     1904.0    1956.0   
    6  Alfred Sisley,Pierre-Auguste Renoir,Camille Pi...     1858.0    1926.0   
    7                                                NaN     1760.0    1828.0   
    8                                        Franz Marc,     1881.0    1944.0   
    9                                                NaN     1858.0    1882.0   

       Places  
    0     NaN  
    1     NaN  
    2     NaN  
    3     NaN  
    4     NaN  
    5     NaN  
    6     NaN  
    7     NaN  
    8     NaN  
    9     NaN  

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

<div class="output execute_result" execution_count="31">

       img_id img_name        img_path  \
    0       1    1.jpg  data_img/1.jpg   
    1       2    2.jpg  data_img/2.jpg   
    2       3    3.jpg  data_img/3.jpg   
    3       4    4.jpg  data_img/4.jpg   
    4       5    5.jpg  data_img/5.jpg   

                                               img_title  \
    0  Portraits of Giuliano and Francesco Giamberti ...   
    1  Militia Company of District II under the Comma...   
    2  Portrait of a Couple as Isaac and Rebecca, kno...   
    3                 The Windmill at Wijk bij Duurstede   
    4                        Portrait of Don Ramón Satué   

                                   artist origin  art_movement genre  \
    0                     Piero di Cosimo   West           NaN   NaN   
    1        Rembrandt Harmensz. van Rijn   West           NaN   NaN   
    2        Rembrandt Harmensz. van Rijn   West           NaN   NaN   
    3        Jacob Isaacksz. van Ruisdael   West           NaN   NaN   
    4  Francisco José de Goya y Lucientes   West           NaN   NaN   

               media style location technique school  date time  object  color  \
    0   oil on panel   NaN      NaN       NaN    NaN  1482   15     NaN    NaN   
    1  oil on canvas   NaN      NaN       NaN    NaN  1642   17     NaN    NaN   
    2  oil on canvas   NaN      NaN       NaN    NaN  1665   17     NaN    NaN   
    3  oil on canvas   NaN      NaN       NaN    NaN  1668   17     NaN    NaN   
    4  oil on canvas   NaN      NaN       NaN    NaN  1823   19     NaN    NaN   

                                                     url  
    0  http://lh4.ggpht.com/NwCWmjro4h__Ord5RqicIJsJb...  
    1  http://lh6.ggpht.com/ZYWwML8mVFonXzbmg2rQBulNu...  
    2  http://lh5.ggpht.com/H-KfOaNgW2an_g0kODWKua5BE...  
    3  http://lh6.ggpht.com/1gH99j2GD85SW4r3CA18uwTDu...  
    4  http://lh4.ggpht.com/wyy5JOPbVx1wQ9ax57OmfOz4k...  

</div>

</div>

<div class="cell markdown">

Every painting either has East or West origin (or not given), may just
filter to one of them

</div>

<div class="cell code" execution_count="32">

``` python
rasta_artists = pd.read_csv("save2.csv")
rasta_artists[0:10]
```

<div class="output execute_result" execution_count="32">

                                   artist origin school  art_movement  FirstYear  \
    0                     Piero di Cosimo   West    NaN           NaN        NaN   
    1        Rembrandt Harmensz. van Rijn   West    NaN           NaN        NaN   
    2        Jacob Isaacksz. van Ruisdael   West    NaN           NaN        NaN   
    3  Francisco José de Goya y Lucientes   West    NaN           NaN        NaN   
    4                    Lucas van Leyden   West    NaN           NaN        NaN   
    5                    Abraham Roentgen   West    NaN           NaN        NaN   
    6                   Hendrick Avercamp   West    NaN           NaN        NaN   
    7                     Hans Bollongier   West    NaN           NaN        NaN   
    8                   Adriaen van Wesel   West    NaN           NaN        NaN   
    9       Jacob Cornelisz van Oostsanen   West    NaN           NaN        NaN   

       LastYear  Places  
    0       NaN     NaN  
    1       NaN     NaN  
    2       NaN     NaN  
    3       NaN     NaN  
    4       NaN     NaN  
    5       NaN     NaN  
    6       NaN     NaN  
    7       NaN     NaN  
    8       NaN     NaN  
    9       NaN     NaN  

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

The Python Class 6 original_networkx_SP_06.ipynb file had a good example
for PageRank

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

## Network connection: Six Degrees of Francis Bacon

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
