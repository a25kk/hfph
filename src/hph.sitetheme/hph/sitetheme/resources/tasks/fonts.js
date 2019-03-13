import gulp from 'gulp';
import pump from 'pump';
import {getter as wfGetter} from 'gulp-google-webfonts';
import gulpLoadPlugins from 'gulp-load-plugins';
var googleWebFonts = require('gulp-google-webfonts');
const $ = gulpLoadPlugins();

// const fontDownload = wfGetter();

var cfg = require('./../config.json');

var font_downloader_options = {
    fontsDir: './assets/fonts',
    cssDir: './sass/generic/',
    cssFilename: '_generic.fonts.custom.scss'
};

export function downloadWebFonts(cb) {
    pump([
            gulp.src('web_fonts.list'),
            googleWebFonts(font_downloader_options),
            gulp.dest(cfg.paths.app)
        ],
        cb
    );
};

downloadWebFonts.description = 'Download web fonts to project';

gulp.task('fonts:download', downloadWebFonts);
