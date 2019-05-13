import gulp from 'gulp';
import gulpLoadPlugins from 'gulp-load-plugins';
const $ = gulpLoadPlugins();

var cfg = require('./../config.json');


gulp.task('replace:base', () => {
    return gulp.src(cfg.paths.dev + '/{,*/}*.html')
        .pipe($.replaceTask({
            patterns: cfg.replacementPatterns.base,
            usePrefix: false,
            preserveOrder: true
        }))
        .pipe(gulp.dest(cfg.paths.dev))
});

gulp.task('replace:server', () => {
    return gulp.src(cfg.paths.base + cfg.paths.dev + '/{,*/}*.html')
        .pipe($.replaceTask({
            patterns: cfg.replacementPatterns.server,
            usePrefix: false,
            preserveOrder: true
        }))
        .pipe(gulp.dest(cfg.paths.base + cfg.paths.dev))
});


gulp.task('replace:pat', () => {
    return gulp.src(cfg.paths.base + cfg.paths.dev + '/{,*/}*.html')
        .pipe($.replaceTask({
            patterns: cfg.replacementPatterns.pat,
            usePrefix: false,
            preserveOrder: true
        }))
        .pipe(gulp.dest(cfg.paths.base + cfg.paths.dev))
});

// Asset revision replacements
gulp.task('replace:revision:styles', () => {
    // var manifest = gulp.src(cfg.paths.base + cfg.paths.dist + '/styles/rev-manifest.json');
    return gulp.src([cfg.paths.dist + '/styles/rev-manifest.json',
                    cfg.paths.dev + '/**/*.html'])
    // .pipe($.revReplace({manifest: manifest}))
    .pipe($.revCollector({
        replaceReved: true,
        dirReplacements: {
            '/styles': '/styles',
            '/scripts': '/scripts'
        }
    }) )
    .pipe(gulp.dest(cfg.paths.dev));
})
;

gulp.task('replace:revision:css', () => {
    var manifest = gulp.src(cfg.paths.dist + '/styles/rev-manifest.json');
return gulp.src(cfg.paths.dev + '/**/*.html')
    .pipe($.revReplace({manifest: manifest}))
    .pipe(gulp.dest(cfg.paths.dev));
})
;

gulp.task('replace:revision:scripts', () => {
    var manifest = gulp.src(cfg.paths.base + cfg.paths.dist + '/scripts/rev-manifest.json');
    return gulp.src(cfg.paths.base + cfg.paths.dev + '/**/*.html')
        .pipe($.revReplace({manifest: manifest}))
        .pipe(gulp.dest(cfg.paths.base + cfg.paths.dev));
})
;
