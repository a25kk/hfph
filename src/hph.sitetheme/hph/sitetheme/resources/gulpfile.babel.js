'use strict'
import gulp from 'gulp';
import gulpLoadPlugins from 'gulp-load-plugins';
import {create as bsCreate} from 'browser-sync';

var HubRegistry = require('gulp-hub');

/* load some files into the registry */
var hub = new HubRegistry([
    './tasks/clean.js',
    './tasks/collect.js',
    './tasks/favicon.js',
    './tasks/sprite.js',
    './tasks/jekyll.js',
    './tasks/styles.js',
    './tasks/inject.js',
    './tasks/revision.js',
    './tasks/replace.js'
]);

/* tell gulp to use the tasks just loaded */
gulp.registry(hub);


const $ = gulpLoadPlugins();
const browserSync = bsCreate();

// Load configuration
var cfg = require('./config.json');



/*
 * TASKS
 *
 */

// Browser sync
gulp.task('bs:reload', function (done) {
    browserSync.reload();
    done();
});


// Build tasks
const buildInit = gulp.series(
    'clean:dist',
    gulp.parallel('collect:fonts', 'collect:images', 'collect:scripts:vendor')
);

buildInit.description = 'Delete distribution and collect fresh copies of static assets';

gulp.task('build:init', buildInit);

// Build collect
const buildCollect = gulp.parallel(
    'collect:fonts', 'collect:images', 'collect:scripts:vendor'
);
buildCollect.description = 'Collect static assets for production build';

gulp.task('build:collect', buildCollect);

// Base tasks
const buildBase = gulp.series(
    'jekyll:build',
    gulp.parallel('styles:dist', 'collect:scripts:app'),
    'inject:head'
);

buildBase.description = 'Compile templates/styles and collect scripts for production';

gulp.task('build:base', buildBase);


const buildPat = gulp.series(
    'build:base',
    'replace:pat',
    'collect:html'
);
buildPat.description = 'Build distribution for ++theme++ support';

gulp.task('build:pat', buildPat);

const buildDevelopment = gulp.series(
    'build:base',
    'replace:base',
    'collect:html'
);
buildDevelopment.description = 'Build local development environment';

gulp.task('build:dev', buildDevelopment);


const buildDistBase = gulp.series(
    'build:base',
    'replace:base',
    'revision:styles',
    'replace:revision:styles',
    'collect:html'
);
buildDistBase.description = 'Build production distribution';

gulp.task('build:dist:base', buildDistBase);


const buildDistFull = gulp.series(
    'build:init',
    'build:dist:base'
);
buildDistFull.description = 'Clean distribution and build full production bundle';

gulp.task('build:dist:full', buildDistFull);


gulp.task('dev:watch:styles', function () {
    gulp.watch(cfg.paths.app + "sass/**/*.scss", gulp.series(
        'styles:dist'
        // browserSync.reload()
        )
    )
});

gulp.task('dev:watch', function () {
    gulp.watch(cfg.paths.app + "sass/**/*.scss", gulp.series(
        'styles:dist'
    )
    );
    gulp.watch(cfg.paths.app + "scripts/**/*.js", gulp.series(
        'collect:scripts:app'
        )
    );
    gulp.watch(cfg.paths.app + "**/*.html", gulp.series(
        'build:dist:base'
        )
    );
});

// Run development build
gulp.task('collect', buildCollect);

// Build distribution versions of styles and scripts
gulp.task('dist', buildDistBase);

// Rebuild whole theme for distribution
gulp.task('build', buildDistFull);

// Development build usable with standalone Plone backend
gulp.task('pat', buildPat);

// Development Server
// gulp.task('serve', ['dev:serve']);

// gulp.task('watch', ['dev:watch'])

// Start working with the styles
gulp.task('default',
    gulp.series(
        'dev:watch:styles'
    )
);

