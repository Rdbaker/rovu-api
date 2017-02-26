var env = (process.env.ENV || 'local').toLowerCase();

var src = './rovu/static/src/';
var dest = './rovu/static/dest/';

module.exports = {
  env: {
    name: env
  },
  src: src,
  dest: dest,


  browserify: {
    src: src + 'js/app.js',
    dest: dest + 'js/',
    debug: (env !== 'production'),
    destName: 'app.js'
  },


  sass: {
    src: src + 'sass/app.sass',
    dest: dest + 'css',
    settings: {
      includePaths: [
        src + 'sass/',
        './node_modules',
        './node_modules/bootstrap-sass/assets/stylesheets'
      ]
    }
  },
};
