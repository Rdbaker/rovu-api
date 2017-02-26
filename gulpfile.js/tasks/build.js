var gulp = require('gulp');
var config = require('../config.js').browserify;
var browserify = require('browserify');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var gutil = require('gulp-util');
var vueify = require('vueify');


gulp.task('build', ['sass'], function() {
  var b = browserify({
    entries: config.src,
    debug: config.debug
  })
  .transform(vueify);

  if(config.debug) {
    return b.bundle()
      .pipe(source(config.destName))
      .pipe(buffer())
      .pipe(sourcemaps.init({loadMaps: true}))
      .on('error', gutil.log)
      .pipe(sourcemaps.write(config.src))
      .pipe(gulp.dest(config.dest));
  } else {
    return b.bundle()
          .pipe(source(config.destName))
          .pipe(buffer())
          .pipe(sourcemaps.init({loadMaps: false}))
          .pipe(uglify())
          .on('error', gutil.log)
          .pipe(sourcemaps.write(config.src))
          .pipe(gulp.dest(config.dest));
  }
});
