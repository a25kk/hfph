import gulp from 'gulp';
import {create as bsCreate} from 'browser-sync';

const browserSync = bsCreate();

var cfg = require('./../config.json');
var cp = require('child_process');

// Jekyll tasks

var messages = {
    jekyllBuild: '<span style="color: grey">Running:</span> $ jekyll build'
};

/**
 * Build the Jekyll Site
 */
gulp.task('jekyll:build', function (done) {
    browserSync.notify(messages.jekyllBuild);
    return cp.spawn('jekyll', ['build', '--quiet'], {stdio: 'inherit', shell: true, cwd: cfg.paths.base})
        .on('close', done);
});

// Build Jekyll without production settings
gulp.task('jekyll:dev', done => {
    shell.exec('jekyll build --quiet');
done();
});

// Build Jekyll with production settings
gulp.task('jekyll:prod', done => {
   return cp.spawn('jekyll', ['build', '--config _config.yml'], {stdio: 'inherit', shell: true, cwd: '../'});
    done();
});

// Check Jekyll for configuration errors
gulp.task('jekyll:doctor', done => {
    return cp.spawn('jekyll', ['doctor'], {stdio: 'inherit', shell: true, cwd: '../'});
    done();
});
