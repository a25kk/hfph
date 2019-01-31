import gulp from 'gulp';
import del from 'del';
import revDel from 'rev-del';
import gulpLoadPlugins from 'gulp-load-plugins';
import {cleanAssets, cleanBase} from "./clean";
const $ = gulpLoadPlugins();

var cfg = require('./../config.json');
var fs = require('fs');


export function revisionStyles() {
    if (fs.existsSync(cfg.paths.dist + 'styles/rev-manifest.json')) {
        var manifest = fs.readFileSync(cfg.paths.dist + 'styles/rev-manifest.json', 'utf8');
        del.sync(Object.values(JSON.parse(manifest)), {'cwd': cfg.paths.dist + 'styles/'})
    }
    return gulp.src(cfg.paths.dist + 'styles/' + cfg.name + '.min.css')
        .pipe($.rev())
        .pipe(gulp.dest(cfg.paths.dist + 'styles'))
        .pipe($.rev.manifest())
        .pipe(revDel({dest: cfg.paths.dist + 'styles'}))
        .pipe(gulp.dest(cfg.paths.dist + 'styles'))
};

export function revisionScripts() {
    return gulp.src(cfg.paths.dist + 'scripts/' + cfg.name + 'min.js')
        .pipe($.rev())
        .pipe(gulp.dest(cfg.paths.dist + 'scripts'))
        .pipe($.rev.manifest())
        .pipe(revDel({dest: cfg.paths.dist + 'scripts'}))
        .pipe(gulp.dest(cfg.paths.dist + 'scripts'))
};

// Revision and cache bust tasks
gulp.task('revision:styles', revisionStyles);
gulp.task('revision:scripts', revisionScripts);
