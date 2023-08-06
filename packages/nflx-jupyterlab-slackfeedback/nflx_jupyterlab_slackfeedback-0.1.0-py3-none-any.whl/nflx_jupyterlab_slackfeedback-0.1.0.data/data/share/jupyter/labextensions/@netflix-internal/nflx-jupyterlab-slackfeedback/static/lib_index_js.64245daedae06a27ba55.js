"use strict";
(self["webpackChunk_netflix_internal_nflx_jupyterlab_slackfeedback"] = self["webpackChunk_netflix_internal_nflx_jupyterlab_slackfeedback"] || []).push([["lib_index_js"],{

/***/ "./lib/buttons.js":
/*!************************!*\
  !*** ./lib/buttons.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SlackFeedbackButtonExtension": () => (/* binding */ SlackFeedbackButtonExtension)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./commands */ "./lib/commands.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");




class SlackFeedbackButtonExtension {
    constructor(commands, _nfa) {
        this.commands = commands;
        this.nfa = _nfa;
    }
    createNew(widget, _context) {
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            label: 'Send Feedback',
            tooltip: 'Send feedback to the Notebooks team slack channel',
            icon: _icons__WEBPACK_IMPORTED_MODULE_2__.slackIcon,
            onClick: () => {
                this.commands.execute(_commands__WEBPACK_IMPORTED_MODULE_3__.openSlackFeedbackCommand);
                this.nfa.logFeatureEngaged('jl-user-feedback', 'toolbar-button-click');
            }
        });
        widget.toolbar.insertAfter('spacer', 'slack-feedback', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}


/***/ }),

/***/ "./lib/commands.js":
/*!*************************!*\
  !*** ./lib/commands.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "addCommands": () => (/* binding */ addCommands),
/* harmony export */   "cloneVersionCommand": () => (/* binding */ cloneVersionCommand),
/* harmony export */   "openSlackFeedbackCommand": () => (/* binding */ openSlackFeedbackCommand),
/* harmony export */   "openTimelineCommand": () => (/* binding */ openTimelineCommand),
/* harmony export */   "openTimelineVersionCommand": () => (/* binding */ openTimelineVersionCommand),
/* harmony export */   "restoreVersionCommand": () => (/* binding */ restoreVersionCommand)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _slackfeedback__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./slackfeedback */ "./lib/slackfeedback.js");


const openTimelineCommand = 'timeline:open';
const cloneVersionCommand = 'timeline:clone';
const restoreVersionCommand = 'timeline:restore';
const openTimelineVersionCommand = 'timeline:open-version';
const openSlackFeedbackCommand = 'slack-feedback:open';
function addCommands(app, nfa) {
    app.commands.addCommand(openSlackFeedbackCommand, {
        label: 'Open Slack Feedback Modal',
        caption: 'Open Slack Feedback Modal',
        execute: () => {
            const widget = new _slackfeedback__WEBPACK_IMPORTED_MODULE_1__.FeedbackWidget(nfa);
            nfa.logFeatureEngaged('timeline', 'sidebar-opened');
            if (!document.getElementById('feedback-slack'))
                _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget.attach(widget, document.body);
        }
    });
}


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "slackIcon": () => (/* binding */ slackIcon)
/* harmony export */ });
/* harmony import */ var _style_slack_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/slack.svg */ "./style/slack.svg");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);


const slackIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'nflx:slack-feedback',
    svgstr: _style_slack_svg__WEBPACK_IMPORTED_MODULE_1__["default"]
});


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
/* harmony import */ var _buttons__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./buttons */ "./lib/buttons.js");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./commands */ "./lib/commands.js");
/* harmony import */ var _netflix_internal_jupyterlab_analytics__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @netflix-internal/jupyterlab-analytics */ "webpack/sharing/consume/default/@netflix-internal/jupyterlab-analytics");
/* harmony import */ var _netflix_internal_jupyterlab_analytics__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_netflix_internal_jupyterlab_analytics__WEBPACK_IMPORTED_MODULE_0__);



/**
 * Initialization data for the nflx-jupyterlab-slackfeedback extension.
 */
const plugin = {
    id: 'nflx-jupyterlab-slackfeedback:plugin',
    autoStart: true,
    requires: [_netflix_internal_jupyterlab_analytics__WEBPACK_IMPORTED_MODULE_0__.INflxAnalytics],
    activate: activate
};
async function activate(app, analytics) {
    console.log('JupyterLab extension nflx-jupyterlab-slackfeedback is activated!');
    app.docRegistry.addWidgetExtension('notebook', new _buttons__WEBPACK_IMPORTED_MODULE_1__.SlackFeedbackButtonExtension(app.commands, analytics));
    (0,_commands__WEBPACK_IMPORTED_MODULE_2__.addCommands)(app, analytics);
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/slackfeedback.js":
/*!******************************!*\
  !*** ./lib/slackfeedback.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FeedbackWidget": () => (/* binding */ FeedbackWidget),
/* harmony export */   "getJupyterPrefix": () => (/* binding */ getJupyterPrefix)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_slack_feedback__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-slack-feedback */ "webpack/sharing/consume/default/react-slack-feedback/react-slack-feedback");
/* harmony import */ var react_slack_feedback__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_slack_feedback__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var typestyle__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! typestyle */ "./node_modules/typestyle/lib.es2015/index.js");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @material-ui/core */ "webpack/sharing/consume/default/@material-ui/core/@material-ui/core");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_material_ui_core__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_5__);






const panelWrapperClass = (0,typestyle__WEBPACK_IMPORTED_MODULE_3__.style)({
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    overflowY: 'auto',
    backgroundColor: 'var(--jp-layout-color1)!important'
});
function sendToServer(payload, success, error, nfa) {
    switch (payload.attachments[0].title) {
        case 'bug':
            nfa.logFeatureEngaged('jl-user-feedback', 'bug');
            break;
        case 'feature':
            nfa.logFeatureEngaged('jl-user-feedback', 'feauture');
            break;
        case 'improvement':
            nfa.logFeatureEngaged('jl-user-feedback', 'improvement');
            break;
    }
    payload['attachments'][0].author_name =
        window.location.pathname.split('/')[1] + '@netflix.com';
    return fetch(`${getJupyterPrefix()}api/slack/messages`, {
        method: 'POST',
        body: JSON.stringify(payload),
        mode: 'no-cors'
    })
        .then(success => removeElement())
        .catch(error);
}
class FeedbackWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    constructor(props) {
        super();
        this.addClass(panelWrapperClass);
        this.nfa = props;
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(SlackFeedbackComponent, { analytics: this.nfa });
    }
}
const removeElement = () => {
    let slackFeedbackElement = document.getElementById('feedback-slack');
    slackFeedbackElement === null || slackFeedbackElement === void 0 ? void 0 : slackFeedbackElement.remove();
};
function SlackFeedbackComponent(props) {
    let slackFeedback = document.getElementById('channel!');
    const officeHoursInfo = () => {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { marginBottom: '16px' } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_4__.Typography, { style: { fontSize: '16px', color: '#0088ff' } }, "Notebooks team has office hours!"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_4__.Typography, { style: { fontSize: '14px', color: 'GrayText' } }, "Join us every Thursday from 1-2pm PST"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { color: "textSecondary", style: { fontSize: '14px', color: 'HighlightText' }, href: "https://docs.google.com/spreadsheets/d/16ZybsUjazQltdTS1KPE8vob1imZ6E30kv-DUQFqjzsc/edit#gid=0", target: "_blank", rel: "noopener noreferrer" }, "Sign up here")));
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (document.getElementById('channel'))
            react_dom__WEBPACK_IMPORTED_MODULE_5___default().render(officeHoursInfo(), document.getElementById('channel'));
    }, [slackFeedback]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { id: "feedback-slack" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react_slack_feedback__WEBPACK_IMPORTED_MODULE_1___default()), { style: { display: 'none' }, open: true, channel: "#ask-notebooks", theme: react_slack_feedback__WEBPACK_IMPORTED_MODULE_1__.themes["default"], onClose: () => removeElement(), onSubmit: (payload, success, error) => sendToServer(payload, success, error, props.analytics)
                .then(success)
                .catch(error) })));
}
function getJupyterPrefix() {
    const windowPath = window.location.pathname;
    return windowPath.substring(0, windowPath.indexOf('lab'));
}


/***/ }),

/***/ "./style/slack.svg":
/*!*************************!*\
  !*** ./style/slack.svg ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"40\" height=\"40\" viewBox=\"0 0 40 40\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M25.0204 31.0599C27.2296 31.0599 29.0204 32.8508 29.0204 35.0599C29.0204 37.2691 27.2296 39.0599 25.0204 39.0599C22.8113 39.0599 21.0204 37.2691 21.0204 35.0599V31.0599H25.0204ZM14.9804 21.0199C17.1896 21.0199 18.9804 22.8108 18.9804 25.0199V35.0199C18.9804 37.2291 17.1896 39.0199 14.9804 39.0199C12.7713 39.0199 10.9804 37.2291 10.9804 35.0199V25.0199C10.9804 22.8108 12.7713 21.0199 14.9804 21.0199ZM8.9404 21.0199V25.0199C8.9404 27.2291 7.1496 29.0199 4.94043 29.0199C2.73129 29.0199 0.94043 27.2291 0.94043 25.0199C0.94043 22.8108 2.73129 21.0199 4.94043 21.0199H8.9404ZM35.0604 21.0199C37.2696 21.0199 39.0604 22.8108 39.0604 25.0199C39.0604 27.2291 37.2696 29.0199 35.0604 29.0199H25.0604C23.6314 29.0199 22.3109 28.2575 21.5963 27.0199C20.8818 25.7823 20.8818 24.2575 21.5963 23.0199C22.3109 21.7823 23.6314 21.0199 25.0604 21.0199H35.0604ZM35.0604 10.9799C37.2696 10.9799 39.0604 12.7708 39.0604 14.9799C39.0604 17.1891 37.2696 18.9799 35.0604 18.9799H31.0604V14.9799C31.0604 12.7708 32.8513 10.9799 35.0604 10.9799ZM25.0204 0.979941C27.2296 0.979941 29.0204 2.7708 29.0204 4.97994V14.9799C29.0204 17.1891 27.2296 18.9799 25.0204 18.9799C22.8113 18.9799 21.0204 17.1891 21.0204 14.9799V4.97994C21.0204 2.7708 22.8113 0.979941 25.0204 0.979941ZM14.9804 10.9599C17.1896 10.9599 18.9804 12.7508 18.9804 14.9599C18.9804 17.1691 17.1896 18.9599 14.9804 18.9599H4.98043C2.77129 18.9599 0.98043 17.1691 0.98043 14.9599C0.98043 12.7508 2.77129 10.9599 4.98043 10.9599H14.9804ZM14.9804 0.939941C17.1896 0.939941 18.9804 2.7308 18.9804 4.93994V8.9399H14.9804C12.7713 8.9399 10.9804 7.1491 10.9804 4.93994C10.9804 2.7308 12.7713 0.939941 14.9804 0.939941Z\" fill=\"black\"/>\n</svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.64245daedae06a27ba55.js.map