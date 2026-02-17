import { useRef, useEffect } from 'react';
import * as THREE from 'three';

export function FlowGradient() {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!containerRef.current) return;

        // SCENE SETUP
        const scene = new THREE.Scene();
        const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 10);
        camera.position.z = 1;

        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        containerRef.current.appendChild(renderer.domElement);

        // SHADER MATERIAL
        // This shader creates a flowing gradient effect with noise and flow
        const vertexShader = `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

        const fragmentShader = `
      uniform float uTime;
      uniform vec2 uResolution;
      uniform vec2 uMouse;
      varying vec2 vUv;

      // Simplex noise function
      vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
      vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
      vec3 permute(vec3 x) { return mod289(((x*34.0)+1.0)*x); }
      float snoise(vec2 v) {
        const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
        vec2 i  = floor(v + dot(v, C.yy) );
        vec2 x0 = v -   i + dot(i, C.xx);
        vec2 i1;
        i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
        vec4 x12 = x0.xyxy + C.xxzz;
        x12.xy -= i1;
        i = mod289(i);
        vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 )) + i.x + vec3(0.0, i1.x, 1.0 ));
        vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
        m = m*m ;
        m = m*m ;
        vec3 x = 2.0 * fract(p * C.www) - 1.0;
        vec3 h = abs(x) - 0.5;
        vec3 ox = floor(x + 0.5);
        vec3 a0 = x - ox;
        m *= 1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h );
        vec3 g;
        g.x  = a0.x  * x0.x  + h.x  * x0.y;
        g.yz = a0.yz * x12.xz + h.yz * x12.yw;
        return 130.0 * dot(m, g);
      }

      void main() {
        vec2 st = gl_FragCoord.xy / uResolution.xy;
        
        // Aspect correction
        st.x *= uResolution.x / uResolution.y;

        // Flow effect
        float time = uTime * 0.2;
        float flow = snoise(vec2(st.x * 2.0 + time, st.y * 2.0 - time));
        
        // Mouse interaction
        float dist = distance(st, uMouse);
        float mouseEffect = smoothstep(0.4, 0.0, dist) * 0.1;
        
        // Colors from palette
        // #151515 (Dark)
        // #DEEBC8 (Pale Green) - Using this for the flow highlights
        // #1E2319 (Darker Greenish Black) - for depth
        
        vec3 colorBg = vec3(0.082, 0.082, 0.082); // #151515
        vec3 colorPrimary = vec3(0.871, 0.922, 0.784); // #DEEBC8
        vec3 colorDeep = vec3(0.1, 0.12, 0.1);

        // Mixing logic
        vec3 color = mix(colorBg, colorDeep, flow);
        color = mix(color, colorPrimary, smoothstep(0.4, 0.6, flow + mouseEffect));
        
        // Add Grain
        float noise = fract(sin(dot(vUv, vec2(12.9898, 78.233))) * 43758.5453);
        color += noise * 0.04;

        gl_FragColor = vec4(color, 1.0);
      }
    `;

        const material = new THREE.ShaderMaterial({
            vertexShader,
            fragmentShader,
            uniforms: {
                uTime: { value: 0 },
                uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
                uMouse: { value: new THREE.Vector2(0.5, 0.5) }
            }
        });

        const geometry = new THREE.PlaneGeometry(2, 2);
        const plane = new THREE.Mesh(geometry, material);
        scene.add(plane);

        // ANIMATION LOOP
        const clock = new THREE.Clock();

        const animate = () => {
            material.uniforms.uTime.value = clock.getElapsedTime();
            renderer.render(scene, camera);
            requestAnimationFrame(animate);
        };
        animate();

        // HANDLERS
        const handleResize = () => {
            renderer.setSize(window.innerWidth, window.innerHeight);
            material.uniforms.uResolution.value.set(window.innerWidth, window.innerHeight);
        };

        const handleMouseMove = (e: MouseEvent) => {
            // Normalize mouse to aspect corrected coordinates roughly
            const x = (e.clientX / window.innerWidth) * (window.innerWidth / window.innerHeight);
            const y = 1.0 - (e.clientY / window.innerHeight); // Flip Y for shader
            material.uniforms.uMouse.value.set(x, y);
        };

        window.addEventListener('resize', handleResize);
        window.addEventListener('mousemove', handleMouseMove);

        return () => {
            window.removeEventListener('resize', handleResize);
            window.removeEventListener('mousemove', handleMouseMove);
            if (containerRef.current) containerRef.current.removeChild(renderer.domElement);
            renderer.dispose();
        };
    }, []);

    return <div ref={containerRef} className="fixed inset-0 z-0 pointer-events-none" />;
}
