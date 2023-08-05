"use strict";
(self["webpackChunkjupyterlab_imarkdown"] = self["webpackChunkjupyterlab_imarkdown"] || []).push([["lib_index_js"],{

/***/ "./lib/cell.js":
/*!*********************!*\
  !*** ./lib/cell.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ERROR_CLASS": () => (/* binding */ ERROR_CLASS),
/* harmony export */   "RENDERED_CLASS": () => (/* binding */ RENDERED_CLASS),
/* harmony export */   "RESULT_CLASS": () => (/* binding */ RESULT_CLASS),
/* harmony export */   "XMarkdownCell": () => (/* binding */ XMarkdownCell)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tokenize__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tokenize */ "./lib/tokenize.js");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _metadata__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./metadata */ "./lib/metadata.js");
/* harmony import */ var _user_expressions__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./user_expressions */ "./lib/user_expressions.js");





// Base CSS class for jupyterlab-imarkdown outputs
const RENDERED_CLASS = 'im-rendered';
// CSS class for execution-result outputs
const RESULT_CLASS = 'im-result';
// CSS class for missing outputs
const ERROR_CLASS = 'im-error';
class XMarkdownCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.MarkdownCell {
    constructor(options) {
        super(options);
        this.__expressions = [];
        this.__lastContent = '';
        this.__doneRendering = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.PromiseDelegate();
        this.__rendermime = options.rendermime;
    }
    /**
     * Create an IRenderMime.IMimeModel for a given IExpressionResult
     */
    renderExpressionResultModel(payload) {
        let options;
        if ((0,_user_expressions__WEBPACK_IMPORTED_MODULE_2__.isOutput)(payload)) {
            // Output results are simple to reinterpret
            options = {
                trusted: this.model.trusted,
                data: payload.data,
                metadata: payload.metadata
            };
        }
        else {
            // Errors need to be formatted as stderr objects
            options = {
                data: {
                    'application/vnd.jupyter.stderr': payload.traceback.join('\n') ||
                        `${payload.ename}: ${payload.evalue}`
                }
            };
        }
        // Invoke MIME rendere
        const model = this.__rendermime.createModel(options);
        // Select preferred mimetype for bundle
        // FIXME: choose appropriate value for `safe`
        const mimeType = this.__rendermime.preferredMimeType(model.data, 'any');
        if (mimeType === undefined) {
            console.error("Couldn't find mimetype");
            // Return error result
            const node = document.createElement('span');
            node.classList.add(RENDERED_CLASS);
            node.classList.add(ERROR_CLASS);
            return node;
        }
        // Create renderer
        const renderer = this.__rendermime.createRenderer(mimeType);
        renderer.addClass(RENDERED_CLASS);
        renderer.addClass(RESULT_CLASS);
        // Render model
        renderer.renderModel(model);
        return renderer.node;
    }
    /**
     * Get an array of names to kernel expressions.
     */
    get expressions() {
        return this.__expressions.map(node => node.expression);
    }
    /**
     * Whether the Markdown renderer has finished rendering.
     */
    get doneRendering() {
        return this.__doneRendering.promise;
    }
    /**
     * Update rendered expressions from current attachment MIME-bundles
     */
    renderExpressions() {
        console.log('Rendering expressions', this.expressions);
        const expressionsMetadata = this.model.metadata.get(_metadata__WEBPACK_IMPORTED_MODULE_3__.metadataSection);
        if (expressionsMetadata === undefined) {
            console.log('Aborting rendering of expressions: no metadata', this.expressions);
            return;
        }
        // Check we have enough keys
        if (expressionsMetadata.length !== this.__expressions.length) {
            console.log('Aborting rendering of expressions: expressions mismatch', this.expressions, expressionsMetadata);
            return;
        }
        // Loop over expressions and render them from the cell attachments
        this.__expressions.forEach((node, index) => {
            var _a;
            const metadata = expressionsMetadata[index];
            // Can't render the remaining keys. Should we have aborted earlier?
            if (metadata.expression !== node.expression) {
                console.log(`Metadata expression does not match Markdown expression at index ${index}`);
                return;
            }
            if (metadata.result === undefined) {
                console.log(`Metadata has no result at index ${index}`);
                return;
            }
            console.log(`Rendering ${metadata.expression} into ${node.element}`);
            const element = this.renderExpressionResultModel(metadata.result);
            (_a = node.element.parentNode) === null || _a === void 0 ? void 0 : _a.replaceChild(element, node.element);
            node.element = element;
        });
    }
    /**
     * Wait for Markdown rendering to complete.
     * Assume that rendered container will have at least one child.
     */
    _waitForRender(widget, timeout) {
        // FIXME: this is a HACK
        return new Promise(resolve => {
            function waitReady() {
                const firstChild = widget.node.querySelector('.jp-RenderedMarkdown *');
                if (firstChild !== null) {
                    return resolve();
                }
                setTimeout(waitReady, timeout);
            }
            waitReady();
        });
    }
    renderInput(widget) {
        // FIXME: `renderInput` is called without waiting for render future to finish
        // Therefore, this is sometimes executed before the DOM is updated.
        super.renderInput(widget);
        const currentContent = this.model.value.text;
        // If the content has changed
        if (this.__lastContent !== currentContent) {
            this.__doneRendering = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.PromiseDelegate();
            // Wait for rendering to complete
            this._waitForRender(widget, 2).then(() => {
                // Identify markup expressions by placeholders
                this._identifyExpressions(widget);
                // Replace placeholders with content from attachments
                this.renderExpressions();
                this.__doneRendering.resolve();
            });
            this.__lastContent = currentContent;
        }
    }
    /**
     * Parse the rendered markdown, and store placeholder and expression mappings
     */
    _identifyExpressions(widget) {
        const exprInputNodes = widget.node.querySelectorAll(`input.${_tokenize__WEBPACK_IMPORTED_MODULE_4__.EXPR_CLASS}`);
        // Store expressions & their current placeholders
        this.__expressions = [];
        exprInputNodes.forEach((elem, index) => {
            this.__expressions.push({
                expression: elem.value,
                element: elem
            });
        });
        console.log('Found expressions', this.__expressions);
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _plugin__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./plugin */ "./lib/plugin.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _cell__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./cell */ "./lib/cell.js");
/* harmony import */ var _kernel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./kernel */ "./lib/kernel.js");





class XMarkdownContentFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.ContentFactory {
    /**
     * Create a new markdown cell widget.
     *
     * #### Notes
     * If no cell content factory is passed in with the options, the one on the
     * notebook content factory is used.
     */
    createMarkdownCell(options, parent) {
        if (!options.contentFactory) {
            options.contentFactory = this;
        }
        return new _cell__WEBPACK_IMPORTED_MODULE_2__.XMarkdownCell(options).initializeState();
    }
}
/**
 * The notebook cell factory provider.
 */
const factory = {
    id: '@agoose77/jupyterlab-imarkdown:factory',
    provides: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.IContentFactory,
    requires: [_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.IEditorServices],
    autoStart: true,
    activate: (app, editorServices) => {
        console.log('Using jupyterlab-imarkdown:editor');
        const editorFactory = editorServices.factoryService.newInlineEditor;
        return new XMarkdownContentFactory({ editorFactory });
    }
};
function isMarkdownCell(cell) {
    return cell.model.type === 'markdown';
}
/**
 * The notebook cell executor.
 */
const executor = {
    id: '@agoose77/jupyterlab-imarkdown:executor',
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    autoStart: true,
    activate: (app, tracker) => {
        console.log('Using jupyterlab-imarkdown:executor');
        const executed = _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed;
        executed.connect((sender, value) => {
            const { notebook, cell } = value;
            // Find the Notebook panel
            const panel = tracker.find((w) => {
                return w.content === notebook;
            });
            // Retrieve the kernel context
            const ctx = panel === null || panel === void 0 ? void 0 : panel.sessionContext;
            if (ctx === undefined) {
                return;
            }
            // Load the user expressions for the given cell.
            if (!isMarkdownCell(cell)) {
                return;
            }
            console.log('Markdown cell was executed, waiting for render to complete ...');
            cell.doneRendering.then(() => {
                console.log('Loading results from kernel');
                (0,_kernel__WEBPACK_IMPORTED_MODULE_3__.executeUserExpressions)(cell, ctx).then(() => {
                    console.log('Re-rendering cell!');
                    cell.renderExpressions();
                });
            });
        });
        return;
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [factory, executor, _plugin__WEBPACK_IMPORTED_MODULE_4__.plugin];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/kernel.js":
/*!***********************!*\
  !*** ./lib/kernel.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "executeUserExpressions": () => (/* binding */ executeUserExpressions)
/* harmony export */ });
/* harmony import */ var _metadata__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./metadata */ "./lib/metadata.js");

/**
 * Load user expressions for given XMarkdown cell from kernel.
 * Store results in cell attachments.
 */
async function executeUserExpressions(cell, sessionContext) {
    var _a;
    const model = cell.model;
    const cellId = { cellId: model.id };
    // Build ordered map from string index to node
    const namedExpressions = new Map(cell.expressions.map((expr, index) => [`${index}`, expr]));
    // Extract expression values
    const userExpressions = {};
    namedExpressions.forEach((expr, key) => {
        userExpressions[key] = expr;
    });
    // Populate request data
    const content = {
        code: '',
        user_expressions: userExpressions
    };
    // Check we have a kernel
    const kernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
    if (!kernel) {
        throw new Error('Session has no kernel.');
    }
    // Perform request
    console.log('Performing kernel request', cell.expressions);
    const future = kernel.requestExecute(content, false, Object.assign(Object.assign({}, model.metadata.toJSON()), cellId));
    // Set response handler
    future.onReply = (msg) => {
        console.log('Handling kernel response', msg);
        // Only work with `ok` results
        const content = msg.content;
        if (content.status !== 'ok') {
            return;
        }
        console.log('Clear existing metadata');
        // Clear metadata if present
        cell.model.metadata.delete(_metadata__WEBPACK_IMPORTED_MODULE_0__.metadataSection);
        // Store results as metadata
        const expressions = [];
        for (const key in content.user_expressions) {
            const expr = namedExpressions.get(key);
            if (expr === undefined) {
                console.error('namedExpressions doesn\'t have key. This should never happen');
                continue;
            }
            const result = content.user_expressions[key];
            const expressionMetadata = {
                expression: expr,
                result: result
            };
            expressions.push(expressionMetadata);
            console.log(`Saving ${expr} to cell attachments`, expressionMetadata);
        }
        // Update cell metadata
        cell.model.metadata.set(_metadata__WEBPACK_IMPORTED_MODULE_0__.metadataSection, expressions);
    };
    await future.done;
}


/***/ }),

/***/ "./lib/metadata.js":
/*!*************************!*\
  !*** ./lib/metadata.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "metadataSection": () => (/* binding */ metadataSection)
/* harmony export */ });
const metadataSection = 'user_expressions';


/***/ }),

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "plugin": () => (/* binding */ plugin)
/* harmony export */ });
/* harmony import */ var _tokenize__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokenize */ "./lib/tokenize.js");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @agoose77/jupyterlab-markup */ "webpack/sharing/consume/default/@agoose77/jupyterlab-markup");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__);


const PACKAGE_NS = '@agoose77/jupyterlab-imarkdown';
/**
 * Captures expressions as data-attributes
 */
const plugin = (0,_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__.simpleMarkdownItPlugin)(PACKAGE_NS, {
    id: 'markdown-it-expression',
    title: 'Create spans with stored expressions from Markdown',
    description: 'Embed Markdown text in a data attribute in rendered spans',
    documentationUrls: {
        Plugin: '...'
    },
    plugin: async () => {
        return [_tokenize__WEBPACK_IMPORTED_MODULE_1__.expressionPlugin];
    }
});


/***/ }),

/***/ "./lib/tokenize.js":
/*!*************************!*\
  !*** ./lib/tokenize.js ***!
  \*************************/
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


/***/ }),

/***/ "./lib/user_expressions.js":
/*!*********************************!*\
  !*** ./lib/user_expressions.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "isError": () => (/* binding */ isError),
/* harmony export */   "isOutput": () => (/* binding */ isOutput)
/* harmony export */ });
function isOutput(output) {
    return output.status === 'ok';
}
function isError(output) {
    return output.status === 'error';
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.249cb2c99b5a834d12c9.js.map