 # Flutter Performance Playbook
 
 GUIDE:
 - Start-up: defer heavy inits; split code; prewarm isolates
 - Rendering: const, keys, RepaintBoundary, avoid deep trees in build
 - Lists: Slivers, itemExtent, cacheExtent, pagination
 - Images: correct sizes, caching, precache, placeholders
 - Animations: use Implicit/AnimatedBuilder; avoid jank
 - Networking: caching, ETag, batch requests, background sync
 - Diagnostics: DevTools (CPU, Memory, Raster), trace marks
 - Targets: <16ms frame build, cold start < Xs, mem < Ys
 
 CHECKS:
 - No layout thrash; minimal setState
 - Avoid synchronous I/O on UI thread
 - Use isolates for CPU-heavy work
 - Profile on real devices; compare iOS/Android
 
