import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/loaders/GLTFLoader.js';

const canvas = document.querySelector('#view');
const status = document.querySelector('#status');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf1f3f5);

const camera = new THREE.PerspectiveCamera(45, 1, 0.01, 100000);
camera.position.set(12, -12, 8);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.autoRotate = false;

scene.add(new THREE.HemisphereLight(0xffffff, 0x66707a, 2.2));
const sun = new THREE.DirectionalLight(0xffffff, 2.5);
sun.position.set(20, -30, 40);
scene.add(sun);

const grid = new THREE.GridHelper(100, 100);
scene.add(grid);

const loader = new GLTFLoader();
let model = null;

function fitCamera(object) {
  const box = new THREE.Box3().setFromObject(object);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  const maxDim = Math.max(size.x, size.y, size.z) || 1;
  const dist = maxDim * 1.6;
  controls.target.copy(center);
  camera.position.set(center.x + dist, center.y - dist, center.z + dist * 0.65);
  camera.near = Math.max(maxDim / 10000, 0.01);
  camera.far = maxDim * 100;
  camera.updateProjectionMatrix();
  controls.update();
}

function showGltf(gltf, label) {
  if (model) scene.remove(model);
  model = gltf.scene;
  scene.add(model);
  fitCamera(model);
  status.textContent = 'โหลดแล้ว: ' + label;
}

function loadUrl(url, label) {
  status.textContent = 'กำลังโหลด...';
  loader.load(url, gltf => showGltf(gltf, label), undefined, err => {
    console.error(err);
    status.textContent = 'ยังไม่มีโมเดล GLB บนเว็บ หรือโหลดไม่สำเร็จ';
  });
}

document.querySelector('#load-default').addEventListener('click', () => {
  loadUrl('./models/NPT_Triangle_structural.glb', 'NPT_Triangle_structural.glb');
});

document.querySelector('#file').addEventListener('change', e => {
  const file = e.target.files?.[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  status.textContent = 'กำลังเปิด ' + file.name;
  loader.load(url, gltf => {
    showGltf(gltf, file.name);
    URL.revokeObjectURL(url);
  }, undefined, err => {
    console.error(err);
    status.textContent = 'เปิดไฟล์ไม่สำเร็จ';
    URL.revokeObjectURL(url);
  });
});

document.querySelector('#rotate').addEventListener('click', e => {
  controls.autoRotate = !controls.autoRotate;
  e.currentTarget.textContent = 'Auto Rotate: ' + (controls.autoRotate ? 'ON' : 'OFF');
});

document.querySelector('#reset').addEventListener('click', () => {
  if (model) fitCamera(model);
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
