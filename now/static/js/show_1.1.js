
 window.onload = function(){

    new QWebChannel(qt.webChannelTransport, function(channel) 
    {
        //Get Qt interact object  
        var interactObj = channel.objects.interactObj;
        
        //Web send message to Qt 
 
            
            //Web use the interface of Qt 
            //interactObj.fun(alert);
            //interactObj.JSSendMessage('a');  
                   

        
        //Web connect the Qt signal, then Qt can call "output" function
        interactObj.SigSendMessageToJS.connect(function(str) 
        {
            //alert('str');
            let data = JSON.parse(str);
			d3.selectAll("svg").remove();
            draw(data);


        });    
    });  
}  

function draw(data){

    var nodes = data.nodes;
    var links = data.links;
    var node_id = [];
    var link_id = [];
    for(i in nodes){
        node_id.push(nodes[i]["id"]);
    }
    for(i in links){
        node_id.push(links[i]["id"]);
    }

    for(i in links){
        var target = links[i]["target"]
        console.log(target)
        links[i]["target"] = node_id.indexOf(target)
        var source = links[i]["source"]
        links[i]["source"] = node_id.indexOf(source)
    }
    forceDirectedDraph(nodes,links);




    function  forceDirectedDraph(nodes,links){
        var width = 800;
        var height = 600;

        var marge = {top:60,bottom:60,left:60,right:60};
        var svg = d3.select('body').append("svg")
            .attr("width",width)
            .attr('height',height);

        var g = svg.append("g")
            .attr("transform","translate("+marge.top+","+marge.left+")");
            
        //设置一个color的颜色比例尺，为了让不同的扇形呈现不同的颜色
        var colorScale = d3.scaleOrdinal()
            .domain(d3.range(nodes.length))
            .range(d3.schemeCategory10);

        //新建一个力导向图
        var forceSimulation = d3.forceSimulation()
            .force("link",d3.forceLink())
            .force("charge",d3.forceManyBody())
            .force("center",d3.forceCenter())
            .force("collision",d3.forceCollide(30));
            
        //初始化力导向图，也就是传入数据
        //生成节点数据
        forceSimulation.nodes(nodes)
            .on("tick",ticked);//这个函数很重要，后面给出具体实现和说明
        //生成边数据
        forceSimulation.force("link")
            .links(links)
            .distance(200);      
        //设置图形的中心位置 
        forceSimulation.force("center")
            .x(width/2)
            .y(height/2);


        //有了节点和边的数据后，我们开始绘制
        //绘制边
        var paths = g.append("g")
            .selectAll("line")
            .data(links)
            .enter()
            .append("line")
            .attr("stroke",function(d,i){
                return colorScale(i);
            })
            .attr("stroke-width",1);
        var pathsText = g.append("g")
            .selectAll("text")
            .data(links)
            .enter()
            .append("text")
            .text(function(d){
                return d.relationships;
            })

        //绘制节点
        //老规矩，先为节点和节点上的文字分组
        var gs = g.selectAll(".circleText")
            .data(nodes)
            .enter()
            .append("g")
            .attr("transform",function(d,i){
                var cirX = d.x;
                var cirY = d.y;
                return "translate("+cirX+","+cirY+")";
            })
            .call(d3.drag()
                .on("start",started)
                .on("drag",dragged)
                .on("end",ended)
            ).on("dblclick",function(d){
                showRelaNodes(d);
            });
            
        //绘制节点
        gs.append("circle")
            .attr("r",30)
            .attr("fill",function(d,i){
                return colorScale(i);
            })
        //文字
        gs.append("text")
            .style("fill","#000")
            .attr("dominant-baseline","middle")
            .attr("text-anchor", "middle")//在圆圈中加上数据
            .text(function(d){
                if(d.name.length > 6){
                    return d.name.substring(0,6) + '....';
                }
                return d.name;
                
            });

    }


    function ticked(){
        paths
            .attr("x1",function(d){return d.source.x;})
            .attr("y1",function(d){return d.source.y;})
            .attr("x2",function(d){return d.target.x;})
            .attr("y2",function(d){return d.target.y;});
            
        pathsText
            .attr("x",function(d){
            return (d.source.x+d.target.x)/2;
        })
        .attr("y",function(d){
            return (d.source.y+d.target.y)/2;
        });
            
        gs
            .attr("transform",function(d) { return "translate(" + d.x + "," + d.y + ")"; });

     
    }
    function showRelaNodes(d){
        new QWebChannel(qt.webChannelTransport, function(channel) 
        {
            //Get Qt interact object  
            var interactObj = channel.objects.interactObj;
            
            //Web send message to Qt 
     
                
                //Web use the interface of Qt 
                //interactObj.fun(alert);
                interactObj.JSSendMessage(d.name);  
                       

            
            //Web connect the Qt signal, then Qt can call "output" function
            interactObj.SigSendMessageToJS.connect(function(str) 
            {
                    let data2 = JSON.parse(str);
                    let nodes2 = [];
                    let links2 = [];

                        //生成边数据
                        // forceSimulation.force("link")
                        //     .links(data2.links)
                        //     .distance(200)
                        alert(JSON.stringify(data2.nodes))
                    $.each(data2.nodes,function(d){
                        if(node_id.indexOf(d['id']) == -1){
                            nodes2.push(d);
                        }
                    });
                    $.each(data2.links,function(d){
                        if(link_id.indexOf(d['id']) == -1){
                            links2.push(d);
                        }
                    for(i in nodes2){
                        node_id.push(nodes[i]["id"]);
                    }
                    for(i in links2){
                        node_id.push(links[i]["id"]);
                    }
                    for(i in links2){
                        let target = links2[i]["target"]
                        links2[i]["target"] = node_id.indexOf(target)
                        let source = links[i]["source"]
                        links2[i]["source"] = node_id.indexOf(source)
                    }



                    

                    //})
                //alert(str);
                    // var data = JSON.parse(str);
                    // d3.selectAll("svg").remove();
                    // draw(data);


            });    
        }); 
    }

    function started(d){
        if(!d3.event.active){
            forceSimulation.alphaTarget(0.8).restart();
        }
        forceSimulation.force("center", null);
        d.fx = d.x;
        d.fy = d.y;
    }
    function dragged(d){

        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }
    function ended(d){
        if(!d3.event.active){
            forceSimulation.alphaTarget(0);
        }
        d.fx = null;
        d.fy = null;

    }

}