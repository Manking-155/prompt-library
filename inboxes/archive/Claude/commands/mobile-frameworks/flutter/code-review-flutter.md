 # Flutter Code Review (Framework Variant)
 
 Extends mobile/3-mobile-code-review.md with Flutter specifics.
 
 CHECKS (Flutter):
 - Widget rebuild hotspots; const usage
 - Dispose controllers/streams; unawaited futures
 - go_router route guards and redirection loops
 - Dio interceptors and error mapping; timeout/backoff
 - Image caching (cacheWidth/height); precache
 - Platform channel safety; isolate heavy work
 - Lints: flutter_lints/pedantic; zero warnings
 
