## Fingerprint service

Run standard finger-printing on different browser setups to see the differences


## Getting Started
- uses python3
- `npm install` for client javascript libs from package.json
- `pip install -r requirements.txt`
- `./app.py` in new terminal; will start flask web server
- open `http://localhost:5000/?browser=<browsername_platform>`
    in browsers of your choice

### Splash
- `./host_splash` in new terminal; will ask for sudo password for docker
- `./splash_fingerprint.py > splash.html`

### Phantom JS
- `npm install phantomjs`
- `./phantom_fingerprint.js > phantom.html`

### Selenium
- `npm install chromedriver geckodriver`
- `./selenium_fingerprint.js` (no html output yet)



## Idea for CDNs
- find a plausible (popular) target to impersonate
- maybe chromebook, as it's linux-based?


## TODO
- inject js code that intercepts/logs/changes requests to
	canvas, webgl, fonts, navigator, etc.
- find other monkey patches (i.e. added methods on objects, etc.)
    - recurse through all (nested) objects attributes
- remove tell-tell signs of automated solutions (i.e. global vars)
- make sure information is consistent (navigator.appVersion, UA, platform)
- capture HTTP request headers
- audio stack fingerprinting
- https://github.com/EFForg/panopticlick-python (AGPL)
- browserspy.dk
- http://noc.to/
- looks like a very valuable source:
    - https://github.com/DIVERSIFY-project/amiunique
    - https://amiunique.org/stats


## Intercept JS accessors
- https://blog.javascripting.com/2014/05/19/wrapping-the-dom-window-object/
- https://stackoverflow.com/questions/14211125/defining-a-general-accessor-callback-in-v8
- https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Proxy
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/observe (only works for write updates)
- https://developer.mozilla.org/en-US/docs/DOM/MutationObserver (only updates)


### Other Fingerprinting
- https://github.com/brave/browser-laptop/wiki/Fingerprinting-Protection-Mode
- https://github.com/RobinLinus/ubercookie (39 stars)
- https://w3c.github.io/fingerprinting-guidance/
- http://darkwavetech.com/device_fingerprint.html 
- https://www.npmjs.com/package/browser-fingerprint
- http://www.hexacta.com/2016/06/15/browser-fingerprinting/
- https://browserleaks.com/canvas
- https://panopticlick.eff.org
- http://browserspy.dk/
 
