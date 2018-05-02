import gulp from 'gulp';
import pump from 'pump';
import gulpLoadPlugins from 'gulp-load-plugins';
const $ = gulpLoadPlugins();

var es = require('event-stream');
var cfg = require('./../config.json');

var scriptSourcesVendor = {
    'vendor': cfg.scripts.src
}
var scriptSourcesApp = {
    'app': cfg.scripts.app
}

var scriptCollectionVendor = Object.keys(scriptSourcesVendor);
var scriptCollectionApp = Object.keys(scriptSourcesApp);

scriptCollectionVendor.forEach(function (libName) {
    gulp.task( 'scripts:'+libName, function () {
        return gulp.src(scriptSourcesVendor[libName], {'cwd': cfg.paths.src})
            .pipe(gulp.dest(cfg.paths.dist + 'scripts/'));
    });
});

gulp.task('collect:scripts:vendor',
    gulp.parallel(
        scriptCollectionVendor.map(function(name) { return 'scripts:'+name; })
    )
);

scriptCollectionApp.forEach(function (libName) {
    gulp.task( 'scripts:'+libName, function () {
        return gulp.src(scriptSourcesApp[libName], {'cwd': cfg.paths.app })
            .pipe(gulp.dest(cfg.paths.dist + 'scripts/'));
    });
});

gulp.task('collect:scripts:app',
    gulp.parallel(
        scriptCollectionApp.map(function(name) { return 'scripts:'+name; })
    )
);


export function collectImages() {
    return gulp.src(cfg.paths.app + 'assets/images/**/*')
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
        .pipe(gulp.dest(cfg.paths.dist + 'assets/images'));
};

gulp.task('collect:images', collectImages);

export function collectFonts() {
    return gulp.src(cfg.paths.app + 'assets/fonts/**/*')
        .pipe(gulp.dest(cfg.paths.dist + 'assets/fonts'));
};

collectFonts.description = 'Copy custom web fonts to distribution directory';

gulp.task('collect:fonts', collectFonts);

export function collectHtml() {
    return gulp.src(cfg.paths.dev + '{,*/}*.html')
        .pipe($.minifyHtml())
        .pipe(gulp.dest(cfg.paths.dist));
};

gulp.task('collect:html', collectHtml);
