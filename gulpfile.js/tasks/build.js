var gulp = require('gulp');
var config = require('../config.js').browserify;
var browserify = require('browserify');
var source = require('vinyl-source-stream');
var vueify = require('vueify');
var babelify = require('babelify');
var notify = require("gulp-notify");

function handleErrors() {
  var args = Array.prototype.slice.call(arguments);

  // Send error to notification center with gulp-notify
  notify.onError({
    title: "Compile Error",
    message: "<%= error %>"
  }).apply(this, args);

  // Keep gulp from hanging on this task
  this.emit('end');
}


gulp.task('build', ['sass'], function() {
  return browserify({
    entries: config.src,
    debug: config.debug
  })
  .transform(vueify)
  .transform(babelify)
  .bundle()
  .on('error', handleErrors)
  .pipe(source(config.destName))
  .pipe(gulp.dest(config.dest))
});
