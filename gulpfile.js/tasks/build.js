var gulp = require('gulp');
var config = require('../config.js').browserify;
var browserify = require('browserify');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var gutil = require('gulp-util');


gulp.task('build', ['sass'], function() {
  var b = browserify({
    entries: config.src,
    debug: config.debug
  });
  b.transform("babelify", {presets: ["es2015", "react"]})

  return b.bundle()
    .pipe(source(config.destName))
    .pipe(buffer())
    .pipe(sourcemaps.init({loadMaps: config.debug}))
    .on('error', gutil.log)
    .pipe(sourcemaps.write(config.src))
    .pipe(gulp.dest(config.dest));
});
