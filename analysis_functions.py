import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter 

birthplace_weight = 0.5; places_weight = 0.4; nationality_weight = 0.8
weights = [birthplace_weight,places_weight,nationality_weight]

year_index_threshold = 0
places_threshold = 1.5
time_place_threshold = 0.4

def plot_network(G, pos, node_size=60, node_color='lightblue', edge_color='gray', width=1, edge_alpha=0.5, labels=False, label_font_size=10, show=True):
    plt.figure(figsize=(10,10))
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color)
    nx.draw_networkx_edges(G, pos, width=width,alpha=edge_alpha, edge_color=edge_color)
    if labels:
        nx.draw_networkx_labels(G, pos, font_size=label_font_size, font_family='sans-serif')
    plt.axis('off')
    if show:
        plt.show()

def plot_4_networks_2d_subplots(graphs, titles, layout_params_list=None):
    fig, axes = plt.subplots(2, 2, figsize=(10,10))
    axes = axes.flatten()

    for gi, G in enumerate(graphs):
        layout_params = layout_params_list[gi] if layout_params_list else None
        pos = nx.spring_layout(G, **layout_params) if layout_params else nx.spring_layout(G)

        nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5, edge_color='grey', ax=axes[gi])
        nx.draw_networkx_nodes(G, pos, node_size=60, node_color='green', alpha=0.5, ax=axes[gi])

        axes[gi].set_title(titles[gi])
        axes[gi].set_axis_off()
    plt.show()

def create_subgraph(graph_with_edgeweights,edge_threshold):
    G = nx.Graph()
    for edge in graph_with_edgeweights.edges():
        if graph_with_edgeweights[edge[0]][edge[1]]['weight'] > edge_threshold:
            G.add_edge(edge[0],edge[1])
    return G

### Index functions (for similarities between artists)

def year_index(years1, years2):
    #Year_index: years between first and last year are accounted with weight 1, years between birth and first year are accounted with weight 0.1.
    #For each overlapping year, we add 1 times the weights. Lastly, we divide by the total number of years of the younger artist.
    year_index = 0
    if(years1[0] > years2[0]):
        yearst = years1;years1 = years2;years2 = yearst
    #No overlap
    if(years1[2] < years2[0]):  #Not needed, but better for computation
        return 0
    for year in range((years1)[0], np.min([years1[2],years2[2]])+1):
        c = 1
        if year < years2[0]:
            c = 0
            continue
        if(year<years1[1]):
            c = c*0.2
        if(year<years2[1]):
            c = c*0.2
        year_index += c
    year_index = year_index/(np.min([years1[2]-years1[0],years2[2]-years2[0]])+1)
    return year_index

def place_index(placescount1, placescount2, birthplace1, birthplace2, nationality1, nationality2):
    #Places index
    i1 = 0; i2 = 0
    if placescount1 is not np.nan and placescount2 is not np.nan:
        places1_count_tuple = [(x.split(":")[0], int(x.split(":")[1])) if ":" in x else (x, 0) for x in placescount1]
        places2_count_tuple = [(x.split(":")[0], int(x.split(":")[1])) if ":" in x else (x, 0) for x in placescount2]
        for tuple1 in places1_count_tuple:
            for tuple2 in places2_count_tuple:
                if(tuple1[0] == tuple2[0]):
                    i1 += tuple1[1]; i2 += tuple2[1]
        sum1 = np.sum([x[1] for x in places1_count_tuple]); sum2 = np.sum([x[1] for x in places2_count_tuple])
        i1 = i1/np.min([sum1,25]); i2 = i2/np.min([sum2,25]) #This allows the places to go over 1, as many paintings in one place suggests a strong connection
        i = np.max([i1,i2])
    else:
        i = 0
    n1 = 0; n2 = 0
    if type(nationality1) == float or type(nationality2) == float:
        n = 0 #One of them is a nan
    else:
        for nat1 in nationality1.split(','):
            for nat2 in nationality2.split(','):
                if(nat1 == nat2):
                    n1 += 1; n2 += 1
        n = n1*n2/len(nationality1.split(','))/len(nationality2.split(','))
    b = 1 if birthplace1 == birthplace2 else 0
        
    """
        #Note: this codes almost always times out.
        else:
        #If they are in the same country, we give a weight of 0.5
        try:
            b = 0.5 if get_country(birthplace1) == get_country(birthplace2) else 0
        except:
            b = 0; print("Error with birthplaces: ", birthplace1, birthplace2)
    """

    return weights[0]*b + weights[1]*i + weights[2]*n



def plot_deg_distr_lin(degrees, ax=None, label_turnoff = False, ticks_list = None):
    import powerlaw as pwl

    deg_distri=Counter(degrees)
    keys, values = zip(*sorted(deg_distri.items()))

    # Degree distribution
    if(ax is None): #Here we divide between if we want to just create a one plot figure, or use this plot as a part of a bigger figure
        plt.scatter(keys, values, color='blue')
        plt.plot(keys, values, color='black', linewidth=2)  # This line connects the points
        plt.xticks(ticks = ticks_list)
        #plt.yticks(fontsize=22)
        if(not label_turnoff):
            plt.xlabel('Degree', )
            plt.ylabel('Frequency', )
            plt.title('Degree Distribution', )
        return plt
    else:
        ax.scatter(keys, values, color='blue')
        ax.plot(keys, values, color='black', linewidth=2)  # This line connects the points
        if (ticks_list is not None):
            ax.set_xticks(ticks_list)
        ax.tick_params(axis='both', which='major', )
        if(not label_turnoff):
            ax.set_title('Degree Distribution', )
            ax.set_xlabel('Degree', )
            ax.set_ylabel('Frequency', )
        return ax
    
def plot_deg_distr_linandlog(degrees, ax=None):
    import powerlaw as pwl
    deg_distri=Counter(degrees)
    keys, values = zip(*sorted(deg_distri.items()))

    #This case is easier, we will use axes anyways, just a difference in whether the function creates them or not
    if ax is None:
        fig, ax = plt.subplots(1, 2, figsize=(12,6))

    if len(ax.shape)==1:
        first_ax = ax[0]
        second_ax = ax[1]
    elif len(ax.shape)==2:
        first_ax = ax[0,0]
        second_ax = ax[0,1]
    else:
        print("Too many dimensions") #Added this for the future
        return

    #Degree distribution
    first_ax.scatter(keys, values, color='blue')
    first_ax.plot(keys, values, color='black', linewidth=2)  # This line connects the points
    first_ax.set_xlabel('Degree', fontsize=22)
    first_ax.set_ylabel('Frequency', fontsize=22)
    first_ax.set_xticks([1,5,10,21])
    first_ax.tick_params(axis='both', which='major', labelsize=20)
    
    #Lin-log
    x=[]; y=[]
    for i in sorted(deg_distri):   
        x.append(i); y.append(deg_distri[i]/len(degrees))
    second_ax.set_yscale('log')
    second_ax.set_xscale('log')
    second_ax.plot(x,y,'ro')
    pwl.plot_pdf(degrees, color='black', linewidth=2, ax=second_ax)
    second_ax.tick_params(axis='both', which='major', labelsize=20)
    second_ax.set_xlabel('Degree ($k$)', fontsize=22)
    second_ax.set_ylabel('$P(k)$', fontsize=22)

    fig.suptitle('Degree Distribution', fontsize=22)
    # Show the figure
    plt.tight_layout()
    if ax is None:
        plt.show()
    return ax

def plot_deg_dist_fit_log_single(degrees, ax=None, label_ignore=False):
    import powerlaw as pwl
    deg_distri=Counter(degrees)
    fit_f = pwl.Fit(degrees)
    
    x=[]; y=[]
    for i in sorted(deg_distri):   
        x.append(i); y.append(deg_distri[i]/len(degrees))

    if ax is None:
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111)

    ax.plot(x, y, 'ro')
    pwl.plot_pdf(degrees, color='black', linewidth=2, ax=ax)
    ax.set_xscale('log')
    ax.set_yscale('log')
    if not label_ignore:
        ax.set_xlabel('Degree ($k$)')
        ax.set_ylabel('$P(k)$')
        ax.set_title("Degree distribution")
    fit_f.power_law.plot_pdf(ax=ax, color='b', linestyle='-', linewidth=1, label='fit')

def plot_deg_dist_fit_log(degrees_list, label_ignore_list=None):
    if label_ignore_list is None:
        label_ignore_list = [False] * len(degrees_list)

    n = len(degrees_list)
    if n == 1:
        plot_deg_dist_fit_log_single(degrees_list[0], label_ignore=label_ignore_list[0])
        #return something
    else:
        rows = (n + 1) // 2
        fig, axes = plt.subplots(rows, 2, figsize=(12, 6*rows))
        axes = axes.flatten()
        for i, degrees in enumerate(degrees_list):
            plot_deg_dist_fit_log_single(degrees, ax=axes[i], label_ignore=label_ignore_list[i])
        plt.tight_layout()
        #plt.show()
        return fig, axes
    

####### Shortest path functions
    
def avg_shortest_path_length_0_disconnected_distance(G):
    # Firstly, a list of components
    G_copy = (G.copy()).to_undirected()
    components = list(nx.connected_components(G_copy))

    total_path_length = 0
    total_pairs = G_copy.number_of_nodes() * (G_copy.number_of_nodes() - 1) / 2  #All possible pairs of nodes

    for component in components:
        # Create a subgraph for this component
        subgraph = G_copy.subgraph(component)
        if len(component) > 1:  # Don't calculate for isolated nodes
            total_path_length += nx.average_shortest_path_length(subgraph) * len(component) * (len(component) - 1)/2
            

    avg = total_path_length / total_pairs  # Average path length
    return avg

#The NetworkX function for average shortest path length does not work for disconnected graphs, so we need to create our own function
def avg_shortest_path_length(G):
    #Firstly, a list of components
    G_copy = (G.copy()).to_undirected()
    components = list(nx.connected_components(G_copy))

    avgs = np.array([])
    lengths = np.array([])
    for component in components:
        if len(component) > 1: #Don't calculate for isolated nodes
            subgraph = G_copy.subgraph(component)
            avgs = np.append(avgs, nx.average_shortest_path_length(subgraph))
            lengths = np.append(lengths, len(component))
    avg = np.sum(avgs*lengths)/np.sum(lengths) #Weighted average: each average has the weight of how many nodes are in the component (basically, this equals summing all node averages, then dividing by the total number of nodes)
    return avg