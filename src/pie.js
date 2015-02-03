/* Copyright (C) 2014 Vincent Rabaud
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// This file displays pie chart using http://ocanvas.org/ which is under MIT license

$(document).ready(function () {

  // Function that goes over the .yaml file and gets data about each type
  // The output is a set of callbacks that will be waited for to get stats
  function getStats() {
    // Go over the data and get some stats about the institutes
    var REGIONS = ['america', 'asia', 'australia', 'europe']
    var PATTERN = 'data/'; //%s.yaml'
    // parse each yaml file
    var callbacks = [];
    for(var region = 0; region < 4; ++region) {
      callbacks.push($.get(PATTERN + REGIONS[region] + '.yaml', {}, function(data) {
        // split the line
        var perLine=data.split('\n');
        for(var i=0;i<perLine.length;++i)
        {
          var line=perLine[i].split(' ');
          for(var j=0;j<line.length;++j) {
            // find the 'type:' property in the lines
            if (line[j] == 'type:') {
              var type = line.slice(j+1).join(' ');
              // increment the stats for that specific type in the global variable
              stats[type] += 1;
              break;
            }
          }
        }
      }, 'text'));
    }
    
    return callbacks;
  }

  function displayPie() {
    // Get the colors from the list
    var colors = [];
    $("#text li").each(function(index) {
      colors.push($(this).find("span").css('color'));
    });

    // Convert the stats in counts
    var counts = [ stats.school, stats.company, stats['research institute'], stats.other + stats.null ];
    // Normalize the stats
    var sum = 0;
    for(var type = 0; type < counts.length; ++type) {
      sum += counts[type];
    }

    // set the dimension of the pie chart
    var chart_width = $('#text').width();
    if (chart_width > 150)
      chart_width = 150;
    $('#pie_chart').prop('height', chart_width).prop('width', chart_width);

    var canvas = oCanvas.create({
      canvas: "#pie_chart",
    });

    var prototype = canvas.display.arc({
      x: canvas.width / 2,
      y: canvas.height / 2,
      radius: chart_width/2,
      pieSection: true
    });

    // Display each arc + text
    var lastEnd;
    for(var i = 0; i < counts.length; i++) {
      // Display the arc
      var angle_end = (i > 0 ? lastEnd : 0) + 360 / (sum / counts[i]) - (i < 1 ? 90 : 0);
      var angle_start = (i < 1 ? -90 : lastEnd);

      var arc = prototype.clone({
        start: angle_start,
        end: angle_end,
        fill: colors[i]
      });

      canvas.addChild(arc);
      lastEnd = angle_end;

      // Also add text
      var x = chart_width/2 + chart_width/2.75*Math.cos(((angle_end+angle_start)/2)/180*Math.PI);
      var y = chart_width/2 + chart_width/2.75*Math.sin(((angle_end+angle_start)/2)/180*Math.PI);
      var text = canvas.display.text({
        x: x,
        y: y,
        origin: { x: "center", y: "center" },
        font: "20px sans-serif",
        text: counts[i].toString(),
        fill: "#000"
      });

      canvas.addChild(text);
    };
  }

  // Once all loaded
  var stats = {'school':0, 'company':0, 'research institute':0, 'other':0, 'null':0};
  // retrieve data from the file ...
  var callbacks = getStats();

  // ... and display data once done
  $.when.apply(null, callbacks).done(displayPie);
});
