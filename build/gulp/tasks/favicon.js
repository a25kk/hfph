import gulp from 'gulp';
import gulpLoadPlugins from 'gulp-load-plugins';
const $ = gulpLoadPlugins();

var cfg = require('./../config.json');
var pkg = require('./../package.json');
var fs = require('fs');

// Generate the icons. This task takes a few seconds to complete.
// You should run it at least once to create the icons. Then,
// you should run it whenever RealFaviconGenerator updates its
// package (see the check-for-favicon-update task below).
gulp.task('favicon:generate', function(done) {
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
        markupFile: cfg.favicon.dataFile
    }, function() {
        done();
    });
});

// Inject the favicon markups in your HTML pages. You should run
// this task whenever you modify a page. You can keep this task
// as is or refactor your existing HTML pipeline.
gulp.task('favicon:inject', function() {
    return gulp.src([ cfg.paths.app + cfg.favicon.html ])
        .pipe($.realFavicon.injectFaviconMarkups(JSON.parse(fs.readFileSync(cfg.favicon.dataFile)).favicon.html_code))
        .pipe(gulp.dest(cfg.paths.app + cfg.favicon.htmlDist));
});

// Check for updates on RealFaviconGenerator (think: Apple has just
// released a new Touch icon along with the latest version of iOS).
// Run this task from time to time. Ideally, make it part of your
// continuous integration system.
gulp.task('favicon:update', function(done) {
    var currentVersion = JSON.parse(fs.readFileSync(cfg.favicon.dataFile)).version;
    $.realFavicon.checkForUpdates(currentVersion, function(err) {
        if (err) {
            throw err;
        }
    });
});
