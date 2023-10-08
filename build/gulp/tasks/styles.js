import gulp from 'gulp';
import pump from 'pump';
import {create as bsCreate} from 'browser-sync';
import gulpLoadPlugins from 'gulp-load-plugins';

const $ = gulpLoadPlugins();
const browserSync = bsCreate();


var cfg = require('./../config.json');
var pkg = require('./../package.json');

// Styles build task
export function styles(cb) {
    pump([
        gulp.src(cfg.paths.theme + 'scss/main.scss'),
        $.plumber(),
        $.sourcemaps.init(),
        $.sass.sync({
            outputStyle: 'expanded',
            precision: 10,
            includePaths: [cfg.paths.src]
        }).on('error', $.sass.logError),
        $.autoprefixer(),
        gulp.dest(cfg.paths.dist + 'styles/'),
        $.cssnano(),
        $.rename({
            basename: cfg.name,
            suffix: '.min'
        }),
        $.sourcemaps.write(),
        gulp.dest(cfg.paths.dist + 'styles/'),
        browserSync.reload({stream: true})
    ], cb);
};

styles.description = 'Compile stylesheet from sass partials and minimize for production';


export function stylesDev() {
    return gulp.src(cfg.paths.app + 'scss/main.scss')
        .pipe($.plumber())
        .pipe($.sourcemaps.init())
        .pipe($.sass.sync({
            outputStyle: 'expanded',
            precision: 10,
            includePaths: [cfg.paths.src]
        }).on('error', $.sass.logError))
        .pipe($.autoprefixer())
        //.pipe($.csscomb())
        .pipe(gulp.dest(cfg.paths.dist + 'styles/'))
        .pipe($.rename({
            basename: pkg.name
        }))
        .pipe($.sourcemaps.write())
        .pipe(gulp.dest(cfg.paths.dist + 'styles/'))
        .pipe(browserSync.reload({stream: true}))
};

stylesDev.description = 'Compile stylesheet from sass partials';


// Styles build task
export function stylesEditor(cb) {
    pump([
        gulp.src(cfg.paths.app + 'scss/wysiwyg.scss'),
        $.plumber(),
        $.sourcemaps.init(),
        $.sass.sync({
            outputStyle: 'expanded',
            precision: 10,
            includePaths: [cfg.paths.src]
        }).on('error', $.sass.logError),
        $.autoprefixer(),
        gulp.dest(cfg.paths.dist + 'styles/'),
        $.cssnano(),
        $.rename({
            basename: 'wysiwyg',
            suffix: '.min'
        }),
        $.sourcemaps.write(),
        gulp.dest(cfg.paths.dist + 'styles/'),
        browserSync.reload({stream: true})
    ], cb);
};

stylesEditor.description = 'Compile stylesheet for wysiwyg editor';


// Stylesheet builds
gulp.task('styles:dev', stylesDev);
gulp.task('styles:dist', styles);
gulp.task('styles:editor', stylesEditor);
