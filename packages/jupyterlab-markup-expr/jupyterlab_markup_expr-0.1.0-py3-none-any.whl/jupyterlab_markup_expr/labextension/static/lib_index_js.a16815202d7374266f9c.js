"use strict";
(self["webpackChunkjupyterlab_markup_expr"] = self["webpackChunkjupyterlab_markup_expr"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _plugin__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./plugin */ "./lib/plugin.js");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @agoose77/jupyterlab-markup */ "webpack/sharing/consume/default/@agoose77/jupyterlab-markup");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__);


const PACKAGE_NS = '@agoose77/jupyterlab-markup-expr';
/**
 * Captures expressions as data-attributes
 */
const plugin = (0,_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__.simpleMarkdownItPlugin)(PACKAGE_NS, {
    id: 'markdown-it-expr',
    title: 'Create spans with stored expressions from Markdown',
    description: 'Embed Markdown text in a data attribute in rendered spans',
    documentationUrls: {},
    plugin: async () => {
        return [_plugin__WEBPACK_IMPORTED_MODULE_1__.expressionPlugin];
    }
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EXPR_CLASS": () => (/* binding */ EXPR_CLASS),
/* harmony export */   "expressionPlugin": () => (/* binding */ expressionPlugin)
/* harmony export */ });
const EXPR_CLASS = 'eval-expr';
function expressionPlugin(md, options) {
    var _a, _b;
    const openDelim = (_a = options === null || options === void 0 ? void 0 : options.openDelim) !== null && _a !== void 0 ? _a : '{{';
    const closeDelim = (_b = options === null || options === void 0 ? void 0 : options.closeDelim) !== null && _b !== void 0 ? _b : '}}';
    function tokenize(state, silent) {
        // Check we start with the correct markers
        let pos = state.pos;
        // For performance, just check first character
        if (state.src[pos] !== openDelim[0]) {
            return false;
        }
        // Does the full substring match?
        if (state.src.slice(pos, pos + openDelim.length) !== openDelim) {
            return false;
        }
        pos += openDelim.length;
        // First index _after_ {{
        const startPos = pos;
        // Find end marker }}
        let stopPos = -1;
        while (stopPos === -1) {
            // Find first character of end marker
            pos = state.src.indexOf(closeDelim[0], pos);
            // Didn't find character
            if (pos === -1) {
                return false;
            }
            // If subsequent tokens don't match, just advance by one token!
            if (state.src.slice(pos, pos + closeDelim.length) !== closeDelim) {
                pos++;
                continue;
            }
            stopPos = pos;
            pos += closeDelim.length;
        }
        // Read tokens inside of the bracket
        const expression = state.src.slice(startPos, stopPos);
        state.pos = pos;
        const exprToken = state.push('expr', 'input', 0);
        exprToken.attrSet('type', 'hidden');
        exprToken.attrSet('class', EXPR_CLASS);
        exprToken.attrSet('value', expression);
        return true;
    }
    md.inline.ruler.after('emphasis', 'expr', tokenize);
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.a16815202d7374266f9c.js.map