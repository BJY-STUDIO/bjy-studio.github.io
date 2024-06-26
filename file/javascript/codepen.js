function CodeBlockCodePen() {
    "use strict";
    this.codepenButtons = document.getElementsByClassName("codepen-button"), this.init()
}
CodeBlockCodePen.prototype.MDLIBS = ["<!-- Material Design Lite -->", '<script src="https://code.getmdl.io/1.3.0/material.min.js"></script>', '<link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">', "<!-- Material Design icon font -->", '<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">'], CodeBlockCodePen.prototype.init = function() {
    "use strict";
    [].slice.call(this.codepenButtons).forEach(function(t) {
        t.addEventListener("click", this.clickHandler(t, t.parentNode))
    }, this)
}, CodeBlockCodePen.prototype.extractTagsContent = function(t, e, n) {
    "use strict";
    for (var i, o, s = ""; n.indexOf(t) !== -1;) i = n.indexOf(t), o = n.indexOf(e), s += n.substring(i + t.length, o), n = n.substring(0, i).trim() + "\n" + n.substr(o + e.length).trim();
    return {
        textRemainder: n,
        tagContent: s
    }
}, CodeBlockCodePen.prototype.clickHandler = function(t, e) {
    "use strict";
    return function() {
        "undefined" != typeof ga && ga("send", {
            hitType: "event",
            eventCategory: "codepen",
            eventAction: "click",
            eventLabel: window.location.pathname + (window.location.hash ? window.location.hash : "")
        });
        var n = e.textContent.replace("../assets/demos/", window.location.origin + "/assets/demos/"),
            i = this.extractTagsContent("<style>", "</style>", n);
        n = i.textRemainder;
        var o = i.tagContent.trim(),
            s = this.extractTagsContent("<script>", "</script>", n);
        n = s.textRemainder.trim();
        for (var r = s.tagContent.trim(); t.firstChild;) t.removeChild(t.firstChild);
        var a = document.createElement("input");
        a.setAttribute("type", "hidden"), a.setAttribute("name", "data"), a.setAttribute("value", JSON.stringify({
            title: "Material Design Lite components demo",
            html: "<html>\n  <head>\n    " + this.MDLIBS.join("\n    ") + "\n  </head>\n  <body>\n    " + n.split("\n").join("\n    ") + "\n  </body>\n</html>",
            css: o,
            js: r
        })), t.appendChild(a), t.submit()
    }.bind(this)
}, window.addEventListener("load", function() {
    "use strict";
    new CodeBlockCodePen
});