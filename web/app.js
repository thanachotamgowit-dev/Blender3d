import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/controls/OrbitControls.js';

const canvas = document.querySelector('#view');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf2f3f1);

const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 200);
camera.position.set(15, -17, 11);

const controls = new OrbitControls(camera, canvas);
controls.target.set(0, 0, 1.6);
controls.enableDamping = true;
controls.autoRotate = false;

scene.add(new THREE.HemisphereLight(0xffffff, 0x58635d, 2.0));
const sun = new THREE.DirectionalLight(0xffffff, 3.2);
sun.position.set(-8, -10, 15);
sun.castShadow = true;
scene.add(sun);

const ground = new THREE.Mesh(
  new THREE.PlaneGeometry(26, 26),
  new THREE.MeshStandardMaterial({ color: 0xdadfd9, roughness: 1 })
);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

const grid = new THREE.GridHelper(26, 26, 0x9aa39d, 0xc6cbc7);
grid.position.y = 0.002;
scene.add(grid);

const mats = {
  concrete: new THREE.MeshStandardMaterial({ color: 0x9d9f9d, roughness: 0.82 }),
  wall: new THREE.MeshStandardMaterial({ color: 0xf3f1eb, roughness: 0.9 }),
  wood: new THREE.MeshStandardMaterial({ color: 0x8a5734, roughness: 0.62 }),
  frame: new THREE.MeshStandardMaterial({ color: 0x242729, roughness: 0.4, metalness: 0.5 }),
  glass: new THREE.MeshPhysicalMaterial({ color: 0x8db8c5, transparent: true, opacity: 0.34, roughness: 0.1, transmission: 0.45 }),
  slab: new THREE.MeshStandardMaterial({ color: 0xb9bbb8, roughness: 0.8 })
};

const groups = {
  structure: new THREE.Group(),
  walls: new THREE.Group(),
  openings: new THREE.Group(),
  roof: new THREE.Group()
};
Object.entries(groups).forEach(([name, group]) => {
  group.name = name;
  scene.add(group);
});

function box(group, name, x, y, z, w, d, h, mat) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, d, h), mat);
  mesh.name = name;
  mesh.position.set(x, y, z);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  group.add(mesh);
  return mesh;
}

// Coordinates: X = width, Y = depth, Z = height.
const W = 10, D = 10, slabT = 0.15, wallT = 0.15, H = 3.0;

// Ground slab.
box(groups.structure, 'Ground_Slab', 0, 0, slabT / 2, W, D, slabT, mats.slab);

// Columns.
const columnPts = [
  [-4.5, -4.5], [0, -4.5], [4.5, -4.5],
  [-4.5, 0], [4.5, 0],
  [-4.5, 4.5], [0, 4.5], [4.5, 4.5]
];
columnPts.forEach(([x, y], i) => box(groups.structure, 'Column_' + (i + 1), x, y, slabT + H / 2, 0.3, 0.3, H, mats.concrete));

// Walls.
const zWall = slabT + H / 2;
box(groups.walls, 'Left_Wall', -W/2 + wallT/2, 0, zWall, wallT, D, H, mats.wall);
box(groups.walls, 'Right_Wall', W/2 - wallT/2, 0, zWall, wallT, D, H, mats.wall);
box(groups.walls, 'Rear_Wall', 0, D/2 - wallT/2, zWall, W, wallT, H, mats.wall);
box(groups.walls, 'Front_Left', -4.15, -D/2 + wallT/2, zWall, 1.7, wallT, H, mats.wall);
box(groups.walls, 'Front_Right', 4.15, -D/2 + wallT/2, zWall, 1.7, wallT, H, mats.wall);

// Internal room partitions.
box(groups.walls, 'Partition_A', -1.6, 2.5, zWall, wallT, 5.0, H, mats.wall);
box(groups.walls, 'Partition_B', 1.6, 2.5, zWall, wallT, 5.0, H, mats.wall);
box(groups.walls, 'Partition_C', 0, 1.1, zWall, 6.4, wallT, H, mats.wall);

// Front glazing and framing.
box(groups.openings, 'Front_Glass', 0, -4.965, slabT + 1.35, 5.8, 0.05, 2.4, mats.glass);
[-2.9, -1.45, 0, 1.45, 2.9].forEach((x, i) => box(groups.openings, 'Frame_' + i, x, -4.99, slabT + 1.35, 0.06, 0.10, 2.45, mats.frame));
box(groups.openings, 'Timber_Left', -3.15, -4.88, slabT + 1.35, 0.35, 0.22, 2.7, mats.wood);
box(groups.openings, 'Timber_Right', 3.15, -4.88, slabT + 1.35, 0.35, 0.22, 2.7, mats.wood);

// Roof slab + parapet.
const roofZ = slabT + H + slabT / 2;
box(groups.roof, 'Roof_Slab', 0, 0, roofZ, W, D, slabT, mats.slab);
const pH = 0.45, pZ = slabT + H + slabT + pH/2;
box(groups.roof, 'Parapet_N', 0, D/2-wallT/2, pZ, W, wallT, pH, mats.wall);
box(groups.roof, 'Parapet_S', 0, -D/2+wallT/2, pZ, W, wallT, pH, mats.wall);
box(groups.roof, 'Parapet_E', W/2-wallT/2, 0, pZ, wallT, D, pH, mats.wall);
box(groups.roof, 'Parapet_W', -W/2+wallT/2, 0, pZ, wallT, D, pH, mats.wall);

// Terrace slab.
box(groups.structure, 'Terrace', 0, -5.8, 0.08, 6.8, 1.6, 0.16, mats.slab);

let exploded = false;
function applyExplode() {
  groups.structure.position.z = exploded ? -0.6 : 0;
  groups.walls.position.z = exploded ? 0.9 : 0;
  groups.openings.position.z = exploded ? 1.8 : 0;
  groups.roof.position.z = exploded ? 3.2 : 0;
}

document.querySelector('#rotate').addEventListener('click', e => {
  controls.autoRotate = !controls.autoRotate;
  e.currentTarget.textContent = 'Auto Rotate: ' + (controls.autoRotate ? 'ON' : 'OFF');
});

document.querySelector('#roof').addEventListener('click', e => {
  groups.roof.visible = !groups.roof.visible;
  e.currentTarget.textContent = (groups.roof.visible ? 'Hide' : 'Show') + ' Roof';
});

document.querySelector('#explode').addEventListener('click', e => {
  exploded = !exploded;
  applyExplode();
  e.currentTarget.textContent = exploded ? 'Assembled View' : 'Exploded View';
});

document.querySelector('#reset').addEventListener('click', () => {
  camera.position.set(15, -17, 11);
  controls.target.set(0, 0, 1.6);
  controls.update();
});

function resize() {
  const r = canvas.getBoundingClientRect();
  const w = Math.max(1, r.width);
  const h = Math.max(1, r.height);
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}

function frame() {
  resize();
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(frame);
}
frame();
