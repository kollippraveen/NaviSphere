import React from 'react';
import { Stage, Layer, Image, Circle, Text, Line, Group } from 'react-konva';
import useImage from 'use-image';

const MapViewer = ({ mapUrl, facilities = [], path = [], highlighted = {}, onNodeClick }) => {
  const [image, status] = useImage(mapUrl);
  const stageWidth = 800;
  const stageHeight = 600;

  // Convert a node name to pixel coords — searches the full list (including hidden waypoints)
  const nodeToPixel = (nodeName) => {
    const node = facilities.find(f => f.name === nodeName);
    if (!node) return null;
    return [(node.x / 100) * stageWidth, (node.y / 100) * stageHeight];
  };

  // Build the flat [x,y,x,y,...] array for the Konva Line.
  // The last coordinate is forcibly clamped to the destination node's exact
  // pixel position so the blue line never overshoots the red endpoint marker,
  // regardless of Konva's internal cap/join rendering.
  const getLinePoints = () => {
    const points = [];
    if (!path || !facilities) return points;
    path.forEach(nodeName => {
      const px = nodeToPixel(nodeName);
      if (px) { points.push(px[0]); points.push(px[1]); }
    });

    // Clamp: replace the very last x,y pair with the destination node's
    // exact coordinates so no rounding or cap extension can overshoot it.
    if (points.length >= 2 && highlighted?.end) {
      const endFac = facilities.find(f => f.name === highlighted.end);
      if (endFac) {
        points[points.length - 2] = (endFac.x / 100) * stageWidth;
        points[points.length - 1] = (endFac.y / 100) * stageHeight;
      }
    }

    return points;
  };

  // Visible (non-hidden) facilities — for the interactive node dots
  const visibleFacilities = (facilities || []).filter(fac => !fac.isHidden);

  // Look up start / end nodes in the FULL list (hidden nodes included) so markers
  // always render even if the selected node is an internal waypoint.
  const startNode = facilities.find(f => f.name === highlighted.start);
  const endNode   = facilities.find(f => f.name === highlighted.end);

  return (
    <div className="border-4 border-slate-700 rounded-[2rem] overflow-hidden bg-slate-100 shadow-2xl relative">
      {status === 'loading' && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-800/80 z-10 text-white">
          <p className="text-xl font-bold animate-pulse">Loading Blueprint...</p>
        </div>
      )}
      {status === 'failed' && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-800/80 z-10 text-white">
           <p className="text-xl font-bold text-red-400">Failed to load {mapUrl}</p>
        </div>
      )}

      <Stage width={stageWidth} height={stageHeight} draggable className="cursor-grab active:cursor-grabbing">
        <Layer>
          {/* ── Blueprint Image ─────────────────────────────────────────── */}
          {image && <Image image={image} width={stageWidth} height={stageHeight} />}

          {/* ── Pass 1: Navigation Path Line ────────────────────────────
              lineCap="butt" stops the line EXACTLY at the destination
              coordinate so it never visually extends past the red marker. */}
          {path?.length > 0 && (
            <Line
              points={getLinePoints()}
              stroke="#06b6d4"
              strokeWidth={8}
              lineCap="butt"
              lineJoin="miter"
              tension={0}
              shadowColor="rgba(6, 182, 212, 0.5)"
              shadowBlur={10}
            />
          )}

          {/* ── Pass 2: Intermediate cyan path dots ─────────────────────
              Start and End nodes are excluded here and rendered separately
              in Pass 3, ensuring the green/red markers always sit ON TOP. */}
          {visibleFacilities.map((fac, index) => {
            const isStart = highlighted.start === fac.name;
            const isEnd   = highlighted.end   === fac.name;
            // Skip start/end — dedicated overlay pass below handles them
            if (isStart || isEnd) return null;

            const inPath = path?.includes(fac.name);
            let dotColor    = "rgba(71, 85, 105, 0.4)";
            let dotRadius   = 6;
            let dotStroke   = "rgba(255, 255, 255, 0.3)";
            let strokeWidth = 1;
            let showLabel   = false;

            if (inPath) {
              dotColor    = "#06b6d4";
              dotRadius   = 10;
              dotStroke   = "white";
              strokeWidth = 2;
              showLabel   = true;
            }

            return (
              <Group
                key={index}
                onClick={() => onNodeClick && onNodeClick(fac.name)}
                onTap={() => onNodeClick && onNodeClick(fac.name)}
                onMouseEnter={(e) => { e.target.getStage().container().style.cursor = 'pointer'; }}
                onMouseLeave={(e) => { e.target.getStage().container().style.cursor = 'grab'; }}
              >
                <Circle
                  x={(fac.x / 100) * stageWidth}
                  y={(fac.y / 100) * stageHeight}
                  radius={dotRadius}
                  fill={dotColor}
                  stroke={dotStroke}
                  strokeWidth={strokeWidth}
                  shadowColor={inPath ? "rgba(0,0,0,0.5)" : "transparent"}
                  shadowBlur={inPath ? 5 : 0}
                />
                {showLabel && (
                  <Text
                    x={(fac.x / 100) * stageWidth + 15}
                    y={(fac.y / 100) * stageHeight - 15}
                    text={fac.name}
                    fill="#1e293b"
                    fontSize={15}
                    fontStyle="bold"
                    shadowColor="white"
                    shadowBlur={4}
                    shadowOffset={{ x: 1, y: 1 }}
                  />
                )}
              </Group>
            );
          })}

          {/* ── Pass 3: Start marker (green) — always on top ────────────
              Rendered LAST so it is never buried under the path line
              or a cyan intermediate dot. */}
          {startNode && (() => {
            const px = nodeToPixel(startNode.name);
            if (!px) return null;
            return (
              <Group key="__start__">
                <Circle
                  x={px[0]} y={px[1]}
                  radius={14} fill="#10b981"
                  stroke="white" strokeWidth={3}
                  shadowColor="rgba(0,0,0,0.6)" shadowBlur={8}
                />
                <Text
                  x={px[0] + 18} y={px[1] - 16}
                  text={startNode.name}
                  fill="#1e293b" fontSize={15} fontStyle="bold"
                  shadowColor="white" shadowBlur={4} shadowOffset={{ x: 1, y: 1 }}
                />
              </Group>
            );
          })()}

          {/* ── Pass 3b: End marker (red) — always on top ───────────────
              Rendered LAST so the red destination dot is never obscured. */}
          {endNode && (() => {
            const px = nodeToPixel(endNode.name);
            if (!px) return null;
            return (
              <Group key="__end__">
                <Circle
                  x={px[0]} y={px[1]}
                  radius={14} fill="#ef4444"
                  stroke="white" strokeWidth={3}
                  shadowColor="rgba(0,0,0,0.6)" shadowBlur={8}
                />
                <Text
                  x={px[0] + 18} y={px[1] - 16}
                  text={endNode.name}
                  fill="#1e293b" fontSize={15} fontStyle="bold"
                  shadowColor="white" shadowBlur={4} shadowOffset={{ x: 1, y: 1 }}
                />
              </Group>
            );
          })()}
        </Layer>
      </Stage>

      <div className="bg-slate-800 p-3 text-center border-t border-slate-700">
        <p className="text-slate-400 text-xs italic">🖱️ Drag to explore • Click nodes to set Start/End points</p>
      </div>
    </div>
  );
};

export default MapViewer;