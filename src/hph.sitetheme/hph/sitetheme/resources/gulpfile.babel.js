'use strict'
import gulp from 'gulp';
import gulpLoadPlugins from 'gulp-load-plugins';
import {create as bsCreate} from 'browser-sync';
import del from 'del';
import revDel from 'rev-del';
import args from 'yargs';
import {stream as wiredep} from 'wiredep';

const $ = gulpLoadPlugins();
const browserSync = bsCreate();

var cp = require('child_process');
var pkg = require('./package.json');
var cfg = require('./config.json');
var fs = require('fs');

// File where the favicon markups are stored
var FAVICON_DATA_FILE = cfg.favicon.dataFile;

var messages = {
    jekyllBuild: '<span style="color: grey">Running:</span> $ jekyll build'
};

var sourcesJS = {
    base: [
        cfg.paths.src + 'tether/dist/js/tether.js',
        cfg.paths.src + 'bootstrap/dist/js/bootstrap.js',
        cfg.paths.src + 'lazysizes/lazysizes.js',
        cfg.paths.src + 'jquery.marquee/jquery.marquee.js'
    ],
    all: [
        cfg.paths.src + 'jquery/dist/jquery.js',
        cfg.paths.src + 'modernizr/modernizr.js',
        cfg.paths.src + 'tether/dist/js/tether.js',
        cfg.paths.src + 'bootstrap/dist/js/bootstrap.js',
        cfg.paths.src + 'mailcheck/src/mailcheck.js',
        cfg.paths.src + 'JVFloat/jvfloat.js',
        cfg.paths.src + 'hideShowPassword/hideShowPassword.js',
        cfg.paths.src + 'lazysizes/lazysizes.js',
        cfg.paths.src + 'jquery.marquee/jquery.marquee.js'

    ]
};

var isProduction = args.env === 'dist';

/**
 * Build the Jekyll Site
 */
gulp.task('jekyll-build', function (done) {
    browserSync.notify(messages.jekyllBuild);
    return cp.spawn('jekyll', ['build'], {stdio: 'inherit'})
        .on('close', done);
});

gulp.task('browser-sync', function () {
    browserSync.init({
        notify: false,
        port: 9499,
        server: {
            baseDir: ['.tmp', cfg.paths.dist],
            routes: {
                '/scripts': cfg.paths.dist + 'scripts',
                '/styles': cfg.paths.dist + 'styles',
                '/assets': cfg.paths.dist + 'assets',
            }
        }
    });
});

gulp.task('bs-reload', function () {
    browserSync.reload();
});

gulp.task('styles', () => {
    return gulp.src(cfg.paths.app + 'sass/main.scss')
        .pipe($.plumber())
        .pipe($.sourcemaps.init())
        .pipe($.sass.sync({
            outputStyle: 'expanded',
            precision: 10,
            includePaths: [cfg.paths.src]
        }).on('error', $.sass.logError))
        .pipe($.autoprefixer({browsers: ['last 1 version']}))
        //.pipe($.csscomb())
        .pipe(gulp.dest(cfg.paths.dist + 'styles/'))
        .pipe($.cssnano())
        .pipe($.rename({
            basename: pkg.name,
            suffix: '.min'
        }))
        .pipe($.sourcemaps.write())
        .pipe(gulp.dest(cfg.paths.dist + 'styles/'))
        .pipe(browserSync.reload({stream: true}))
});

gulp.task('scripts', () => {
    return gulp.src(isProduction ? sourcesJS.all : sourcesJS.base)
        .pipe($.plumber({
            errorHandler: function (error) {
                console.log(error.message);
                this.emit('end');
            }
        }))
        // .pipe($.jshint())
        // .pipe($.jshint.reporter('default'))
        .pipe($.concat(pkg.name + '.js'))
        .pipe(gulp.dest(cfg.paths.dist + 'scripts/'))
        .pipe($.rename({suffix: '.min'}))
        .pipe($.uglify())
        .pipe(gulp.dest(cfg.paths.dist + 'scripts/'))
        .pipe(browserSync.reload({stream: true}));
})
;

gulp.task('images', () => {
    return gulp.src(cfg.paths.app + 'assets/img/**/*')
        .pipe($.if($.if.isFile, $.cache($.imagemin({
            progressive: true,
            interlaced: true,
            // don't remove IDs from SVGs, they are often used
            // as hooks for embedding and styling
            svgoPlugins: [{cleanupIDs: false}]
        }))
            .on('error', function (err) {
                console.log(err);
                this.end();
            })))
        .pipe(gulp.dest(cfg.paths.dist + 'assets/img'));
})
;

gulp.task('fonts', () => {
    return gulp.src(require('main-bower-files')({
        filter: '**/*.{eot,svg,ttf,woff,woff2}'
    }).concat(cfg.paths.app + 'assets/fonts/**/*'))
        .pipe(gulp.dest('.tmp/fonts'))
        .pipe(gulp.dest(cfg.paths.dist + 'assets/fonts'));
})
;

gulp.task('html', () => {
    return gulp.src(cfg.paths.dev + '{,*/}*.html')
        .pipe($.minifyHtml())
        .pipe(gulp.dest(cfg.paths.dist));
})
;

gulp.task('cb', () => {
    return gulp.src(cfg.paths.dist + 'styles/*.min.css')
        .pipe($.rev())
        .pipe(gulp.dest(cfg.paths.dist + 'styles'))
        .pipe($.rev.manifest())
        .pipe(revDel({dest: cfg.paths.dist + 'styles'}))
        .pipe(gulp.dest(cfg.paths.dist + 'styles'))
}
)
;

gulp.task('revreplace', () => {
    var manifest = gulp.src(cfg.paths.dist + '/styles/rev-manifest.json');
return gulp.src(cfg.paths.dev + '/{,*/}*.html')
    .pipe(revReplace({manifest: manifest}))
    .pipe(gulp.dest(cfg.paths.dev));
})
;

gulp.task('replace', () => {
    return gulp.src(cfg.paths.dev + '/{,*/}*.html')
        .pipe(replace({
            patterns: [
                {
                    match: '../../assets/',
                    replacement: '../assets/'
                }
            ],
            usePrefix: false,
            preserveOrder: true
        }))
        .pipe(gulp.dest(cfg.paths.dev))
});

gulp.task('clean', del.bind(null, ['.tmp', cfg.paths.dist]));

gulp.task('serve', ['styles', 'scripts', 'jekyll-build', 'html'], () => {
    browserSync.init({
    notify: false,
    port: 9499,
    server: {
        baseDir: ['.tmp', cfg.paths.dist],
        routes: {
            '/scripts': cfg.paths.dist + '/scripts',
            '/styles': cfg.paths.dist + '/styles',
            '/assets': cfg.paths.dist + '/assets',
        }
    }
});

gulp.watch([
    cfg.paths.app + '/*.html',
    cfg.paths.app + '/scripts/*.js',
    cfg.paths.app + '/styles/*.css',
]).on('change', browserSync.reload);

gulp.watch(cfg.paths.app + "sass/**/*.scss", ['styles']);
gulp.watch(cfg.paths.app + "scripts/**/*.js", ['scripts']);
gulp.watch(cfg.paths.app + "{,*/}*.html", ['jekyll-build', 'html']);
});

gulp.task('default', ['browser-sync'], function () {
    gulp.watch(cfg.paths.app + "sass/**/*.scss", ['styles']);
    gulp.watch(cfg.paths.app + "scripts/**/*.js", ['scripts']);
    gulp.watch(cfg.paths.app + "*.html", ['bs-reload']);
});

// Generate the icons. This task takes a few seconds to complete.
// You should run it at least once to create the icons. Then,
// you should run it whenever RealFaviconGenerator updates its
// package (see the check-for-favicon-update task below).
gulp.task('generate-favicon', function(done) {
    $.realFavicon.generateFavicon({
        masterPicture: cfg.paths.app + cfg.favicon.iconPath + cfg.favicon.masterPicture,
        dest: cfg.paths.dist + cfg.favicon.iconPath,
        iconsPath: '/',
        design: {
            ios: {
                pictureAspect: 'backgroundAndMargin',
                backgroundColor: cfg.favicon.ios,
                margin: '14%',
                assets: {
                    ios6AndPriorIcons: false,
                    ios7AndLaterIcons: false,
                    precomposedIcons: false,
                    declareOnlyDefaultIcon: true
                }
            },
            desktopBrowser: {},
            windows: {
                pictureAspect: 'noChange',
                backgroundColor: cfg.favicon.windows,
                onConflict: 'override',
                assets: {
                    windows80Ie10Tile: false,
                    windows10Ie11EdgeTiles: {
                        small: false,
                        medium: true,
                        big: false,
                        rectangle: false
                    }
                }
            },
            androidChrome: {
                pictureAspect: 'backgroundAndMargin',
                margin: '17%',
                backgroundColor: cfg.favicon.androidBackground,
                themeColor: cfg.favicon.androidColor,
                manifest: {
                    name: pkg.name,
                    display: 'standalone',
                    orientation: 'notSet',
                    onConflict: 'override',
                    declared: true
                },
                assets: {
                    legacyIcon: false,
                    lowResolutionIcons: false
                }
            },
            safariPinnedTab: {
                pictureAspect: 'silhouette',
                themeColor: cfg.favicon.safariColor
            }
        },
        settings: {
            compression: 3,
            scalingAlgorithm: 'Mitchell',
            errorOnImageTooSmall: false
        },
        versioning: {
            paramName: 'v',
            paramValue: cfg.favicon.revisionKey
        },
        markupFile: FAVICON_DATA_FILE
    }, function() {
        done();
    });
});

// Inject the favicon markups in your HTML pages. You should run
// this task whenever you modify a page. You can keep this task
// as is or refactor your existing HTML pipeline.
gulp.task('inject-favicon-markups', function() {
    gulp.src([ cfg.paths.app + cfg.favicon.html ])
        .pipe($.realFavicon.injectFaviconMarkups(JSON.parse(fs.readFileSync(cfg.favicon.dataFile)).favicon.html_code))
        .pipe(gulp.dest(cfg.paths.app + cfg.favicon.htmlDist));
});

// Check for updates on RealFaviconGenerator (think: Apple has just
// released a new Touch icon along with the latest version of iOS).
// Run this task from time to time. Ideally, make it part of your
// continuous integration system.
gulp.task('check-for-favicon-update', function(done) {
    var currentVersion = JSON.parse(fs.readFileSync(cfg.favicon.dataFile)).version;
    $.realFavicon.checkForUpdates(currentVersion, function(err) {
        if (err) {
            throw err;
        }
    });
});
