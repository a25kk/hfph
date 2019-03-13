import gulp from 'gulp';
import {create as bsCreate} from 'browser-sync';
import gulpLoadPlugins from 'gulp-load-plugins';

const $ = gulpLoadPlugins();
const browserSync = bsCreate();


var cfg = require('./../config.json');
var pkg = require('./../package.json');

// Build and concat scripts
gulp.task('scripts', () => {
    return gulp.src(cfg.paths.base + cfg.scripts.base)
        .pipe($.plumber({
            errorHandler: function (error) {
                console.log(error.message);
                this.emit('end');
            }
        }))
        // .pipe($.jshint())
        // .pipe($.jshint.reporter('default'))
        .pipe($.concat(pkg.name + '.js'))
        .pipe(gulp.dest(cfg.paths.base + cfg.paths.dist + 'scripts/'))
        .pipe($.rename({suffix: '.min'}))
        .pipe($.uglify())
        .pipe(gulp.dest(cfg.paths.base + cfg.paths.dist + 'scripts/'))
        .pipe(browserSync.reload({stream: true}));
})
;

