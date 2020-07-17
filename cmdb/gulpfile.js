const {series, src, dest} = require('gulp');
var path = require('path')

function jquery() {
    const files = [
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/jquery/dist/jquery.slim.min.js',
        'node_modules/jquery.easing/jquery.easing.min.js',
    ]
    return src(files).pipe(dest('pages/static/pages/jquery/'))
}

function jqueryui() {
    const files = [
        'node_modules/jquery-ui-dist/jquery-ui.min.css',
        'node_modules/jquery-ui-dist/jquery-ui.min.js',
    ]
    return src(files).pipe(dest('pages/static/pages/jqueryui/')),
        src(path.join('node_modules/jquery-ui-dist/images/', "*")).pipe(dest('pages/static/pages/jqueryui/images/'))
}


function angularjs() {
    const files = [
        'node_modules/angular/angular.min.js',
        'node_modules/angular-animate/angular-animate.min.js',
        'node_modules/angular-route/angular-route.min.js',
        'node_modules/angular-aria/angular-aria.min.js',
        'node_modules/angular-messages/angular-messages.min.js',
    ]
    return src(files).pipe(dest('pages/static/pages/angularjs/'))
}

function moment() {
    const files = [
        'node_modules/moment/min/moment.min.js',
    ]
    return src(files).pipe(dest('pages/static/pages/moment/'))
}

function bootstrap() {
    const files = [
        'node_modules/bootstrap/dist/js/bootstrap.min.js',
        'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js',
        'node_modules/bootstrap/dist/css/bootstrap.min.css',
    ]
    return src(files).pipe(dest('pages/static/pages/bootstrap/'))
}


function sbAdmin2() {
    const files = [
        'node_modules/startbootstrap-sb-admin-2/vendor/fontawesome-free/css/all.min.css',
        'node_modules/startbootstrap-sb-admin-2/vendor/jquery-easing/jquery.easing.min.js',
        'node_modules/startbootstrap-sb-admin-2/css/sb-admin-2.min.css',
        'node_modules/startbootstrap-sb-admin-2/js/sb-admin-2.min.js',]
    return src(files).pipe(dest('pages/static/pages/sbAdmin2/'))
}


function popper() {
    const files = [
        'node_modules/popper.js/dist/umd/popper.min.js',

    ]
    return src(files).pipe(dest('pages/static/pages/popper/'))
}

function animate() {
    const files = [
        'node_modules/animate.css/animate.min.css',
    ]
    return src(files).pipe(dest('pages/static/pages/animate/'))
}

function socketIO() {
    const files = [
        'node_modules/socket.io-client/dist/socket.io.js',
    ]
    return src(files).pipe(dest('pages/static/pages/socketio/'))
}


function xterm() {
    const files = [
        'node_modules/xterm/lib/xterm.js',
        'node_modules/xterm/css/xterm.css',
    ]
    return src(files).pipe(dest('pages/static/pages/xterm/'))
}

function echarts() {
    const files = [
        'node_modules/echarts/dist/echarts.min.js',
    ]
    return src(files).pipe(dest('pages/static/pages/echarts/'))
}

function fontawesome() {
    const files = [
        'node_modules/@fortawesome/fontawesome-free/js/',
        'node_modules/@fortawesome/fontawesome-free/css/all.min.css',
    ]
    return src(files).pipe(dest('pages/static/pages/fontawesome/'))
}

function webfonts() {
    const files = [
        'node_modules/@fortawesome/fontawesome-free/webfonts/fa-regular-400.woff2',
        'node_modules/@fortawesome/fontawesome-free/webfonts/fa-regular-400.woff',
        'node_modules/@fortawesome/fontawesome-free/webfonts/fa-regular-400.ttf',
        'node_modules/@fortawesome/fontawesome-free/webfonts/fa-brands-400.woff2',
        'node_modules/@fortawesome/fontawesome-free/webfonts/fa-brands-400.woff',
        'node_modules/@fortawesome/fontawesome-free/webfonts/fa-brands-400.ttf',
        'node_modules/@fortawesome/fontawesome-free/webfonts/fa-solid-900.woff2',
    ]
    return src(files).pipe(dest('pages/static/pages/webfonts/'))
}

exports.default = series(jquery, angularjs, moment, bootstrap,
    sbAdmin2, popper, animate, socketIO, xterm, echarts,
    fontawesome, webfonts, jqueryui)
