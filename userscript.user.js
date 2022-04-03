// ==UserScript==
// @name         KaIT Logo template
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the canvas!
// @author       oralekin, drbaka-de
// @match        https://hot-potato.reddit.com/embed*
// @icon         https://www.kit.edu/img/intern/favicon.ico
// @grant        none
// @updateURL    https://drbaka-de.github.io/rplace/userscript.user.js
// @downloadURL  https://drbaka-de.github.io/rplace/userscript.user.js
// ==/UserScript==
if (window.top !== window.self) {
    window.addEventListener('load', () => {
            document.getElementsByTagName("mona-lisa-embed")[0].shadowRoot.children[0].getElementsByTagName("mona-lisa-canvas")[0].shadowRoot.children[0].appendChild(
        (function () {
            const i = document.createElement("img");
            const time = Math.floor(Date.now() / 10000);
            i.src = "https://raw.githubusercontent.com/drbaka-de/rplace/main/overlay.png?tstamp=" + time;
            i.style = "position: absolute;left: 0;top: 0;image-rendering: pixelated;width: 2000px;height: 2000px;";
            console.log(i);
            return i;
        })())
    }, false);
}
