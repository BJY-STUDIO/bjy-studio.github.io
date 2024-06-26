self = "undefined" != typeof window ? window : "undefined" != typeof WorkerGlobalScope && self instanceof WorkerGlobalScope ? self : {};
var Prism = function() {
    var e = /\blang(?:uage)?-(?!\*)(\w+)\b/i,
        t = self.Prism = {
            util: {
                encode: function(e) {
                    return e instanceof a ? new a(e.type, t.util.encode(e.content), e.alias) : "Array" === t.util.type(e) ? e.map(t.util.encode) : e.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/\u00a0/g, " ")
                },
                type: function(e) {
                    return Object.prototype.toString.call(e).match(/\[object (\w+)\]/)[1]
                },
                clone: function(e) {
                    var a = t.util.type(e);
                    switch (a) {
                        case "Object":
                            var n = {};
                            for (var r in e) e.hasOwnProperty(r) && (n[r] = t.util.clone(e[r]));
                            return n;
                        case "Array":
                            return e.map(function(e) {
                                return t.util.clone(e)
                            })
                    }
                    return e
                }
            },
            languages: {
                extend: function(e, a) {
                    var n = t.util.clone(t.languages[e]);
                    for (var r in a) n[r] = a[r];
                    return n
                },
                insertBefore: function(e, a, n, r) {
                    r = r || t.languages;
                    var i = r[e];
                    if (2 == arguments.length) {
                        n = arguments[1];
                        for (var s in n) n.hasOwnProperty(s) && (i[s] = n[s]);
                        return i
                    }
                    var l = {};
                    for (var o in i)
                        if (i.hasOwnProperty(o)) {
                            if (o == a)
                                for (var s in n) n.hasOwnProperty(s) && (l[s] = n[s]);
                            l[o] = i[o]
                        }
                    return t.languages.DFS(t.languages, function(t, a) {
                        a === r[e] && t != e && (this[t] = l)
                    }), r[e] = l
                },
                DFS: function(e, a, n) {
                    for (var r in e) e.hasOwnProperty(r) && (a.call(e, r, e[r], n || r), "Object" === t.util.type(e[r]) ? t.languages.DFS(e[r], a) : "Array" === t.util.type(e[r]) && t.languages.DFS(e[r], a, r))
                }
            },
            highlightAll: function(e, a) {
                for (var n, r = document.querySelectorAll('code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code'), i = 0; n = r[i++];) t.highlightElement(n, e === !0, a)
            },
            highlightElement: function(n, r, i) {
                for (var s, l, o = n; o && !e.test(o.className);) o = o.parentNode;
                if (o && (s = (o.className.match(e) || [, ""])[1], l = t.languages[s]), l) {
                    n.className = n.className.replace(e, "").replace(/\s+/g, " ") + " language-" + s, o = n.parentNode, /pre/i.test(o.nodeName) && (o.className = o.className.replace(e, "").replace(/\s+/g, " ") + " language-" + s);
                    var u = n.textContent;
                    if (u) {
                        u = u.replace(/^(?:\r?\n|\r)/, "");
                        var c = {
                            element: n,
                            language: s,
                            grammar: l,
                            code: u
                        };
                        if (t.hooks.run("before-highlight", c), r && self.Worker) {
                            var g = new Worker(t.filename);
                            g.onmessage = function(e) {
                                c.highlightedCode = a.stringify(JSON.parse(e.data), s), t.hooks.run("before-insert", c), c.element.innerHTML = c.highlightedCode, i && i.call(c.element), t.hooks.run("after-highlight", c)
                            }, g.postMessage(JSON.stringify({
                                language: c.language,
                                code: c.code
                            }))
                        } else c.highlightedCode = t.highlight(c.code, c.grammar, c.language), t.hooks.run("before-insert", c), c.element.innerHTML = c.highlightedCode, i && i.call(n), t.hooks.run("after-highlight", c)
                    }
                }
            },
            highlight: function(e, n, r) {
                var i = t.tokenize(e, n);
                return a.stringify(t.util.encode(i), r)
            },
            tokenize: function(e, a, n) {
                var r = t.Token,
                    i = [e],
                    s = a.rest;
                if (s) {
                    for (var l in s) a[l] = s[l];
                    delete a.rest
                }
                e: for (var l in a)
                    if (a.hasOwnProperty(l) && a[l]) {
                        var o = a[l];
                        o = "Array" === t.util.type(o) ? o : [o];
                        for (var u = 0; u < o.length; ++u) {
                            var c = o[u],
                                g = c.inside,
                                p = !!c.lookbehind,
                                f = 0,
                                d = c.alias;
                            c = c.pattern || c;
                            for (var m = 0; m < i.length; m++) {
                                var h = i[m];
                                if (i.length > e.length) break e;
                                if (!(h instanceof r)) {
                                    c.lastIndex = 0;
                                    var y = c.exec(h);
                                    if (y) {
                                        p && (f = y[1].length);
                                        var v = y.index - 1 + f,
                                            y = y[0].slice(f),
                                            w = y.length,
                                            k = v + w,
                                            b = h.slice(0, v + 1),
                                            P = h.slice(k + 1),
                                            x = [m, 1];
                                        b && x.push(b);
                                        var A = new r(l, g ? t.tokenize(y, g) : y, d);
                                        x.push(A), P && x.push(P), Array.prototype.splice.apply(i, x)
                                    }
                                }
                            }
                        }
                    }
                return i
            },
            hooks: {
                all: {},
                add: function(e, a) {
                    var n = t.hooks.all;
                    n[e] = n[e] || [], n[e].push(a)
                },
                run: function(e, a) {
                    var n = t.hooks.all[e];
                    if (n && n.length)
                        for (var r, i = 0; r = n[i++];) r(a)
                }
            }
        },
        a = t.Token = function(e, t, a) {
            this.type = e, this.content = t, this.alias = a
        };
    if (a.stringify = function(e, n, r) {
            if ("string" == typeof e) return e;
            if ("Array" === t.util.type(e)) return e.map(function(t) {
                return a.stringify(t, n, e)
            }).join("");
            var i = {
                type: e.type,
                content: a.stringify(e.content, n, r),
                tag: "span",
                classes: ["token", e.type],
                attributes: {},
                language: n,
                parent: r
            };
            if ("comment" == i.type && (i.attributes.spellcheck = "true"), e.alias) {
                var s = "Array" === t.util.type(e.alias) ? e.alias : [e.alias];
                Array.prototype.push.apply(i.classes, s)
            }
            t.hooks.run("wrap", i);
            var l = "";
            for (var o in i.attributes) l += o + '="' + (i.attributes[o] || "") + '"';
            return "<" + i.tag + ' class="' + i.classes.join(" ") + '" ' + l + ">" + i.content + "</" + i.tag + ">"
        }, !self.document) return self.addEventListener ? (self.addEventListener("message", function(e) {
        var a = JSON.parse(e.data),
            n = a.language,
            r = a.code;
        self.postMessage(JSON.stringify(t.util.encode(t.tokenize(r, t.languages[n])))), self.close()
    }, !1), self.Prism) : self.Prism;
    var n = document.getElementsByTagName("script");
    return n = n[n.length - 1], n && (t.filename = n.src, document.addEventListener && !n.hasAttribute("data-manual") && document.addEventListener("DOMContentLoaded", t.highlightAll)), self.Prism
}();
"undefined" != typeof module && module.exports && (module.exports = Prism), Prism.languages.markup = {
        comment: /<!--[\w\W]*?-->/,
        prolog: /<\?.+?\?>/,
        doctype: /<!DOCTYPE.+?>/,
        cdata: /<!\[CDATA\[[\w\W]*?]]>/i,
        tag: {
            pattern: /<\/?[\w:-]+\s*(?:\s+[\w:-]+(?:=(?:("|')(\\?[\w\W])*?\1|[^\s'">=]+))?\s*)*\/?>/i,
            inside: {
                tag: {
                    pattern: /^<\/?[\w:-]+/i,
                    inside: {
                        punctuation: /^<\/?/,
                        namespace: /^[\w-]+?:/
                    }
                },
                "attr-value": {
                    pattern: /=(?:('|")[\w\W]*?(\1)|[^\s>]+)/i,
                    inside: {
                        punctuation: /=|>|"/
                    }
                },
                punctuation: /\/?>/,
                "attr-name": {
                    pattern: /[\w:-]+/,
                    inside: {
                        namespace: /^[\w-]+?:/
                    }
                }
            }
        },
        entity: /&#?[\da-z]{1,8};/i
    }, Prism.hooks.add("wrap", function(e) {
        "entity" === e.type && (e.attributes.title = e.content.replace(/&amp;/, "&"))
    }), Prism.languages.css = {
        comment: /\/\*[\w\W]*?\*\//,
        atrule: {
            pattern: /@[\w-]+?.*?(;|(?=\s*\{))/i,
            inside: {
                punctuation: /[;:]/
            }
        },
        url: /url\((?:(["'])(\\\n|\\?.)*?\1|.*?)\)/i,
        selector: /[^\{\}\s][^\{\};]*(?=\s*\{)/,
        string: /("|')(\\\n|\\?.)*?\1/,
        property: /(\b|\B)[\w-]+(?=\s*:)/i,
        important: /\B!important\b/i,
        punctuation: /[\{\};:]/,
        function: /[-a-z0-9]+(?=\()/i
    }, Prism.languages.markup && (Prism.languages.insertBefore("markup", "tag", {
        style: {
            pattern: /<style[\w\W]*?>[\w\W]*?<\/style>/i,
            inside: {
                tag: {
                    pattern: /<style[\w\W]*?>|<\/style>/i,
                    inside: Prism.languages.markup.tag.inside
                },
                rest: Prism.languages.css
            },
            alias: "language-css"
        }
    }), Prism.languages.insertBefore("inside", "attr-value", {
        "style-attr": {
            pattern: /\s*style=("|').*?\1/i,
            inside: {
                "attr-name": {
                    pattern: /^\s*style/i,
                    inside: Prism.languages.markup.tag.inside
                },
                punctuation: /^\s*=\s*['"]|['"]\s*$/,
                "attr-value": {
                    pattern: /.+/i,
                    inside: Prism.languages.css
                }
            },
            alias: "language-css"
        }
    }, Prism.languages.markup.tag)), Prism.languages.clike = {
        comment: [{
            pattern: /(^|[^\\])\/\*[\w\W]*?\*\//,
            lookbehind: !0
        }, {
            pattern: /(^|[^\\:])\/\/.*/,
            lookbehind: !0
        }],
        string: /("|')(\\\n|\\?.)*?\1/,
        "class-name": {
            pattern: /((?:(?:class|interface|extends|implements|trait|instanceof|new)\s+)|(?:catch\s+\())[a-z0-9_\.\\]+/i,
            lookbehind: !0,
            inside: {
                punctuation: /(\.|\\)/
            }
        },
        keyword: /\b(if|else|while|do|for|return|in|instanceof|function|new|try|throw|catch|finally|null|break|continue)\b/,
        boolean: /\b(true|false)\b/,
        function: {
            pattern: /[a-z0-9_]+\(/i,
            inside: {
                punctuation: /\(/
            }
        },
        number: /\b-?(0x[\dA-Fa-f]+|\d*\.?\d+([Ee]-?\d+)?)\b/,
        operator: /[-+]{1,2}|!|<=?|>=?|={1,3}|&{1,2}|\|?\||\?|\*|\/|~|\^|%/,
        ignore: /&(lt|gt|amp);/i,
        punctuation: /[{}[\];(),.:]/
    }, Prism.languages.javascript = Prism.languages.extend("clike", {
        keyword: /\b(break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|false|finally|for|function|get|if|implements|import|in|instanceof|interface|let|new|null|package|private|protected|public|return|set|static|super|switch|this|throw|true|try|typeof|var|void|while|with|yield)\b/,
        number: /\b-?(0x[\dA-Fa-f]+|\d*\.?\d+([Ee][+-]?\d+)?|NaN|-?Infinity)\b/,
        function: /(?!\d)[a-z0-9_$]+(?=\()/i
    }), Prism.languages.insertBefore("javascript", "keyword", {
        regex: {
            pattern: /(^|[^\/])\/(?!\/)(\[.+?]|\\.|[^\/\r\n])+\/[gim]{0,3}(?=\s*($|[\r\n,.;})]))/,
            lookbehind: !0
        }
    }), Prism.languages.markup && Prism.languages.insertBefore("markup", "tag", {
        script: {
            pattern: /<script[\w\W]*?>[\w\W]*?<\/script>/i,
            inside: {
                tag: {
                    pattern: /<script[\w\W]*?>|<\/script>/i,
                    inside: Prism.languages.markup.tag.inside
                },
                rest: Prism.languages.javascript
            },
            alias: "language-javascript"
        }
    }),
    function() {
        self.Prism && self.document && document.querySelector && (self.Prism.fileHighlight = function() {
            var e = {
                js: "javascript",
                html: "markup",
                svg: "markup",
                xml: "markup",
                py: "python",
                rb: "ruby",
                ps1: "powershell",
                psm1: "powershell"
            };
            Array.prototype.slice.call(document.querySelectorAll("pre[data-src]")).forEach(function(t) {
                var a = t.getAttribute("data-src"),
                    n = (a.match(/\.(\w+)$/) || [, ""])[1],
                    r = e[n] || n,
                    i = document.createElement("code");
                i.className = "language-" + r, t.textContent = "", i.textContent = "Loading…", t.appendChild(i);
                var s = new XMLHttpRequest;
                s.open("GET", a, !0), s.onreadystatechange = function() {
                    4 == s.readyState && (s.status < 400 && s.responseText ? (i.textContent = s.responseText, Prism.highlightElement(i)) : s.status >= 400 ? i.textContent = "✖ Error " + s.status + " while fetching file: " + s.statusText : i.textContent = "✖ Error: File does not exist or is empty")
                }, s.send(null)
            })
        }, self.Prism.fileHighlight())
    }();