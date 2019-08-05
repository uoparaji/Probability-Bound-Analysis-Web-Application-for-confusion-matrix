$(document).ready(function() {

	$('form').on('submit', function(event) {
	       event.preventDefault(); 

		$.ajax({
			data : {
			prevType   : $('#prevType').val(),
				prev    : $('#prev').val(),
				truePos : $('#TP').val(),
				falsePos: $('#FP').val(),
				falseNeg: $('#FN').val(),
				trueNeg : $('#TN').val()
				

			},
			type : 'POST',
			url : '/process'
		})
		

		.done(function(data) {
		
		if (data.sensitivity_lower) {

    		$('#output').text(data.sensitivity_lower).show();
     	   $('#output1').text(data.sensitivity_upper).show();
     	   $('#output2').text(data.specificity_lower).show();
     	   $('#output3').text(data.specificity_upper).show();
     	   $('#output4').text(data.prevelance_lower).show();
     	   $('#output5').text(data.prevelance_upper).show();
     	   $('#output6').text(data.ppv_lower).show();
     	   $('#output7').text(data.ppv_upper).show();
     	   $('#output8').text(data.fpr_lower).show();
     	   $('#output9').text(data.fpr_upper).show();
     	   $('#output10').text(data.fnr_lower).show();
     	   $('#output11').text(data.fnr_upper).show();
     	   $('#output12').text(data.npv_lower).show();
     	   $('#output13').text(data.npv_upper).show();
     	   $('#output14').text(data.plr_lower).show();
     	   $('#output15').text(data.plr_upper).show();
     	   $('#output16').text(data.nlr_lower).show()
     	   $('#output17').text(data.nlr_upper).show();
     	   $('#ppv_lower').text(data.ppv_new_lower).show();
     	   $('#ppv_upper').text(data.ppv_new_upper).show();
     	   $('#npv_lower').text(data.npv_new_lower).show();
     	   $('#npv_upper').text(data.npv_new_lower).show();
     	   $('#k_param').text(data.k_param).show();
     	   $('#n_param').text(data.n_param).show();
     	   $('#k_param_opt').text(data.k_param_opt).show();
     	   $('#n_param_opt').text(data.n_param_opt).show();
     	   
		}
		
		console.log(data.ppv_new_left_x)
		
		document.getElementById("iFrame").src = 'http://www.iconarray.com/pictographs/embed?axis_endpoints=0&axis_font=Arial&axis_font_size=12&axis_format=%25n+---&axis_labels=1&axis_position=left&background_color=%23ffffff&cell_grouping=normal&cell_height=40&cell_spacing=5&cell_width=22&cols=10&icon=https%3A%2F%2Fs3.amazonaws.com%2Ficon-array%2Ficons%2Fmale.png&legend_font=Arial&legend_font_size=12&legend_position=right&legend_scale=1&risks_attributes%5B0%5D%5Bdescription%5D=out+of+100+people+don%27t+exhibit+this+property&risks_attributes%5B0%5D%5Bdisplay%5D=0&risks_attributes%5B0%5D%5Bhex%5D=%23DCDCDC&risks_attributes%5B1%5D%5Bdescription%5D=out+of+'+ Math.floor(data.n_param_opt) + '+people+exhibit+this+property&risks_attributes%5B1%5D%5Bdisplay%5D=1&risks_attributes%5B1%5D%5Bhex%5D=%2311AA89&risks_attributes%5B1%5D%5Bvalue%5D='+ Math.ceil(data.k_param_opt) +'&rows=10&title_alignment=left&title_font=Helvetica&title_font_size=18';

		// chart 1
      google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart1);

        function drawChart1() {
          var container = new google.visualization.DataTable();
          container.addColumn('string', 'x');
          container.addColumn('number', 'values');
          container.addColumn({id:'i0', type:'number', role:'interval'});
          container.addColumn({id:'i1', type:'number', role:'interval'});
          container.addRows([
              ['Sens', (data.sensitivity_lower +data.sensitivity_upper)/2, data.sensitivity_lower, data.sensitivity_upper],
              ['Spec', (data.specificity_lower +data.specificity_upper)/2, data.specificity_lower, data.specificity_upper],
              ['PPV1', (data.ppv_lower +data.ppv_upper)/2, data.ppv_lower, data.ppv_upper],
              ['PPV2', (data.ppv_new_lower +data.ppv_new_upper)/2, data.ppv_new_lower, data.ppv_new_upper],
              ['FPR', (data.fpr_lower +data.fpr_upper)/2, data.fpr_lower, data.fpr_upper],
              ['FNR', (data.fnr_lower +data.fnr_upper)/2, data.fnr_lower, data.fnr_upper],
              ['NPV1', (data.npv_lower +data.npv_upper)/2, data.npv_lower, data.npv_upper],
              ['NPV2', (data.npv_new_lower +data.npv_new_upper)/2, data.npv_new_lower, data.npv_new_upper],
              ['PLR', (data.plr_lower +data.plr_upper)/2, data.plr_lower, data.plr_upper],
              ['NLR', (data.nlr_lower +data.nlr_upper)/2, data.nlr_lower, data.nlr_upper]]);
  
        // The intervals data as narrow lines (useful for showing raw source data)
          /*var options = {vAxis: {viewWindow: {min: 0, max: 3},},
          
          chartArea: {
        backgroundColor: {
            stroke: '#000000',
            strokeWidth: 3
                       }
                   },
                    
          title: 'Hello',
          curveType:'function',
          lineWidth: 4,
          series: [{'color': '#1A8763'}],
          intervals: { 'lineWidth':2, 'barWidth': 0.5, style: 'boxes' },
          legend: 'none',
          vAxis: {
          title: 'values'
        },
            }; */
            
       var options_boxes_background = {
     
     'chartArea': {
    'backgroundColor': {
        'fill': '#F4F4F4',
        'opacity': 100
     },
       },
       vAxis: {
          title: 'values'
        },
        
        hAxis : { 
        textStyle : {
            fontSize: 20, 
            titleFontSize: 20
        }

    },

        title:'Confidence Box Approach',
        titleTextStyle: {
      color: '#000000',
      fontName: 'Arial',
      fontSize: 20
    },
          titlePosition: 'right',


        curveType:'function',
        lineWidth: 4,
        series: [{'color': '#1A8763'}],
        intervals: { 'lineWidth':2, 'barWidth': 0.5 },
        interval: {
            'i2': { 'style':'boxes', 'color':'grey', 'boxWidth': 2.5,
            'lineWidth': 0, 'fillOpacity': 0.2 }
        },
        legend: 'none',
    };
  
          var chart_lines = new google.visualization.LineChart(document.getElementById('chart_lines2'));
          chart_lines.draw(container, options_boxes_background);
      }
    
    
    // end chart 1
    
const group_data_left = new Array(data.ppv_new_left_x.length).fill(null).map((i, idx) => [data.ppv_new_left_x[idx], data.ppv_new_left_support[idx]])
const group_data_right = new Array(data.ppv_new_right_x.length).fill(null).map((i, idx) => [data.ppv_new_right_x[idx], data.ppv_new_right_support[idx]])


const group_data_left2 = new Array(data.npv_new_left_x.length).fill(null).map((i, idx) => [data.npv_new_left_x[idx], data.npv_new_left_support[idx]])
const group_data_right2 = new Array(data.npv_new_right_x.length).fill(null).map((i, idx) => [data.npv_new_right_x[idx], data.npv_new_right_support[idx]])    
// icon array stuff

// chart 2
function drawChart2() {
    var data1 = new google.visualization.DataTable();
    data1.addColumn('number', 'X');
    data1.addColumn('number', 'LB PPV');
    
    data1.addRows(group_data_left);
    
    var data2 = new google.visualization.DataTable();
    data2.addColumn('number', 'X');
    data2.addColumn('number', 'UB PPV');
    
    data2.addRows(group_data_right);
    
    var joinedData = google.visualization.data.join(data1, data2, 'full', [[0, 0]], [1], [1]);
    
    var chart = new google.visualization.LineChart(document.getElementById('chart_lines3'));
    
    
    
    chart.draw(joinedData, {
        height: 300,
        width: 400,
        interpolateNulls: true
    });
}
google.load('visualization', '1', {packages:['corechart'], callback: drawChart2});

// end chart 2		 


// chart 3
function drawChart3() {
    var data1 = new google.visualization.DataTable();
    data1.addColumn('number', 'X');
    data1.addColumn('number', 'LB NPV');
    
    data1.addRows(group_data_left2);
    
    var data2 = new google.visualization.DataTable();
    data2.addColumn('number', 'X');
    data2.addColumn('number', 'UB NPV');
    
    data2.addRows(group_data_right2);
    
    var joinedData = google.visualization.data.join(data1, data2, 'full', [[0, 0]], [1], [1]);
    
    var chart = new google.visualization.LineChart(document.getElementById('chart_lines4'));
    
    
    chart.draw(joinedData, {
        height: 300,
        width: 400,
        interpolateNulls: true
    });
}
google.load('visualization', '1', {packages:['corechart'], callback: drawChart3});

// end chart 2	
		});

		

	});
	
});








