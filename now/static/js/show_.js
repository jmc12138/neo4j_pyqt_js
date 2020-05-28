
var nodes;
var links;

d3.json("../data/json/search_return.json",function(error,json){
    console.log('dwe')
    console.log(json)
    nodes = json.nodes
    links = json.links
})



index = []
for(iNode in nodes){
    index.push(nodes[iNode]["id"])
}
//console.log(index)
for(iLink in links){
    var target = links[iLink]["target"]
    console.log(target)
    links[iLink]["target"] = index.indexOf(target)
    var source = links[iLink]["source"]
    links[iLink]["source"] = index.indexOf(source)
}


 var edges = links


var marge = {top:60,bottom:60,left:60,right:60}
var svg = d3.select("svg")
var width = svg.attr("width")
var height = svg.attr("height")
var g = svg.append("g")
    .attr("transform","translate("+marge.top+","+marge.left+")");
    
//设置一个color的颜色比例尺，为了让不同的扇形呈现不同的颜色


//新建一个力导向图
var forceSimulation = d3.forceSimulation()
    .force("link",d3.forceLink())
    .force("charge",d3.forceManyBody())
    .force("center",d3.forceCenter());;
    
//初始化力导向图，也就是传入数据
//生成节点数据
forceSimulation.nodes(nodes)
    .on("tick",ticked);//这个函数很重要，后面给出具体实现和说明
//生成边数据
forceSimulation.force("link")
    .links(edges)
    .distance(200)      
//设置图形的中心位置 
forceSimulation.force("center")
    .x(width/2)
    .y(height/2);
//在浏览器的控制台输出
console.log(nodes);
console.log(edges);

//有了节点和边的数据后，我们开始绘制
//绘制边
var links = g.append("g")
    .selectAll("line")
    .data(edges)
    .enter()
    .append("line")
    .attr("stroke","black")
    .attr("stroke-width",1);
var linksText = g.append("g")
    .selectAll("text")
    .data(edges)
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
    );
    
//绘制节点
gs.append("circle")
    .attr("r",10)
    .attr("fill","pink")
//文字
gs.append("text")
    .attr("x",-10)
    .attr("y",-20)
    .attr("dy",10)
    .text(function(d){
        return d.name;
    })

function ticked(){
    links
        .attr("x1",function(d){return d.source.x;})
        .attr("y1",function(d){return d.source.y;})
        .attr("x2",function(d){return d.target.x;})
        .attr("y2",function(d){return d.target.y;});
        
    linksText
        .attr("x",function(d){
        return (d.source.x+d.target.x)/2;
    })
    .attr("y",function(d){
        return (d.source.y+d.target.y)/2;
    });
        
    gs
        .attr("transform",function(d) { return "translate(" + d.x + "," + d.y + ")"; });
}
function started(d){
    if(!d3.event.active){
        forceSimulation.alphaTarget(0.8).restart();
    }
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