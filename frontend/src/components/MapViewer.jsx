import React from 'react';
import { Stage, Layer, Image, Circle, Text, Line, Group } from 'react-konva';
import useImage from 'use-image';

const MapViewer = ({ mapUrl, facilities = [], path = [], highlighted = {}, onNodeClick }) => {
  const [image, status] = useImage(mapUrl);
  const stageWidth = 800;
  const stageHeight = 600;

  // Safely generate points for the navigation line
  const getLinePoints = () => {
    const points = [];
    if (!path || !facilities) return points;

    path.forEach(nodeName => {
      const node = facilities.find(f => f.name === nodeName);
      if (node) {
        points.push((node.x / 100) * stageWidth);
        points.push((node.y / 100) * stageHeight);
      }
    });
    return points;
  };

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
          {/* Blueprint Image */}
          {image && <Image image={image} width={stageWidth} height={stageHeight} />}
          
          {/* Active Navigation Path Line */}
          {path?.length > 0 && (
            <Line
              points={getLinePoints()}
              stroke="#06b6d4"
              strokeWidth={8}
              lineCap="round"
              lineJoin="round"
              shadowColor="rgba(6, 182, 212, 0.5)"
              shadowBlur={10}
            />
          )}

          {/* All Facility Nodes (Selectable) */}
          {(facilities || []).map((fac, index) => {
            const isStart = highlighted.start === fac.name;
            const isEnd = highlighted.end === fac.name;
            const inPath = path?.includes(fac.name);

            // Determine if it should be fully highlighted, faintly visible, or hidden based on state
            let dotColor = "rgba(71, 85, 105, 0.4)"; // Faint slate for unselected
            let dotRadius = 6;
            let dotStroke = "rgba(255, 255, 255, 0.3)";
            let strokeWidth = 1;
            let showLabel = false;

            if (isStart) {
              dotColor = "#10b981"; // Emerald
              dotRadius = 14;
              dotStroke = "white";
              strokeWidth = 3;
              showLabel = true;
            } else if (isEnd) {
              dotColor = "#ef4444"; // Red
              dotRadius = 14;
              dotStroke = "white";
              strokeWidth = 3;
              showLabel = true;
            } else if (inPath) {
              dotColor = "#06b6d4"; // Cyan
              dotRadius = 10;
              dotStroke = "white";
              strokeWidth = 2;
              showLabel = true;
            }

            return (
              <Group 
                key={index} 
                onClick={() => onNodeClick && onNodeClick(fac.name)}
                onTap={() => onNodeClick && onNodeClick(fac.name)}
                onMouseEnter={(e) => {
                  const container = e.target.getStage().container();
                  container.style.cursor = 'pointer';
                }}
                onMouseLeave={(e) => {
                  const container = e.target.getStage().container();
                  container.style.cursor = 'grab';
                }}
              >
                <Circle
                  x={(fac.x / 100) * stageWidth}
                  y={(fac.y / 100) * stageHeight}
                  radius={dotRadius}
                  fill={dotColor}
                  stroke={dotStroke}
                  strokeWidth={strokeWidth}
                  shadowColor={isStart || isEnd || inPath ? "rgba(0,0,0,0.5)" : "transparent"}
                  shadowBlur={isStart || isEnd || inPath ? 5 : 0}
                />
                {(showLabel) && (
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
        </Layer>
      </Stage>
      <div className="bg-slate-800 p-3 text-center border-t border-slate-700">
        <p className="text-slate-400 text-xs italic">🖱️ Drag to explore • Click nodes to set Start/End points</p>
      </div>
    </div>
  );
};

export default MapViewer;