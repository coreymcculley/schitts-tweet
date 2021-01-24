function gauge_line(pos_value){
    anychart.onDocumentReady(function () {

        // create data
        var data = [pos_value*100];
    
        // set the gauge type
        var gauge = anychart.gauges.linear();
    
        // set the data for the gauge
        gauge.data(data);
    
        // set the layout
        gauge.layout('horizontal');
    
        // create a color scale
        var scaleBarColorScale = anychart.scales.ordinalColor().ranges(
        [
            {
                from: 0,
                to: 33,
                color: ['#D81E05', '#FFD700']
            },
            {
                from: 33,
                to: 66,
                color: ['#FFD700', '#CAD70b']
            },
            {
                from: 66,
                to: 100,
                color: ['#CAD70b', '#00FF00']
            }
        ]
        );
    
        // create a Scale Bar
        var scaleBar = gauge.scaleBar(0);
    
        // set the height and offset of the Scale Bar (both as percentages of the gauge height)
        scaleBar.width('5%');
        scaleBar.offset('31.5%');
    
        // use the color scale (defined earlier) as the color scale of the Scale Bar
        scaleBar.colorScale(scaleBarColorScale);
    
        // add a marker pointer
        var marker = gauge.marker(0);
    
        // set the offset of the pointer as a percentage of the gauge width
        marker.offset('31.5%');
    
        // set the marker type
        marker.type('triangle-up');
    
        // set the zIndex of the marker
        marker.zIndex(10);
    
        // configure the scale
        var scale = gauge.scale();
        scale.minimum(0);
        scale.maximum(100);
        scale.ticks().interval(20);
    
        // configure the axis
        var axis = gauge.axis();
        axis.minorTicks(true)
        axis.minorTicks().stroke('#cecece');
        axis.width('1%');
        axis.offset('29.5%');
        axis.orientation('top');
    
        // format axis labels
        axis.labels().format('{%value}%');
    
        // set paddings
        gauge.padding([0, 50]);
    
        // set the container id
        gauge.container('container');
    
        // initiate drawing the gauge
        gauge.draw();
    });
}