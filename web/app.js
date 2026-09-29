import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.180.0/examples/jsm/loaders/GLTFLoader.js';

const canvas = document.querySelector('#view');
const renderer = new THREE.WebGLRenderer({canvas, antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled = true;
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101513);

const camera = new THREE.PerspectiveCamera(40,1,0.1,200);
camera.position.set(14,-16,10);

const controls = new OrbitControls(camera,canvas);
controls.target.set(0,0,1.8);
controls.enableDamping = true;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.8;

scene.add(new THREE.HemisphereLight(0xffffff,0x354038,2.3));
const sun = new THREE.DirectionalLight(0xfff0d6,3.0);
sun.position.set(-8,-10,16);
sun.castShadow = true;
scene.add(sun);

const grid = new THREE.GridHelper(30,30,0x667069,0x303832);
scene.add(grid);

new GLTFLoader().load('./assets/house_10x10.glb', ({scene:model}) => {
  model.traverse(o => {
    if (o.isMesh) {
      o.castShadow = true;
      o.receiveShadow = true;
    }
  });
  scene.add(model);
}, undefined, err => console.error('GLB load failed', err));

document.querySelector('#rotate').addEventListener('click', e => {
  controls.autoRotate = !controls.autoRotate;
  e.currentTarget.textContent = 'Auto Rotate: ' + (controls.autoRotate ? 'ON' : 'OFF');
});

function resize(){
  const r = canvas.getBoundingClientRect();
  renderer.setSize(r.width,r.height,false);
  camera.aspect = r.width/r.height;
  camera.updateProjectionMatrix();
}
function frame(){
  resize();
  controls.update();
  renderer.render(scene,camera);
  requestAnimationFrame(frame);
}
frame();
