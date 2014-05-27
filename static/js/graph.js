/**
 * Creates a Graph object when given the json object that is a graph represented as a dictionary
 * adjacency list (a dictionary mapping node names to lists of node names).
 * (Such an adjacency list can be created by the python script: graph_text_to_json.py)
 * Note that this representation essentially assumes that you only have one friend
 * with any specific name.  Sorry.  You could work around this by making the "name" the
 * id of the point.  Also note that this representation assuems that all edges have the
 * same weight as that's all that's needed for your implementation of PageRank.
 */ 
function Graph(json) {
    this.graph = json;
    this.nodes = {};
    this.names = Object.keys(this.graph);
    for (var i = 0; i < this.names.length; i++) {
        this.nodes[this.names[i]] = new Node(i, this.names[i]);
    }
}

/**
 * Returns the nodes that go into this node.  If these haven't yet been
 * determined, this function takes the time to determine this set and then
 * saves it.
 */
Graph.prototype.getIn = function(node) {
    if (node.getIn()) {
        return node.getIn();
    }
    var inNodes = [];
    for (var i = 0; i < this.names.length; i++) {
        var inNode = this.nodes[this.names[i]];
        var edges = this.graph[this.names[i]];
        for (var e = 0; e < edges.length; e++) {
            var endNode = this.nodes[edges[e]];
            if (endNode.equals(node)) {
                inNodes.push(inNode);
            }
        }
    }
    node.setIn(inNodes);
    return inNodes; 
}

/**
 * Returns the nodes that this node has edges to as a list of names.
 */
Graph.prototype.getOut = function(node) {
    var name = node.name;
    return this.graph[name];
}

/**
 * Returns a list of nodes that do not have any edges out (have an out-degree of 0).
 */
Graph.prototype.getSinks = function() {
    if (this.sinks) {
        return this.sinks;
    }
    this.sinks = [];
    for (var i = 0; i < this.names.length; i++) {
        var edges = this.graph[this.names[i]];
        if (edges.length == 0) {
            this.sinks.push(this.nodes[this.names[i]]);
        }
    }
    return this.sinks;
}

/**
 * Given a dictionary mapping from node names to pagerank values, sets all of the
 * pageranks for the graph.  Assumes the names in the dictionary are the same as
 * the node names in the graph.
 */
Graph.prototype.setPageRanks = function(pageranks) {
    for (var i = 0; i < this.names.length; i++) {
        var node = this.nodes[this.names[i]];
        node.setPageRank(pageranks[this.names[i]]);
    }
}

/**
 * Takes the names of two nodes and returns true if there is an edge between them.
 * Note that this edge is assumed to be directed from nodeName1 to nodeName2.  For
 * an undirected graph, this assumes that the adjacency list representation contains
 * both directions of the edge.
 */
Graph.prototype.hasEdge = function(nodeName1, nodeName2) {
    if (this.graph[nodeName1]) {
        var edges = this.graph[nodeName1];
        return containsNode(edges, nodeName2);
    } 
    return false;
}

function containsNode(list, nodeName) {
    for (var i = 0; i < list.length; i++) {
        if (nodeName === list[i]) {
            return true;
        }
    }
    return false;
}

/**
 * Given a node name, returns the node object.
 */
Graph.prototype.getNode = function(nodeName) {
    return this.nodes[nodeName];
}

/**
 * Returns a list of the nodes sorted by pagerank.
 */
Graph.prototype.getRankedNodes = function() {
    var nodesList = [];
    for (var i = 0; i < this.names.length; i++) {
        nodesList.push(this.nodes[this.names[i]]);
    }
    return nodesList.sort(function(a, b) {
        return b.getPageRank() - a.getPageRank();
    });
}

function Node(id, name) {
    // ids must be unique per node.
    this.id = id;
    this.name = name;
}

Node.prototype.setPageRank = function(pagerank) {
    this.pagerank = pagerank;
}

Node.prototype.getPageRank = function() {
    if (this.pagerank) {
        return this.pagerank;
    }
    return null;
}

Node.prototype.getIn = function() {
    return this.inNodes;
}

Node.prototype.setIn = function(nodeList) {
    this.inNodes = nodeList;
}

Node.prototype.equals = function(otherNode) {
    return this.id === otherNode.id;
}
