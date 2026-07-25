import { useEffect, useRef } from "react";

const NODE_COLORS = {
  suspect: "#ef4444",
  fir: "#3b82f6",
  location: "#22c55e",
  evidence: "#eab308",
};

export default function CaseCanvas({ nodes, edges, onNodeClick }) {
  const svgRef = useRef(null);
  const simulationRef = useRef(null);

  useEffect(() => {
    const d3 = window.d3;
    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;

    svg.selectAll("*").remove();

    const container = svg.append("g");

    svg.call(
      d3.zoom()
        .scaleExtent([0.3, 4])
        .on("zoom", (event) => container.attr("transform", event.transform))
    );

    // Deep copy so D3 mutation doesn't fight React state
    const nodesCopy = nodes.map((n) => ({ ...n }));
    const edgesCopy = edges.map((e) => ({ ...e }));

    const simulation = d3
      .forceSimulation(nodesCopy)
      .force("link", d3.forceLink(edgesCopy).id((d) => d.id).distance(120))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(40));

    simulationRef.current = simulation;

    const link = container
      .append("g")
      .selectAll("line")
      .data(edgesCopy)
      .join("line")
      .attr("stroke", "#4b5563")
      .attr("stroke-width", 1.5);

    const linkLabel = container
      .append("g")
      .selectAll("text")
      .data(edgesCopy)
      .join("text")
      .text((d) => d.label || "")
      .attr("font-size", 9)
      .attr("fill", "#9ca3af");

    const node = container
      .append("g")
      .selectAll("circle")
      .data(nodesCopy)
      .join("circle")
      .attr("r", 22)
      .attr("fill", (d) => NODE_COLORS[d.type] || "#a3a3a3")
      .attr("stroke", "#111827")
      .attr("stroke-width", 2)
      .style("cursor", "pointer")
      .on("click", (event, d) => onNodeClick && onNodeClick(d))
      .call(
        d3
          .drag()
          .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    const label = container
      .append("g")
      .selectAll("text")
      .data(nodesCopy)
      .join("text")
      .text((d) => d.label || d.id)
      .attr("font-size", 10)
      .attr("fill", "#f3f4f6")
      .attr("text-anchor", "middle")
      .attr("dy", 35);

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      linkLabel
        .attr("x", (d) => (d.source.x + d.target.x) / 2)
        .attr("y", (d) => (d.source.y + d.target.y) / 2);

      node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
      label.attr("x", (d) => d.x).attr("y", (d) => d.y);
    });

    return () => simulation.stop();
  }, [nodes, edges]);

  return (
    <svg ref={svgRef} className="w-full h-full bg-gray-950" />
  );
}
