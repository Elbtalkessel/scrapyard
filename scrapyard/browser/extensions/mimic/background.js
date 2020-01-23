function f() {
    navigator.languages = ['en-US', 'en'];
    navigator.plugins = [1, 2, 3, 4, 5];
    Object.defineProperty(navigator, 'languages', {
        get: function () {
            return ['en-US', 'en'];
        },
    });
    Object.defineProperty(navigator, 'plugins', {
        get: function () {
            // this just needs to have `length > 0`, but we could mock the plugins too
            return [1, 2, 3, 4, 5];
        },
    });
    const getParameter = WebGLRenderingContext.getParameter;
    WebGLRenderingContext.prototype.getParameter = function (parameter) {
        // UNMASKED_VENDOR_WEBGL
        if (parameter === 37445) {
            return 'Intel Open Source Technology Center';
        }
        // UNMASKED_RENDERER_WEBGL
        if (parameter === 37446) {
            return 'Mesa DRI Intel(R) Ivybridge Mobile ';
        }

        return getParameter(parameter);
    };
    ['height', 'width'].forEach(property => {
        // store the existing descriptor
        const imageDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property);

        // redefine the property with a patched descriptor
        Object.defineProperty(HTMLImageElement.prototype, property, {
            ...imageDescriptor,
            get: function () {
                // return an arbitrary non-zero dimension if the image failed to load
                if (this.complete && this.naturalHeight == 0) {
                    return 20;
                }
                // otherwise, return the actual dimension
                return imageDescriptor.get.apply(this);
            },
        });
    });
    // store the existing descriptor
    const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');
    // redefine the property with a patched descriptor
    Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {
        ...elementDescriptor,
        get: function () {
            if (this.id === 'modernizr') {
                return 1;
            }
            return elementDescriptor.get.apply(this);
        },
    });
    // Pass the Webdriver test
    Object.defineProperty(navigator, 'webdriver', {
        get: () => false,
    });
}
chrome.webRequest.onBeforeRequest.addListener(f);
f();
