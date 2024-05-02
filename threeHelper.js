import * as THREE from './build/three.module.js';

export function renderParallelCoords(renderer, sceneInfo) {
 
  // get the viewport relative position of this element
  const {left, right, top, bottom, width, height} =
      sceneInfo.elem.getBoundingClientRect();
 
  // camera.aspect = width / height;
  // camera.updateProjectionMatrix();
 
  const positiveYUpBottom = renderer.domElement.clientHeight - bottom; 
  renderer.setScissor(left, positiveYUpBottom, width, height);
  renderer.setViewport(left, positiveYUpBottom, width, height);
 
  renderer.render(sceneInfo.scene, sceneInfo.camera); 
}

export function makeScene(elem) {
    const scene = new THREE.Scene();
   
    const fov = 80;
    const width = elem.clientWidth
    const height = elem.clientHeight
    const aspect = width / height;

    elem.style.width = width
    elem.style.height = height
    
		const camera = new THREE.OrthographicCamera( - 1, 1, 1, - 1, 0, 1 ); // cleaner! wants a 2x2 plane
    // const camera = new THREE.PerspectiveCamera(fov, aspect, .1, 5);
    // camera.position.z = .6; // by trial and error

    const geometry = new THREE.PlaneGeometry( 1, 1 );
    geometry.attributes.position.set(0,0,2);
    const material = new THREE.MeshBasicMaterial( {color: 0xaaaaaa, transparent: true, opacity: 0.1 } )// , side: THREE.DoubleSide} ); 
    const backing = new THREE.Mesh(geometry, material);
    scene.add(backing)
   
    return {scene, camera, elem, backing};
  }

  /* export function initParallelCoords() {
    const sceneInfo = makeScene(document.querySelector('#parallel'));
  
    const material = new THREE.ShaderMaterial( {
      vertexShader: document.getElementById( 'vertexshader-parcoords' ).textContent,
      fragmentShader: document.getElementById( 'fragmentshader-parcoords' ).textContent
    
    } );
    const geometry = new THREE.BufferGeometry({
  
      attributes: {
        xy: { value: new THREE.Vector2() },
        vColor: { value: new THREE.Vector3() }
      },
    });
    
    const line = new THREE.Line( geometry, material );
    // const mesh = new THREE.Mesh(geometry, material);
  
    sceneInfo.scene.add(line);
  
    return sceneInfo
  } */