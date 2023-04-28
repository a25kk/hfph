import gulp from 'gulp';
import pump from 'pump';
import gulpLoadPlugins from 'gulp-load-plugins';
const $ = gulpLoadPlugins();


// Build Base
const buildBase = gulp.series(
    'jekyll:build',
    gulp.parallel('styles:dist', 'collect:scripts:app'),
    'inject:head:styles'
);

buildBase.description = 'Compile templates and collect  production build';

gulp.task('build:base', buildBase);
