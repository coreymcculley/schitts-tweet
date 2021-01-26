function gauge(pos_value){
    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 30, bottom: 40, left: 90},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;
    
    // append the svg object to the body of the page
    var svg = d3.select("#gauge_chart")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");
    
    // Parse the Data
    function(data) {
    
      // Add X axis
      var x = d3.scaleLinear()
        .domain([0, 100])
        .range([ 0, width]);
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
          .attr("transform", "translate(-10,0)rotate(-45)")
          .style("text-anchor", "end");
    
      // Y axis
      var y = d3.scaleBand()
        .range([ 0, height ])
        .domain(100)
        .padding(.1);
      svg.append("g")
        .call(d3.axisLeft(y))
    
      //Bars
      svg.selectAll("myRect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", x(0) )
        .attr("y", 'Positivity Rating')
        .attr("width", pos_value )
        .attr("height", 90)
        .attr("fill", "#69b3a2")
    
    
        // .attr("x", function(d) { return x(d.Country); })
        // .attr("y", function(d) { return y(d.Value); })
        // .attr("width", x.bandwidth())
        // .attr("height", function(d) { return height - y(d.Value); })
        // .attr("fill", "#69b3a2")
    
    }
}