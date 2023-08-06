"use strict";
(self["webpackChunk_agoose77_jupyterlab_imarkdown"] = self["webpackChunk_agoose77_jupyterlab_imarkdown"] || []).push([["lib_index_js"],{

/***/ "./lib/actions.js":
/*!************************!*\
  !*** ./lib/actions.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "executeUserExpressions": () => (/* binding */ executeUserExpressions),
/* harmony export */   "notebookExecuted": () => (/* binding */ notebookExecuted)
/* harmony export */ });
/* harmony import */ var _metadata__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./metadata */ "./lib/metadata.js");

function isMarkdownCell(cell) {
    return cell.model.type === 'markdown';
}
/**
 * Load user expressions for given XMarkdown cell from kernel.
 * Store results in cell attachments.
 */
async function executeUserExpressions(cell, sessionContext) {
    var _a;
    // Check we have a kernel
    const kernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
    if (!kernel) {
        throw new Error('Session has no kernel.');
    }
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
    // Perform request
    console.debug('Performing kernel request', content);
    const future = kernel.requestExecute(content, false, Object.assign(Object.assign({}, model.metadata.toJSON()), cellId));
    // Set response handler
    future.onReply = (msg) => {
        console.debug('Handling kernel response', msg);
        // Only work with `ok` results
        const content = msg.content;
        if (content.status !== 'ok') {
            console.error('Kernel response was not OK', msg);
            return;
        }
        console.debug('Clear existing metadata');
        // Clear metadata if present
        cell.model.metadata.delete(_metadata__WEBPACK_IMPORTED_MODULE_0__.metadataSection);
        // Store results as metadata
        const expressions = [];
        for (const key in content.user_expressions) {
            const expr = namedExpressions.get(key);
            if (expr === undefined) {
                console.error("namedExpressions doesn't have key. This should never happen");
                continue;
            }
            const result = content.user_expressions[key];
            const expressionMetadata = {
                expression: expr,
                result: result
            };
            expressions.push(expressionMetadata);
            console.debug(`Saving ${expr} to cell attachments`, expressionMetadata);
        }
        // Update cell metadata
        cell.model.metadata.set(_metadata__WEBPACK_IMPORTED_MODULE_0__.metadataSection, expressions);
    };
    await future.done;
}
function notebookExecuted(notebook, cell, tracker) {
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
    console.debug(`Markdown cell ${cell.model.id} was executed, waiting for render to complete ...`);
    cell.doneRendering
        .then(() => executeUserExpressions(cell, ctx))
        .catch(console.error)
        .then(() => cell.renderExpressionsFromMetadata())
        .catch(console.error);
}


/***/ }),

/***/ "./lib/cell.js":
/*!*********************!*\
  !*** ./lib/cell.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EXPR_CLASS": () => (/* binding */ EXPR_CLASS),
/* harmony export */   "IMarkdownCell": () => (/* binding */ IMarkdownCell)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _metadata__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./metadata */ "./lib/metadata.js");
/* harmony import */ var _renderers__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./renderers */ "./lib/renderers.js");
/* harmony import */ var _expression__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./expression */ "./lib/expression.js");






// CSS class for expression nodes
const EXPR_CLASS = 'eval-expr';
class IMarkdownCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.MarkdownCell {
    constructor(options) {
        super(options);
        this.__lastContent = '';
        this._expressions = [];
        this._doneRendering = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
        this.__rendermime = options.rendermime.clone();
        this.__rendermime.addFactory(_renderers__WEBPACK_IMPORTED_MODULE_3__.textRendererFactory);
        this._expressions = [];
        // Dispose of existing expressions
        this._triageElement = document.createElement('div');
        this._triageElement.setAttribute('visibility', 'hidden');
        this.node.appendChild(this._triageElement);
    }
    /**
     * Get an array of names to kernel expressions.
     */
    get expressions() {
        return this._expressions.map(node => node.expression);
    }
    /**
     * Whether the Markdown renderer has finished rendering.
     */
    get doneRendering() {
        return this._doneRendering.promise;
    }
    /**
     * Update rendered expressions from current attachment MIME-bundles
     */
    renderExpressionsFromMetadata() {
        console.debug('Rendering expressions', this.expressions);
        const expressionsMetadata = this.model.metadata.get(_metadata__WEBPACK_IMPORTED_MODULE_4__.metadataSection);
        if (expressionsMetadata === undefined) {
            console.debug('Aborting rendering of expressions: no metadata', this.expressions);
            return Promise.reject();
        }
        // Check we have enough keys
        if (expressionsMetadata.length !== this._expressions.length) {
            console.error('Aborting rendering of expressions: expressions mismatch', this.expressions, expressionsMetadata);
            return Promise.reject();
        }
        // Loop over expressions and render them from the cell attachments
        const promises = [];
        this._expressions.forEach((node, index) => {
            const metadata = expressionsMetadata[index];
            // Can't render the remaining keys. Should we have aborted earlier?
            if (metadata.expression !== node.expression) {
                console.error(`Metadata expression does not match Markdown expression at index ${index}`);
                return;
            }
            if (metadata.result === undefined) {
                console.error(`Metadata has no result at index ${index}`);
                return;
            }
            // Create element and replace it in the parent's DOM tree
            console.debug(`Rendering ${metadata.expression}`);
            // Update the placeholder once rendered
            promises.push(node.renderExpression(metadata.result));
        });
        return Promise.all(promises).then();
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
        // Therefore, this is sometimes executed before the DOM is updated.
        super.renderInput(widget);
        const currentContent = this.model.value.text;
        // If the content has changed
        if (this.__lastContent !== undefined && // Not sure why this happens, but run with it.
            this.__lastContent !== currentContent) {
            this._doneRendering = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
            // Wait for rendering to complete
            this._waitForRender(widget, 2)
                .then(() => {
                this._clearExpressions();
                // Identify markup expressions by placeholders
                this._identifyExpressions(widget);
                // Replace placeholders with content from attachments
                return this.renderExpressionsFromMetadata();
            })
                .catch(console.error)
                .then(() => {
                this._doneRendering.resolve();
            });
            this.__lastContent = currentContent;
        }
    }
    /**
     * Dispose of the rendered expressions
     */
    _clearExpressions() {
        console.debug('Clearing expressions');
        if (this._expressions !== undefined && this._triageElement !== undefined) {
            this._expressions.forEach(expr => {
                if (!document.body.contains(expr.node)) {
                    this._triageElement.appendChild(expr.node);
                }
                expr.dispose();
            });
        }
        this._expressions = [];
    }
    /**
     * Parse the rendered markdown, and store placeholder and expression mappings
     */
    _identifyExpressions(widget) {
        const exprInputNodes = widget.node.querySelectorAll(`input.${EXPR_CLASS}`);
        // Store expressions & their current placeholders
        this._expressions = [...exprInputNodes].map((elem) => {
            const element = elem;
            // Create expression
            const expression = new _expression__WEBPACK_IMPORTED_MODULE_5__.RenderedExpression({
                expression: element.value,
                trusted: this.model.trusted,
                rendermime: this.__rendermime,
                safe: 'any'
            });
            // Inject widget into DOM
            _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget.attach(expression, element.parentElement || widget.node, element);
            console.assert(expression.isAttached, 'expr should be attached', expression);
            element.remove();
            // Return expression node
            return expression;
        });
        console.debug('Found expressions', this._expressions);
    }
}


/***/ }),

/***/ "./lib/expression.js":
/*!***************************!*\
  !*** ./lib/expression.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RenderedExpression": () => (/* binding */ RenderedExpression),
/* harmony export */   "RenderedExpressionError": () => (/* binding */ RenderedExpressionError)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _user_expressions__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./user_expressions */ "./lib/user_expressions.js");


class RenderedExpressionError extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this.addClass('im-RenderedExpressionError');
    }
}
class RenderedExpression extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(options) {
        super();
        this.trusted = options.trusted;
        this.expression = options.expression;
        this.rendermime = options.rendermime;
        this.safe = options.safe;
        this.addClass('im-RenderedExpression');
        // We can only hold one renderer at a time
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.SingletonLayout());
        layout.widget = new RenderedExpressionError();
    }
    renderExpression(payload) {
        const layout = this.layout;
        let options;
        if ((0,_user_expressions__WEBPACK_IMPORTED_MODULE_1__.isOutput)(payload)) {
            // Output results are simple to reinterpret
            options = {
                trusted: this.trusted,
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
        // Invoke MIME renderer
        const model = this.rendermime.createModel(options);
        // Select preferred mimetype for bundle
        const mimeType = this.rendermime.preferredMimeType(model.data, this.safe);
        if (mimeType === undefined) {
            console.error("Couldn't find mimetype for ", model);
            // Create error
            layout.widget = new RenderedExpressionError();
            return Promise.resolve();
        }
        // Create renderer
        const renderer = this.rendermime.createRenderer(mimeType);
        layout.widget = renderer;
        console.assert(renderer.isAttached, 'renderer was not attached!', renderer);
        // Render model
        return renderer.renderModel(model);
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
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _cell__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./cell */ "./lib/cell.js");
/* harmony import */ var _actions__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./actions */ "./lib/actions.js");




class IMarkdownContentFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.ContentFactory {
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
        return new _cell__WEBPACK_IMPORTED_MODULE_2__.IMarkdownCell(options).initializeState();
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
        return new IMarkdownContentFactory({ editorFactory });
    }
};
/**
 * The notebook cell executor.
 */
const executor = {
    id: '@agoose77/jupyterlab-imarkdown:executor',
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    autoStart: true,
    activate: (app, tracker) => {
        console.log('Using jupyterlab-imarkdown:executor');
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed.connect((sender, value) => {
            const { notebook, cell } = value;
            (0,_actions__WEBPACK_IMPORTED_MODULE_3__.notebookExecuted)(notebook, cell, tracker);
        });
        return;
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [factory, executor];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


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

/***/ "./lib/renderers.js":
/*!**************************!*\
  !*** ./lib/renderers.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RenderedText": () => (/* binding */ RenderedText),
/* harmony export */   "renderText": () => (/* binding */ renderText),
/* harmony export */   "textRendererFactory": () => (/* binding */ textRendererFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__);

/**
 * Render text into a host node.
 *
 * @param options - The options for rendering.
 *
 * @returns A promise which resolves when rendering is complete.
 */
function renderText(options) {
    // Unpack the options.
    const { host, sanitizer, source } = options;
    // Create the raw text content.
    let content;
    content = sanitizer.sanitize(source, {
        allowedTags: []
    });
    // Remove quotes if required
    if (options.strip_quotes) {
        content = content.replace(/^(["'])(.*)\1$/, '$2');
    }
    // Set the sanitized content for the host node.
    const span = document.createElement('span');
    span.innerHTML = content;
    host.appendChild(span);
    // Return the rendered promise.
    return Promise.resolve(undefined);
}
/**
 * A widget for displaying plain text.
 */
class RenderedText extends _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__.RenderedCommon {
    /**
     * Construct a new rendered text widget.
     *
     * @param options - The options for initializing the widget.
     */
    constructor(options) {
        super(options);
        this.addClass('im-RenderedText');
    }
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @returns A promise which resolves when rendering is complete.
     */
    render(model) {
        return renderText({
            host: this.node,
            sanitizer: this.sanitizer,
            source: String(model.data[this.mimeType]),
            strip_quotes: true
        });
    }
}
/**
 * A mime renderer factory for plain and jupyter console text data.
 */
const textRendererFactory = {
    safe: true,
    mimeTypes: ['text/plain'],
    defaultRank: 100,
    createRenderer: options => new RenderedText(options)
};


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
//# sourceMappingURL=lib_index_js.6ee0bb0b142a17dac4ef.js.map