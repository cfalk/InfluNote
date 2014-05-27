/* A very simple testing example that is run by testing.html.  You'll want
 * to put your more interesting tests here.
 */
test( "Graph", function() {
    // You'll need to write a file out to adjacency_list.json using graph_text_to_json.py.
    d3.json("adjacency_list.json", function(error, json) {
        if (error) return console.warn(error);
        var graph = new Graph(json);
        calculatePageRank(graph);  // You'll need to write this.
        console.log(graph.getRankedNodes());
        // Sadly, you can't actually put automatic checks here because it's in the callback.
    });
    // And you can't put them here either, since it's not in the callback so the data won't have
    // loaded.  So you'll need to do tests that don't require loading in the full graph, but
    // rather creating a small test graph by hand (which is what you should do anyway for tests).
    // You should mostly use this as a demo for how to get your data into Graph object form.
    expect(0);
});


