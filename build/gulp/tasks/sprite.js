import gulp from 'gulp';
import pump from 'pump';
import gulpLoadPlugins from 'gulp-load-plugins';
const $ = gulpLoadPlugins();

var cfg = require('./../config.json');


export function spriteBuild(cb) {
    pump([
            gulp.src(cfg.paths.app + 'assets/svg/**/*.svg'),
            $.svgSprite(cfg.sprite),
            gulp.dest(cfg.paths.dist + 'assets/')
        ],
        cb
    );
};

spriteBuild.description = 'Collect svg files and concat to sprite';

gulp.task('sprite:collect', spriteBuild);
