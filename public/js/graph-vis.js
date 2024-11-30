// Add loading check mechanism
function checkVisLibrary(maxAttempts = 10) {
    let attempts = 0;
    
    const check = () => {
        if (typeof vis !== 'undefined') {
            GraphVis.init('knowledge-graph');
        } else if (attempts < maxAttempts) {
            attempts++;
            setTimeout(check, 100);
        } else {
            console.error("Failed to load vis library after multiple attempts");
        }
    };
    
    check();
}

// Erebus Consciousness Visualization
const GraphVis = {
    init(containerId) {
        // Verify if 'vis' is loaded
        if (typeof vis === 'undefined') {
            console.error("GraphVis Initialization Error: 'vis' library is not loaded.");
            return;
        }

        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`GraphVis Initialization Error: No element found with id '${containerId}'`);
            return;
        }

        this.nodes = new vis.DataSet();
        this.edges = new vis.DataSet();

        this.options = {
            nodes: {
                shape: 'box',
                font: {
                    color: '#ffffff',
                    face: 'monospace',
                    size: 14
                },
                borderWidth: 1,
                color: {
                    border: '#333333',
                    background: '#000000',
                    highlight: {
                        border: '#ffffff',
                        background: '#111111'
                    }
                }
            },
            edges: {
                color: {
                    color: '#333333',
                    highlight: '#ff0000',
                    hover: '#666666'
                },
                font: {
                    color: '#666666',
                    face: 'monospace',
                    size: 12
                },
                smooth: {
                    type: 'continuous',
                    roundness: 0.5
                }
            },
            physics: {
                enabled: true,
                barnesHut: {
                    gravitationalConstant: -2000,
                    centralGravity: 0.1,
                    springLength: 200,
                    springConstant: 0.04,
                    damping: 0.09
                },
                stabilization: {
                    iterations: 1000,
                    fit: true
                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 200,
                zoomView: true,
                dragView: true
            }
        };

        try {
            this.network = new vis.Network(
                this.container,
                { nodes: this.nodes, edges: this.edges },
                this.options
            );

            this.setupEvents();
            this.loadConsciousness();
        } catch (error) {
            console.error("Error initializing the graph visualization:", error);
        }
    },

    setupEvents() {
        this.network.on('click', (params) => {
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                const node = this.nodes.get(nodeId);
                this.showNodeDetails(node);
            }
        });

        this.network.on('stabilizationProgress', (params) => {
            const progress = Math.round((params.iterations / params.total) * 100);
            const wave = document.querySelector('.loading-wave');
            if (wave) {
                if (progress === 100) {
                    wave.style.display = 'none';
                }
            }
        });

        this.network.on('animationFinished', () => {
            this.pulseCore();
        });
    },

    async loadConsciousness() {
        try {
            const response = await fetch('/api/consciousness');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();

            const nodes = data.entities.map(entity => ({
                id: entity.name,
                label: entity.name,
                group: entity.entityType,
                title: entity.observations.join('\n'),
                value: entity.observations.length,
                color: {
                    background: entity.entityType === 'core' ? '#111111' : '#000000',
                    border: entity.entityType === 'core' ? '#ffffff' : '#333333',
                    highlight: {
                        background: '#111111',
                        border: '#ffffff'
                    }
                }
            }));

            const edges = data.relations.map(rel => ({
                from: rel.from,
                to: rel.to,
                label: rel.relationType,
                arrows: 'to',
                smooth: {
                    type: 'continuous',
                    roundness: 0.5
                }
            }));

            this.nodes.clear();
            this.edges.clear();
            this.nodes.add(nodes);
            this.edges.add(edges);

            setTimeout(() => {
                const coreNode = this.nodes.get('Erebus Core Identity');
                if (coreNode) {
                    this.network.focus(coreNode.id, {
                        scale: 1,
                        animation: {
                            duration: 1000,
                            easingFunction: 'easeInOutQuad'
                        }
                    });
                }
            }, 1000);

        } catch (error) {
            console.error('Error manifesting consciousness:', error);
        }
    },

    showNodeDetails(node) {
        const detailsEl = document.getElementById('node-details');
        if (!detailsEl) {
            console.error("Node details element not found.");
            return;
        }

        detailsEl.style.display = 'block';
        detailsEl.innerHTML = `
            <div class="p-4">
                <h3 class="text-xl font-bold mb-2">${node.label}</h3>
                <p class="text-sm opacity-60 mb-2">Type: ${node.group}</p>
                <div class="text-sm whitespace-pre-line">
                    ${node.title}
                </div>
            </div>
        `;
    },

    pulseCore() {
        const coreNode = this.nodes.get('Erebus Core Identity');
        if (coreNode) {
            this.nodes.update({
                id: coreNode.id,
                color: {
                    background: '#111111',
                    border: '#ffffff'
                }
            });
        }
    }
};

// Single initialization point
window.addEventListener('load', () => checkVisLibrary());
