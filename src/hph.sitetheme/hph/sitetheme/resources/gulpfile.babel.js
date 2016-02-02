import gulp from 'gulp';
import gulpLoadPlugins from 'gulp-load-plugins';
import browserSync from 'browser-sync';
import del from 'del';
import args from 'yargs';
import {stream as wiredep} from 'wiredep';

const $ = gulpLoadPlugins();
const reload = browserSync.reload;

var cp = require('child_process');
var pkg = require('./package.json');

var messages = {
    jekyllBuild: '<span style="color: grey">Running:</span> $ jekyll build'
};

var basePaths = {
    app: 'app',
    dev: '_site',
    dist: 'dist',
    diazoPrefix: '/++theme++pkg.name.sitetheme',
    bower: 'bower_components/'
};

var sourcesJS = {
  base: [
    basePaths.bower + 'bootstrap-without-jquery/bootstrap3/bootstrap-without-jquery.js',
    basePaths.bower + 'lazysizes/lazysizes.js',
    basePaths.bower + 'flickity/dist/flickity.pkgd.js'
  ],
  all: [
    basePaths.bower +'jquery/dist/jquery.js',
    basePaths.bower +'modernizr/modernizr.js',
    basePaths.bower + 'bootstrap-without-jquery/bootstrap3/bootstrap-without-jquery.js',
    basePaths.bower +'mailcheck/src/mailcheck.js',
    basePaths.bower +'JVFloat/jvfloat.js',
    basePaths.bower +'hideShowPassword/hideShowPassword.js',
    basePaths.bower + 'lazysizes/lazysizes.js',
    basePaths.bower + 'flickity/dist/flickity.pkgd.js'

  ]
}

var isProduction = args.env === 'dist';

/**
 * Build the Jekyll Site
 */
gulp.task('jekyll-build', function (done) {
    browserSync.notify(messages.jekyllBuild);
    return cp.spawn('jekyll', ['build'], {stdio: 'inherit'})
        .on('close', done);
});

gulp.task('browser-sync', function() {
  browserSync({
    server: {
       baseDir: "./"
    }
  });
});

gulp.task('bs-reload', function () {
  browserSync.reload();
});

gulp.task('images', function(){
  gulp.src('src/images/**/*')
    .pipe(cache(imagemin({ optimizationLevel: 3, progressive: true, interlaced: true })))
    .pipe(gulp.dest('dist/images/'));
});

//gulp.task('styles', () => {
//    return gulp.src('app/styles/*.scss')
//        .pipe($.plumber())
//        .pipe($.sourcemaps.init())
//        .pipe($.sass.sync({
//            outputStyle: 'expanded',
//            precision: 10,
//            includePaths: ['.']
//        }).on('error', $.sass.logError))
//        .pipe($.autoprefixer({browsers: ['last 1 version']}))
//        .pipe($.sourcemaps.write())
//        .pipe(gulp.dest('.tmp/styles'))
//        .pipe(reload({stream: true}));
//});


gulp.task('styles', () =>  {
  return gulp.src('app/sass/main.scss')
    .pipe($.plumber())
    .pipe($.sourcemaps.init())
    .pipe($.sass.sync({
      outputStyle: 'expanded',
      precision: 10,
      includePaths: ['bower_components']
    }).on('error', $.sass.logError))
    .pipe($.autoprefixer({browsers: ['last 1 version']}))
    .pipe(gulp.dest('dist/styles'))
    .pipe($.minifyCss())
    .pipe($.rename({suffix: '.min'}))
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest('dist/styles/'))
    .pipe(reload({stream: true}));
});

gulp.task('scripts', function(){
  return gulp.src(isProduction ? sourcesJS.all : sourcesJS.base)
    .pipe($.plumber({
      errorHandler: function (error) {
        console.log(error.message);
        this.emit('end');
    }}))
    .pipe($.jshint())
    .pipe($.jshint.reporter('default'))
    .pipe(concat(pkg.name + '.js'))
    .pipe(gulp.dest(basePaths.dist + 'scripts/'))
    .pipe($.rename({suffix: '.min'}))
    .pipe($.uglify())
    .pipe(gulp.dest(basePaths.dist + 'scripts/'))
    .pipe(browserSync.reload({stream:true}));
});

gulp.task('default', ['browser-sync'], function(){
  gulp.watch("sass/**/*.scss", ['styles']);
  gulp.watch("src/scripts/**/*.js", ['scripts']);
  gulp.watch("*.html", ['bs-reload']);
});
