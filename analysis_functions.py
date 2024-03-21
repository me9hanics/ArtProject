import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter 

birthplace_weight = 0.8; places_weight = 1; nationality_weight = 0.3; citizenship_weight = 0.4 #A bit more, as it is more specific
place_weights = [birthplace_weight,places_weight,nationality_weight, citizenship_weight]

year_index_threshold = 0; places_threshold = 1.5; time_place_threshold = 0.4
index_thresholds = [year_index_threshold,places_threshold,time_place_threshold]

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
    if(years1[0] > years2[0]): #Make sure the second year is the larger
        yearst = years1;years1 = years2;years2 = yearst
    #No overlap
    if(years1[2] < years2[0]): #Not necessary (we'd return 0 anyways) but better for computation
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
    year_index = year_index/(np.min([years1[2]-years1[0], (years2[2]-years2[0])])+1) #Theoretically, the denominator cannot be 0 or negative 
    return year_index

def place_index_biased(places1, places2, birthplace1, birthplace2, nationality1, nationality2, citizenship1, citizenship2, weights = None, thresholds = None):
    #Places index
    if weights is None:
        weights = place_weights
    if thresholds is None:
        thresholds = index_thresholds
        
    i = 0
    if places1 and places2:
        for place1 in places1.split(','):
            for place2 in places2.split(','):
                if place1 == place2:
                    i += 1
        num_places1 = len(places1); num_places2 = len(places2)
        block = max(num_places1, num_places2) // 5 #Go in blocks of 5
        i = i * (0.8**block) #The more places, the less important it is
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

    if type(citizenship1) == float or type(citizenship2) == float:
        c = 0
    else:
        if citizenship1 == citizenship2:
            c = 1

    return weights[0]*b + weights[1]*i + weights[2]*n + weights[3]*c

def index_simple(places1, places2, years1, years2, birthplace1, birthplace2, nationality1, nationality2, citizenship1, citizenship2, active_years_only = False):
    p = 0
 
    if (type(places1) != float and type(places2) != float):
        #Assuming not np.nan, but list
        for place1 in places1:
            for place2 in places2:
                if place1 == place2:
                    p += 1

    if not type(birthplace1) == float and not type(birthplace2) == float:
        if birthplace1 == birthplace2:
            p += 1
    if not type(nationality1) == float and not type(nationality2) == float:
        for nat1 in nationality1:
            for nat2 in nationality2:
                if nat1 == nat2:
                    p += 0.3/(len(nationality1)*len(nationality2))
    if not type(citizenship1) == float and not type(citizenship2) == float:
        if citizenship1 == citizenship2:
            p += 0.3

    #Years: Birthyear, first year, last year, death year. Assumed all four are given
    common_years = 0
    common_active_years = 0
    if years1[1] > years2[1]:
        years_min, years_max = years2, years1
    else:
        years_min, years_max = years1, years2

    for i in range(int(years_min[1]), int(years_min[2])+1):
        if i >= years_max[1] and i <= years_max[2]:
            common_active_years += 1
    
    if years1[0]>years2[0]:
        years_min, years_max = years2, years1
    else:
        years_min, years_max = years1, years2

    for i in range(int(years_min[0]), int(years_min[3])+1):
        if i >= years_max[0] and i <= years_max[3]:
            common_years += 1


    #Formula: average_common_years / places  *  common_places  -> Dimension: time (which is good, because more time means more connections)
    if active_years_only:
        average_common_years_per_place1 = common_active_years/(len(places1))
        average_common_years_per_place2 = common_active_years/(len(places2))
    else:
        average_common_years_per_place1 = common_years/(len(places1))
        average_common_years_per_place2 = common_years/(len(places2))
    
    return (average_common_years_per_place1 + average_common_years_per_place2) * p


    



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