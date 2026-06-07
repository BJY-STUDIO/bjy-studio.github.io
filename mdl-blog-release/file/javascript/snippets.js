/**
 * 代码块 click-to-copy 功能
 * 点击代码区域即可复制，鼠标移出后恢复
 * 适用于 code-with-text 和 snippet-group 容器内的所有语言代码块
 */
function MaterialComponentsSnippets() {
    "use strict";
    // 匹配所有语言的 <code> 元素
    this.snippets = document.querySelectorAll("code[class*='language-']");
    this.init();
}

MaterialComponentsSnippets.prototype.init = function() {
    "use strict";
    [].slice.call(this.snippets).forEach(function(t) {
        t.addEventListener("click", this.onMouseClickHandler(t));
        t.addEventListener("mouseout", this.onMouseOutHandler(t));
    }, this);
};

MaterialComponentsSnippets.prototype.CssClasses_ = {
    COPIED: "copied",
    NOT_SUPPORTED: "nosupport"
};

MaterialComponentsSnippets.prototype.copyToClipboard = function(t) {
    "use strict";
    // 优先使用现代 Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(t.textContent);
        return true;
    }
    // 降级使用 execCommand
    var e = window.getSelection(),
        n = document.createRange();
    n.selectNodeContents(t);
    e.removeAllRanges();
    e.addRange(n);
    var s = false;
    try {
        s = document.execCommand("copy");
    } catch (t) {
        console.error(t);
    }
    e.removeAllRanges();
    return s;
};

MaterialComponentsSnippets.prototype.onMouseClickHandler = function(t) {
    "use strict";
    return function() {
        if (!(window.getSelection().toString().length > 0)) {
            var e = this.CssClasses_.COPIED;
            this.copyToClipboard(t) || (e = this.CssClasses_.NOT_SUPPORTED);
            t.classList.add(e);
        }
    }.bind(this);
};

MaterialComponentsSnippets.prototype.onMouseOutHandler = function(t) {
    "use strict";
    return function() {
        t.classList.remove(this.CssClasses_.COPIED);
        t.classList.remove(this.CssClasses_.NOT_SUPPORTED);
    }.bind(this);
};

window.addEventListener("load", function() {
    "use strict";
    new MaterialComponentsSnippets();
});
