// Aesthetic 3D Background Animation using Three.js
document.addEventListener("DOMContentLoaded", () => {
    // Only run if canvas container exists
    let bgContainer = document.getElementById("bg-canvas-container");
    if(!bgContainer) {
        bgContainer = document.createElement('div');
        bgContainer.id = "bg-canvas-container";
        bgContainer.style.position = "fixed";
        bgContainer.style.top = "0";
        bgContainer.style.left = "0";
        bgContainer.style.width = "100vw";
        bgContainer.style.height = "100vh";
        bgContainer.style.zIndex = "-5";
        bgContainer.style.pointerEvents = "none";
        document.body.appendChild(bgContainer);
    }

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    bgContainer.appendChild(renderer.domElement);

    // Create particles
    const geometry = new THREE.BufferGeometry();
    const particlesCount = 800;
    const posArray = new Float32Array(particlesCount * 3);

    for(let i = 0; i < particlesCount * 3; i++) {
        // spread particles
        posArray[i] = (Math.random() - 0.5) * 12;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    
    // Create material for particles
    const material = new THREE.PointsMaterial({
        size: 0.018,
        color: 0x00e5ff,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending
    });

    const particlesMesh = new THREE.Points(geometry, material);
    scene.add(particlesMesh);

    camera.position.z = 3;

    // Mouse interaction
    let mouseX = 0;
    let mouseY = 0;
    
    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX / window.innerWidth) - 0.5;
        mouseY = (event.clientY / window.innerHeight) - 0.5;
    });

    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);
        const elapsedTime = clock.getElapsedTime();

        // Slow rotation
        particlesMesh.rotation.y = elapsedTime * 0.03;
        particlesMesh.rotation.x = elapsedTime * 0.01;

        // Slight parallax on mouse move target
        particlesMesh.rotation.y += mouseX * 0.05;
        particlesMesh.rotation.x += mouseY * 0.05;

        renderer.render(scene, camera);
    }
    
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
});
