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
        gulp.src(cfg.paths.app + 'sass/main.scss'),
        $.plumber(),
        $.sourcemaps.init(),
        $.sass.sync({
            outputStyle: 'expanded',
            precision: 10,
            includePaths: [cfg.paths.src]
        }).on('error', $.sass.logError),
        $.autoprefixer({browsers: ['last 4 version']}),
        gulp.dest(cfg.paths.dist + 'styles/'),
        $.cssnano(),
        $.rename({
            basename: pkg.name,
            suffix: '.min'
        }),
        $.sourcemaps.write(),
        gulp.dest(cfg.paths.dist + 'styles/'),
        browserSync.reload({stream: true})
    ], cb);
};

styles.description = 'Compile stylesheet from sass partials and minimize for production';


export function stylesDev() {
    return gulp.src(cfg.paths.app + 'sass/main.scss')
        .pipe($.plumber())
        .pipe($.sourcemaps.init())
        .pipe($.sass.sync({
            outputStyle: 'expanded',
            precision: 10,
            includePaths: [cfg.paths.src]
        }).on('error', $.sass.logError))
        .pipe($.autoprefixer({browsers: ['last 4 version']}))
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


// Stylesheet builds
gulp.task('styles:dev', stylesDev);
gulp.task('styles:dist', styles);
