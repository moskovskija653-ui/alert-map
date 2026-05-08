const bounds = L.latLngBounds(L.latLng(25, 5), L.latLng(90, 210));
const map = L.map('map', { 
    attributionControl: false,
    minZoom: 4,
    maxZoom: 8,
    maxBounds: bounds,
    maxBoundsViscosity: 0.5
}).setView([55.75, 37.61], 5);

let geoJsonLayer, crimeaLayer;
const firebaseURL = "https://alertrussiamap-default-rtdb.europe-west1.firebasedatabase.app/alerts.json";

function createPatterns() {
    const svg = document.querySelector('#map svg');
    if (!svg) return setTimeout(createPatterns, 100);
    let defs = svg.querySelector('defs') || svg.appendChild(document.createElementNS("http://www.w3.org/2000/svg", "defs"));
    
    const makeStripe = (id, color, opacity = "0.4") => {
        let p = document.createElementNS("http://www.w3.org/2000/svg", "pattern");
        p.setAttribute('id', id);
        p.setAttribute('patternUnits', 'userSpaceOnUse');
        p.setAttribute('width', '10');
        p.setAttribute('height', '10');
        p.setAttribute('patternTransform', 'rotate(45)');
        p.innerHTML = `<line x1="0" y1="0" x2="0" y2="10" stroke="${color}" stroke-width="3" opacity="${opacity}" />`;
        defs.appendChild(p);
    };
    makeStripe('stripeWhite', '#ffffff');
    makeStripe('stripeRed', '#ff0000', "0.6");
}

function getStyle(status, isCrimea = false) {
    let style = { fillColor: "#343a40", weight: 1.2, opacity: 1, color: '#111', fillOpacity: 1 };
    if (status === "danger") {
        style.fillColor = isCrimea ? "url(#stripeRed)" : "#b91c1c";
    } else {
        style.fillColor = isCrimea ? "url(#stripeWhite)" : "#4b5563";
    }
    return style;
}

async function refreshStatuses() {
    try {
        const res = await fetch(firebaseURL + "?t=" + Date.now());
        const statusData = await res.json();
        if (!statusData) return;

        if (statusData.Crimea && crimeaLayer) {
            crimeaLayer.setStyle(getStyle(statusData.Crimea, true));
        }

        if (geoJsonLayer) {
            geoJsonLayer.eachLayer(l => {
                const props = l.feature.properties;
                const allNames = [props.name, props.name_ru, props.russian_name].filter(Boolean).map(n => n.toLowerCase());
                
                for (let key in statusData) {
                    const searchKey = key.toLowerCase();
                    const isMatch = allNames.some(name => name.includes(searchKey));
                    if (isMatch) {
                        l.setStyle(getStyle(statusData[key]));
                    }
                }
            });
        }
    } catch (e) { console.error("Firebase Error:", e); }
}

async function init() {
    loadBackgroundMask();
    createPatterns();
    
    const geoData = await fetch("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/russia.geojson").then(r => r.json());

    geoJsonLayer = L.geoJSON(geoData, {
        style: () => getStyle("safe"),
        onEachFeature: (f, layer) => {
            const displayName = f.properties.name_ru || f.properties.name;
            layer.bindTooltip(displayName, { sticky: true, className: 'leaflet-tooltip-own' });
        }
    }).addTo(map);

    const crimeaCoords = [[46.166, 33.682], [46.183, 33.729], [46.136, 33.791], [46.069, 33.821], [46.052, 33.914], [46.101, 34.116], [46.101, 34.254], [46.052, 34.341], [45.981, 34.502], [45.922, 34.694], [45.908, 34.793], [45.782, 34.821], [45.698, 34.884], [45.578, 34.919], [45.501, 35.004], [45.495, 35.158], [45.482, 35.341], [45.394, 35.495], [45.334, 35.612], [45.352, 35.794], [45.452, 35.941], [45.482, 36.102], [45.493, 36.251], [45.474, 36.421], [45.434, 36.635], [45.378, 36.654], [45.302, 36.551], [45.241, 36.471], [45.184, 36.424], [45.105, 36.416], [45.031, 36.384], [45.021, 36.216], [45.032, 36.054], [45.048, 35.836], [45.121, 35.641], [45.074, 35.482], [45.011, 35.385], [44.954, 35.214], [44.891, 35.104], [44.832, 34.962], [44.811, 34.854], [44.782, 34.721], [44.714, 34.541], [44.697, 34.411], [44.642, 34.341], [44.582, 34.302], [44.492, 34.184], [44.441, 34.141], [44.406, 34.058], [44.394, 33.914], [44.386, 33.729], [44.404, 33.641], [44.453, 33.522], [44.484, 33.484], [44.552, 33.454], [44.591, 33.421], [44.641, 33.484], [44.704, 33.521], [44.756, 33.551], [44.852, 33.594], [44.952, 33.594], [45.045, 33.521], [45.121, 33.441], [45.195, 33.284], [45.281, 33.214], [45.324, 33.004], [45.334, 32.784], [45.321, 32.501], [45.341, 32.484], [45.414, 32.504], [45.482, 32.614], [45.541, 32.741], [45.592, 32.884], [45.654, 32.954], [45.748, 33.211], [45.852, 33.341], [45.952, 33.484], [46.041, 33.584], [46.155, 33.644], [46.166, 33.682]];
    
    crimeaLayer = L.polygon(crimeaCoords, getStyle("safe", true)).addTo(map);
    crimeaLayer.bindTooltip("Крым", { sticky: true, className: 'leaflet-tooltip-own' });

    refreshStatuses();
    setInterval(refreshStatuses, 15000); 
}

function loadBackgroundMask() {
    fetch("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson")
        .then(res => res.json())
        .then(worldData => {
            L.geoJSON(worldData, {
                style: () => ({ fillColor: "#1a1d21", fillOpacity: 1, weight: 0 }),
                interactive: false 
            }).addTo(map).bringToBack();
        });
}

init();
