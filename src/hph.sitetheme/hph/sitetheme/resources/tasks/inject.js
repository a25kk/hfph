import gulp from 'gulp';
import pump from 'pump';
import gulpLoadPlugins from 'gulp-load-plugins';
const $ = gulpLoadPlugins();

var pkg = require('./../package.json');
var cfg = require('./../config.json');

const ignoredPaths = [
    cfg.paths.dist,
    '../' + cfg.paths.dist,
    '../../' + cfg.paths.dist,
    '../../../' + cfg.paths.dist
]

export function inject() {
    return gulp.src(cfg.paths.dev + '**/*.html')
    // Look for any CSS files in the 'stylesheets' directory
    // Don't read the files for performance and ignore the base directory
        .pipe($.inject(gulp.src(cfg.paths.dist + 'styles/' + pkg.name + '.min.css',
            {read: false}),
            {relative: false},
            {removeTags: true},
            {ignorePath: ['../','../../','../../../', '/dist/', 'dist/']}
        ))
        // Output the file back into it's directory
        .pipe(gulp.dest(cfg.paths.dev))
};

export function injectStyles(cb) {
    pump([
            gulp.src(cfg.paths.dev + '**/*.html'),
            inject(gulp.src(cfg.paths.dist + 'styles/' + pkg.name + '.min.css',
                {read: false}),
                {relative: false},
                {removeTags: true},
                {ignorePath: ['../','../../','../../../','dist/', '/dist/']}
            ),
            gulp.dest(cfg.paths.dev)
        ],
        cb
    );
};


export function injectSprite() {
    return gulp.src(cfg.paths.dev + '**/*.html')
    // Look for any CSS files in the 'stylesheets' directory
    // Don't read the files for performance and ignore the base directory
        .pipe($.inject(gulp.src(cfg.paths.dist + 'assets/symbol/svg/' + '*.svg',
            {read: false}),
            {relative: false},
            {removeTags: true},
            {ignorePath: ['../','../../','../../../', '/dist/', 'dist/']}
        ))
        // Output the file back into it's directory
        .pipe(gulp.dest(cfg.paths.dev))
};


gulp.task('inject:head', inject);
gulp.task('inject:head:styles', injectStyles);
gulp.task('inject:head:sprite', injectSprite);

