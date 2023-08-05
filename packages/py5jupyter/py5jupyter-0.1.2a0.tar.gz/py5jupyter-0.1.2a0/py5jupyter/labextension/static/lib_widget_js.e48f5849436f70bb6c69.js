"use strict";
(self["webpackChunkjupyter_py5"] = self["webpackChunkjupyter_py5"] || []).push([["lib_widget_js"],{

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports) {


var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.bufferToImage = void 0;
// *****************************************************************************
//
//   Part of the py5jupyter (& py5) library
//   Copyright (C) 2022 Jim Schmitz
//
//   This library is free software: you can redistribute it and/or modify it
//   under the terms of the GNU Lesser General Public License as published by
//   the Free Software Foundation, either version 2.1 of the License, or (at
//   your option) any later version.
//
//   This library is distributed in the hope that it will be useful, but
//   WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
//   General Public License for more details.
//
//   You should have received a copy of the GNU Lesser General Public License
//   along with this library. If not, see <https://www.gnu.org/licenses/>.
//
// *****************************************************************************
function bufferToImage(buffer) {
    return __awaiter(this, void 0, void 0, function* () {
        let url;
        const blob = new Blob([buffer], { type: 'image/jpeg' });
        url = URL.createObjectURL(blob);
        const img = new Image();
        return new Promise(resolve => {
            img.onload = () => {
                resolve(img);
            };
            img.src = url;
        });
    });
}
exports.bufferToImage = bufferToImage;
//# sourceMappingURL=utils.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// *****************************************************************************
//
//   Part of the py5jupyter (& py5) library
//   Copyright (C) 2022 Jim Schmitz
//
//   This library is free software: you can redistribute it and/or modify it
//   under the terms of the GNU Lesser General Public License as published by
//   the Free Software Foundation, either version 2.1 of the License, or (at
//   your option) any later version.
//
//   This library is distributed in the hope that it will be useful, but
//   WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
//   General Public License for more details.
//
//   You should have received a copy of the GNU Lesser General Public License
//   along with this library. If not, see <https://www.gnu.org/licenses/>.
//
// *****************************************************************************
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Py5SketchPortalView = exports.Py5SketchPortalModel = void 0;
// *****************************************************************************
//
//   Part of the py5jupyter (& py5) library
//   Copyright (C) 2022 Jim Schmitz
//
//   This library is free software: you can redistribute it and/or modify it
//   under the terms of the GNU Lesser General Public License as published by
//   the Free Software Foundation, either version 2.1 of the License, or (at
//   your option) any later version.
//
//   This library is distributed in the hope that it will be useful, but
//   WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
//   General Public License for more details.
//
//   You should have received a copy of the GNU Lesser General Public License
//   along with this library. If not, see <https://www.gnu.org/licenses/>.
//
// *****************************************************************************
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Low%20Level.html
class Py5SketchPortalModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: Py5SketchPortalModel.model_name, _model_module: Py5SketchPortalModel.model_module, _model_module_version: Py5SketchPortalModel.model_module_version, _view_name: Py5SketchPortalModel.view_name, _view_module: Py5SketchPortalModel.view_module, _view_module_version: Py5SketchPortalModel.view_module_version, width: '', height: '', value: new DataView(new ArrayBuffer(0)) });
    }
}
exports.Py5SketchPortalModel = Py5SketchPortalModel;
Py5SketchPortalModel.serializers = Object.assign(Object.assign({}, base_1.DOMWidgetModel.serializers), { value: {
        serialize: (value) => {
            return new DataView(value.buffer.slice(0));
        },
    } });
Py5SketchPortalModel.model_name = 'Py5SketchPortalModel';
Py5SketchPortalModel.model_module = version_1.MODULE_NAME;
Py5SketchPortalModel.model_module_version = version_1.MODULE_VERSION;
Py5SketchPortalModel.view_name = 'Py5SketchPortalView';
Py5SketchPortalModel.view_module = version_1.MODULE_NAME;
Py5SketchPortalModel.view_module_version = version_1.MODULE_VERSION;
class Py5SketchPortalView extends base_1.DOMWidgetView {
    render() {
        this._canvas = document.createElement('canvas');
        this._canvas.width = this.model.get('width');
        this._canvas.height = this.model.get('height');
        this._canvas.tabIndex = 0;
        const ctx = this._canvas.getContext('2d');
        if (ctx === null) {
            throw 'Could not create 2d context.';
        }
        else {
            this._ctx = ctx;
        }
        this._updateImgSrc();
        this.el.appendChild(this._canvas);
        this._canvas.addEventListener('keydown', {
            handleEvent: this.onKeyEvent.bind(this, 'key_down')
        });
        this._canvas.addEventListener('keypress', {
            handleEvent: this.onKeyEvent.bind(this, 'key_press')
        });
        this._canvas.addEventListener('keyup', {
            handleEvent: this.onKeyEvent.bind(this, 'key_up')
        });
        this._canvas.addEventListener('mouseenter', {
            handleEvent: this.onMouseEvent.bind(this, 'mouse_enter')
        });
        this._canvas.addEventListener('mousedown', {
            handleEvent: this.onMouseDown.bind(this)
        });
        this._canvas.addEventListener('mousemove', {
            handleEvent: this.onMouseEvent.bind(this, 'mouse_move')
        });
        this._canvas.addEventListener('mouseup', {
            handleEvent: this.onMouseEvent.bind(this, 'mouse_up')
        });
        this._canvas.addEventListener('mouseleave', {
            handleEvent: this.onMouseEvent.bind(this, 'mouse_leave')
        });
        this._canvas.addEventListener('click', {
            handleEvent: this.onMouseEvent.bind(this, 'mouse_click')
        });
        this._canvas.addEventListener('wheel', {
            handleEvent: this.onMouseWheel.bind(this)
        });
        // Python -> JavaScript update
        this.model.on('change:value', this._updateImgSrc, this);
    }
    _updateImgSrc() {
        return __awaiter(this, void 0, void 0, function* () {
            const img = yield utils_1.bufferToImage(this.model.get('value'));
            this._ctx.drawImage(img, 0, 0);
        });
    }
    // https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent
    onKeyEvent(event_name, event) {
        this.model.send(Object.assign({ event: event_name, key: event.key, repeat: event.repeat }, this.getModifiers(event)), {});
    }
    onMouseEvent(event_name, event) {
        this.model.send(Object.assign(Object.assign({ event: event_name, buttons: event.buttons }, this.getModifiers(event)), this.getCoordinates(event)), {});
    }
    onMouseDown(event) {
        // Bring focus to the img element, so keyboard events can be triggered
        this._canvas.focus();
        this.model.send(Object.assign(Object.assign({ event: 'mouse_down', buttons: event.buttons }, this.getModifiers(event)), this.getCoordinates(event)), {});
    }
    // https://developer.mozilla.org/en-US/docs/Web/API/GlobalEventHandlers
    onMouseWheel(event) {
        this.model.send(Object.assign(Object.assign({ event: 'mouse_wheel', buttons: event.buttons, wheel: ((event.deltaY != 0) ? event.deltaY : event.deltaX) }, this.getModifiers(event)), this.getCoordinates(event)), {});
    }
    getCoordinates(event) {
        // https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
        const rect = this._canvas.getBoundingClientRect();
        const x = (this._canvas.width * (event.clientX - rect.left)) / rect.width;
        const y = (this._canvas.height * (event.clientY - rect.top)) / rect.height;
        return { x, y };
    }
    getModifiers(event) {
        return { mod: (+event.shiftKey) * 1 + (+event.ctrlKey) * 2 + (+event.metaKey) * 4 + (+event.altKey) * 8 };
    }
}
exports.Py5SketchPortalView = Py5SketchPortalView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"jupyter-py5","version":"0.1.0","description":"py5 Jupyter tools","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com//py5jupyter","bugs":{"url":"https://github.com//py5jupyter/issues"},"license":"BSD-3-Clause","author":{"name":"Jim Schmitz","email":"jim@ixora.io"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com//py5jupyter"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf py5jupyter/labextension","clean:nbextension":"rimraf py5jupyter/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"py5jupyter/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.e48f5849436f70bb6c69.js.map