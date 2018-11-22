import gulp from 'gulp';
import del from 'del';

var cfg = require('./../config.json');


export const cleanBase = () => del(
    [cfg.paths.base + cfg.paths.dev],
    {force: true}
);

export const cleanAssets = () => del(
    ['.tmp', cfg.paths.base + cfg.paths.dist + 'assets'],
    {force: true}
);

export const cleanDist = () => del(
    [cfg.paths.base + cfg.paths.dist],
    {force: true}
);


// Cleaning tasks
gulp.task('clean:base', cleanBase);
gulp.task('clean:assets', cleanAssets);
gulp.task('clean:dist', cleanDist);

