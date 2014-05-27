function showGraph(){
	d3.selectAll(".edge")
		.attr("opacity", 1);
	d3.selectAll("circle").transition().delay(50)
		.attr("stroke", "black")
		.attr("stroke-width", 1)
		.attr("fill", function(d) { return colorScale(d.value) });
	d3.selectAll(".node")
		.style("cursor", "pointer")
		.attr("opacity", 1);
	d3.selectAll("#resetButton").remove();
}
