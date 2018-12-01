# R Tutorial

RTFM: http://igraph.org/r/doc/igraph.pdf

## Load and/or install all the packages we'll need

```R
library(igraph)
library(ape)
library(jsonlite)
library(data.table)
library(igraph)
library(maps)
library(igraph)
library(ggmap)
```

or 

```R
install.packages("igraph")
install.packages("ape")
install.packages("jsonlite")
install.packages("data.table")
install.packages("igraph")
install.packages("maps")
install.packages("igraph")
install.packages("ggmap")
```

## Package landscape

* igraph: http://igraph.org/r/
  * workhorse for general purpose network analysis

* sna: http://www.statnet.org/
  * general purpose network analysis and statistical inference
  
* ggraph: https://github.com/thomasp85/ggraph
  * great for visualization 

* circlize: https://github.com/jokergoo/circlize
  * chord diagrams for relational data
  
* many other, more specialized packages

## "hello world" example

```R
# initialize a graph
g <- make_empty_graph()

# add a vertex
g <- add_vertices(g, 1, name="hello")

# add another vertex
g <- add_vertices(g, 1, name="world")

# add an edge
g <- add_edges(g, c("hello","world"))

# plot the graph
plot(g)

# see the vertices
V(g)

# see the edges
E(g)

# count the vertices
vcount(g)

# count the edges
ecount(g)

# check out the affiliation matrix
g[]
g[1,]

# check whether graph is directed
is_directed(g)

# remake undirected graph
g = make_empty_graph(directed=FALSE)
g <- add_vertices(g, 1, name="hello")
g <- add_vertices(g, 1, name="world")
g <- add_edges(g, c("hello","world"))
is_directed(g)

# you can also create a graph just from a list of edges
g <- graph( c("hello", "world"))

# for small graphs, igraph also has a "graph_from_literal" function that is useful
g <- graph_from_literal(hello---world) # undirected edge
plot(g)
g <- graph_from_literal(hello--+world) # directed edge
plot(g)
```

## Generating graphs

Let's move beyond our "hello world" example and start looking at more complex networks.

```R
# empty graph
eg <- make_empty_graph(10)

# full graph
fg <- make_full_graph(10)

# star graph
sg <- make_star(10)

# ring graph
rg <- make_ring(10)

# bipartite graph
bg <- make_full_bipartite_graph(5, 5)

par(mfrow = c(2,3))
plot(eg)
plot(fg)
plot(sg)
plot(rg)
plot(bg, layout = layout.bipartite)

# igraph also has a few famous graphs stored internally, e.g.,
g <- make_graph("Zachary")
plot(g, layout = layout.fruchterman.reingold, vertex.size = 2, vertex.label = NA)

g <- make_graph("Krackhardt kite")
plot(g, layout = layout.fruchterman.reingold, vertex.size = 2, vertex.label = NA)

# igraph also has many functions for generating random graphs with certain properties

# small world
g <- sample_smallworld(dim=1, size=15, nei=3, p=0.1)
plot(g, layout=layout.circle, vertex.size = 2, vertex.label = NA)

# barabasi
g <- sample_pa(1000)
plot(g, layout=layout.fruchterman.reingold, vertex.size = 2, vertex.label = NA, edge.arrow.size=0.5)

# erdos renyi
g <- erdos.renyi.game(n=1000, p=1/1000)
plot(g, layout=layout.fruchterman.reingold, vertex.size = 2, vertex.label = NA, edge.arrow.size=0.5)
```

## Characterizing vertices

```R
# make a sample graph
g <- sample_smallworld(dim=1, size=100, nei=3, p=0.3)
plot(g, layout=layout.fruchterman.reingold, vertex.size = 2, vertex.label = NA)

# get some measures of centrality
V(g)$degree <- degree(g)
V(g)$betweenness <- betweenness(g)
V(g)$closeness <- closeness(g)
V(g)$page_rank <- page_rank(g)$vector

# structural holes
V(g)$constraint <- constraint(g)

# plot with vertex weights proportional to centrality
plot(g, layout=layout.fruchterman.reingold, vertex.size = V(g)$degree, vertex.label = NA)

# for fun, what if we had weighted edges?
E(g)$weight <- rpois(ecount(g), 3)
plot(g, layout=layout.fruchterman.reingold, vertex.size = V(g)$degree, edge.width = E(g)$weight, vertex.label = NA)

# let's fiddle with some other plot settings
plot(g, layout=layout.fruchterman.reingold, 
        vertex.size = V(g)$degree, 
        vertex.color = "#334D5C80",
        vertex.frame.color = NA,
        edge.color = "#45B29D80",
        edge.width = E(g)$weight, 
        edge.lty = "dashed",
        edge.curved = 0.8,
        vertex.label = NA)

# getting crazy
pie_values <- lapply(1:vcount(g), function(x) sample(1:vcount(g),2))
plot(g, layout=layout.fruchterman.reingold, 
        vertex.size = V(g)$degree, 
        vertex.color = "#334D5C80",
        vertex.frame.color = NA,
        edge.color = "#45B29D80",
        edge.width = E(g)$weight, 
        edge.lty = "dashed",
        edge.curved = 0.8,
        vertex.label = NA,
        vertex.shape="pie",
       vertex.pie= pie_values,
       vertex.pie.color=list(c("#DF4949", "#EFC94C")))
```

## Characterizing networks

```R
# make a sample graph
g <- sample_smallworld(dim=1, size=100, nei=3, p=0.3)
plot(g, layout=layout.fruchterman.reingold, vertex.size = 2, vertex.label = NA)

# density
edge_density(g)

# path lengths
mean_distance(g)
distance_table(g) # note on "dijkstra"

# diameter
diameter(g)

# communities

# run walktrap community detection on our favorite graph
g <- make_graph("Zachary")
wc <- cluster_walktrap(g)

# check modularity
modularity(wc)

# save community membership of nodes
membership(wc)

# save edges that cross communities
E(g)$boundary_spanning <- crossing(wc, g)
E(g)[boundary_spanning == TRUE]$color <- "#DF4949"
E(g)[boundary_spanning == FALSE]$color <- "#334D5C"

# plot boundary spanning edges
plot(g, layout = layout.fruchterman.reingold, 
        vertex.label = NA, 
        vertex.frame.color = NA, 
        vertex.size = degree(g), 
        vertex.color = "#45B29D80", 
        edge.color = E(g)$color, 
        edge.width=2)

# plot community structure
plot(wc, g, layout = layout.fruchterman.reingold, 
            vertex.label = NA, 
            vertex.size = 2)

# plot dendrograms
plot_dendrogram(wc, mode="phylo")
dendPlot(wc, 
         type = "fan", 
         cex = 1, 
         no.margin = FALSE, 
         label.offset = 2, 
         col = "#000000")
```

## Network data structures

```R

# three main types to know

# edge list
edl <- matrix( c("foo", "bar", "bar", "foobar"), nc = 2)
g <- graph_from_edgelist(edl)
plot(g, layout=layout.fruchterman.reingold)

# adjacency matrix
adj <- matrix(sample(0:1, 100, replace=TRUE, prob=c(0.9,0.1)), nc=10)
g <- graph_from_adjacency_matrix( adj )
plot(g, layout=layout.fruchterman.reingold)

# incidence matrix (for bipartite graphs)
inc <- matrix(sample(0:1, 15, repl=TRUE), 3, 5)
colnames(inc) <- letters[1:5]
rownames(inc) <- LETTERS[1:3]
g <- graph_from_incidence_matrix(inc)
plot(g, layout = layout.bipartite)

## Working with data

# pull inventors on patents with at least one inventor from Minneapolis, MN in 2014
data <- jsonlite::fromJSON("http://www.patentsview.org/api/inventors/query?q={%22_and%22:[{%22_gte%22:{%22patent_date%22:%222014-01-01%22}},{%22_lt%22:{%22patent_date%22:%222014-12-31%22}},{%22location_city%22:%22Minneapolis%22},{%22location_state%22:%22MN%22}]}&f=[%22patent_number%22,%22inventor_id%22]&o={%22per_page%22:%202000}")

# make a 2 mode edge list
edges_2mode <- as.data.frame(rbindlist(data$inventors$patents, use.names=TRUE, fill=TRUE, idcol="inventor_idx"))

# make a bipartite graph
g <- graph_from_data_frame(edges_2mode, directed=FALSE)

# check whether bipartite
is_bipartite(g)

# need to add types vertex attribute
V(g)$type <- V(g)$name %in% edges_2mode[,1]

# check again
is_bipartite(g)

# plot the bipartite graph
V(g)[type == TRUE]$color <- "#45B29D80"
V(g)[type == FALSE]$color <- "#DF494980"
plot(g, layout = layout.bipartite, 
        vertex.color = V(g)$color, 
        vertex.size = 5, 
        edge.width = 0.25,
        vertex.label = NA,
        edge.color =  "#334D5C80")
        
# we're probably more interested in connections among inventors
g_patents <- bipartite.projection(g)$proj1
g_inventors <- bipartite.projection(g)$proj2

# we could drop the isolates
V(g_inventors)$degree <- degree(g_inventors)
g_inventors <- delete_vertices(g_inventors, V(g_inventors)[degree==0])

# let's just focus on the main component
cl <- clusters(g_inventors) 
g_inventors <- induced.subgraph(g_inventors, which(cl$membership == which.max(cl$csize)))

# plot
plot(g_inventors, 
        vertex.size = sqrt(betweenness(g_inventors)/100), 
        vertex.label = NA,
        edge.color =  "#334D5C80")
```

## Networks on maps

```R
# make a map
map("state", plot=TRUE, col = "#121212", bg="#000000", fill = TRUE) 
map("state", plot=TRUE, boundary = TRUE, lty = 1, col = "#424143", fill = FALSE, add=TRUE) 

# make a graph
g <- make_star(5, mode="undirected")

# get some latitudes and longitudes of US cities from the maps package
coords <- data.frame(us.cities$lat, us.cities$lon)

# assign locations to vertices
vs_coords <- coords[sample(nrow(coords), vcount(g)),]

# create the layout
layout <- as.matrix(cbind(vs_coords$us.cities.lon, vs_coords$us.cities.lat))

# plot the graph
plot(g, layout= layout, 
        vertex.size = degree(g), 
        vertex.color = "#334D5C80",
        vertex.frame.color = NA,
        edge.color = "#0039FF80",
        vertex.label = NA,
        rescale=FALSE, 
        add=TRUE)

# let's kick it up a notch
map("state", plot=TRUE, col = "#121212", bg="#000000", fill = TRUE) 
map("state", plot=TRUE, boundary = TRUE, lty = 1, col = "#424143", fill = FALSE, add=TRUE) 

# make a graph
g <- sample_smallworld(dim=1, size=1000, nei=3, p=0.3)

# get some latitudes and longitudes of US cities from the maps package
coords <- data.frame(us.cities$lat, us.cities$lon)

# assign locations to vertices
vs_coords <- coords[sample(nrow(coords), vcount(g), replace=TRUE),]

# create the layout
layout <- as.matrix(cbind(vs_coords$us.cities.lon, vs_coords$us.cities.lat))

# plot the graph
plot(g, layout= layout, 
        vertex.size = degree(g)**2, 
        vertex.color = "#00B8FF40",
        vertex.frame.color = NA,
        edge.color = "#0039FF15",
        vertex.label = NA,
        rescale=FALSE, 
        add=TRUE)


# going back to the star graph, we can also have R (via the Google Maps API) geocode some stuff for us
map("state", plot=TRUE, col = "#121212", bg="#000000", fill = TRUE) 
map("state", plot=TRUE, boundary = TRUE, lty = 1, col = "#424143", fill = FALSE, add=TRUE) 

# make a graph
g <- make_star(5, mode="undirected")

# geocode with Google maps (careful, read the terms of service)
vs_coords <- rbind(geocode("university of minnesota, twin cities"),
                   geocode("houston texas"),
                   geocode("lake meade"),
                   geocode("spokane washington"),      
                   geocode("1600 pennsylvania avenue, washington dc"))

# create the layout
layout <- as.matrix(cbind(vs_coords$lon, vs_coords$lat))

# plot the graph
plot(g, layout= layout, 
        vertex.size = degree(g), 
        vertex.color = "#334D5C80",
        vertex.frame.color = NA,
        edge.color = "#0039FF80",
        vertex.label = NA,
        rescale=FALSE, 
        add=TRUE)
```

## Additional resources and further reading

* https://www.r-bloggers.com/
* https://flowingdata.com/
* https://www.rstudio.com/resources/cheatsheets/



