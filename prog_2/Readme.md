## Proxy Cache

##### Author
Atharva Chalke

#### Compilation and Running
- compilation: javac -deprecation *.java
- running: sudo java ProxyCache 80

#### Configuration for MAC
- PLEASE USE SAFARI AND NOT CHROMO
- go to setting, and then network.
- Go to advanced, then proxies
- Select HTTP, and write "local host" in Web Proxy server field.
- Make the port number (Field after semicolon) to 80
- Select ok and then apply 

#### Extensions
- Better Error Handling: In Response, we check the status line to see if we have a 404. If we do, then the function returns without checking for anything further
- Content Transformation: We replace the word "Computer" with "DaddyWho", replace "University of Massachusetts, Amherst" with "UC DAVIS ROXXXXXX", and change the url for "/personnel/towsley.html" to "https://www.facebook.com". 

#### Tests
- This was tested on http://gaia.cs.umass.edu. You can notice the changes by opening the page , looking through it , and clicking the hyperlink for Don Townsley.
- The proxy works well for HTTP websites, but not for HTTPS since we don't support that. Also we cannot have content larger 100kb as specified by the initial code provided. This can be modified though.


