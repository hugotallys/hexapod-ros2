import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import * as dat from 'dat.gui';

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
const orbit = new OrbitControls( camera, renderer.domElement );
camera.position.set( 0, 3, 0 );
orbit.update();

const axesHelper = new THREE.AxesHelper( 3 );
scene.add( axesHelper );

let w = 1;
let h = 2;
let m = 1.5;

const bodyGeometry = new THREE.BufferGeometry();

bodyGeometry.setAttribute( 'position', new THREE.BufferAttribute( computeBodyGeometry(w, h, m), 3 ) );
const bodyMaterial = new THREE.MeshBasicMaterial( { color: 0x721ec7, side: THREE.DoubleSide, transparent: true, opacity: 0.4 } );
const body = new THREE.Mesh( bodyGeometry, bodyMaterial );

body.geometry.attributes.position.needsUpdate = true;

scene.add( body );

const gui = new dat.GUI();

const options = {
    bodyColor: 0x721ec7,
    wireframe: false,
    width: w,
    height: w,
    middle: m
};

gui.addColor( options, 'bodyColor' ).onChange(
    (e) => { body.material.color.set(e); }
);

gui.add( options, 'wireframe' ).onChange(
    (e) => { body.material.wireframe = e; }
);

gui.add( options, 'width').onChange(
    (e) => { 
        w = e;
        bodyGeometry.setAttribute( 'position', new THREE.BufferAttribute( computeBodyGeometry(w, h, m), 3 ) );
    }
);
gui.add( options, 'height').onChange(
    (e) => { 
        h = e;
        bodyGeometry.setAttribute( 'position', new THREE.BufferAttribute( computeBodyGeometry(w, h, m), 3 ) );
    }
);
gui.add( options, 'middle').onChange(
    (e) => { 
        m = e;
        bodyGeometry.setAttribute( 'position', new THREE.BufferAttribute( computeBodyGeometry(w, h, m), 3 ) );
    }
);

function animate() {
    requestAnimationFrame( animate );
    body.rotation.x += 0.01
    body.rotation.y += 0.01
    renderer.render( scene, camera );
};

animate();

function computeBodyGeometry(w, h, m) {
    const vertices = [
        [0.5 * w, 0.0, -0.5 * h], [0.5 * m, 0.0, 0.0], [0.5 * w, 0.0, 0.5 * h],
        [-0.5 * w, 0.0, 0.5 * h], [-0.5 * m, 0.0, 0.0], [-0.5 * w, 0.0, -0.5 * h]
    ];

    const faces = [
        4, 5, 0,
        4, 0, 1,
        4, 1, 2,
        4, 2, 3
    ];

    let mapped = new Float32Array( faces.map((i) => vertices[i]).flat() );

    return mapped;
}