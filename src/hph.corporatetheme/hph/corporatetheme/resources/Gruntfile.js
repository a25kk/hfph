/* jshint node: true */

module.exports = function (grunt) {

  'use strict';

  // load all grunt tasks
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  require('time-grunt')(grunt);

  // Configurable paths
  var appconfig = {
    app: 'app',
    dev: '_site',
    dist: 'dist'
  };

  // Project configuration.
  grunt.initConfig({

    // Project settings
    appconfig: appconfig,

    // Metadata.
    pkg: grunt.file.readJSON('package.json'),
    banner: '/*!\n' +
              '* <%= pkg.name %> v<%= pkg.version %> by Ade25\n' +
              '* Copyright <%= pkg.author %>\n' +
              '* Licensed under <%= pkg.licenses %>.\n' +
              '*\n' +
              '* Designed and built by ade25\n' +
              '*/\n',
    jqueryCheck: 'if (typeof jQuery === "undefined") { throw new Error(\"We require jQuery\") }\n\n',

      // Task configuration.
    clean: {
      dist: ['<%= appconfig.dist %>']
    },

    jshint: {
      options: {
        jshintrc: 'js/.jshintrc'
      },
      grunt: {
        src: 'Gruntfile.js'
      },
      src: {
        src: ['js/*.js']
      }
    },

    jscs: {
      options: {
        config: 'js/.jscsrc'
      },
      grunt: {
        src: '<%= jshint.grunt.src %>'
      },
      src: {
        src: '<%= jshint.src.src %>'
      }
    },

    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: false
      },
      dist: {
        src: [
          'bower_components/jquery/dist//jquery.js',
          'bower_components/modernizr/modernizr.js',
          'bower_components/bootstrap/dist/js/bootstrap.js',
          'bower_components/JQuery.Marquee/jquery.marquee.js',
          'bower_components/datatables/media/js/jquery.dataTables.js',
          'bower_components/headroom.js/dist/headroom.js',
          'bower_components/headroom.js/dist/jQuery.headroom.js',
          'js/application.js'
        ],
        dest: '<%= appconfig.dist %>/js/<%= pkg.name %>.js'
      },
      theme: {
        src: [
          'bower_components/bootstrap/dist/js/bootstrap.js',
          'bower_components/JQuery.Marquee/jquery.marquee.js',
          'bower_components/datatables/media/js/jquery.dataTables.js',
          'bower_components/headroom.js/dist/headroom.js',
          'bower_components/headroom.js/dist/jQuery.headroom.js',
          'js/application.js'
        ],
        dest: '<%= appconfig.dist %>/js/main.js'
      }
    },

    uglify: {
      options: {
        banner: '<%= banner %>'
      },
      dist: {
        src: ['<%= concat.dist.dest %>'],
        dest: '<%= appconfig.dist %>/js/<%= pkg.name %>.min.js'
      }
    },

    less: {
      compileTheme: {
        options: {
          strictMath: false,
          sourceMap: true,
          outputSourceFiles: true,
          sourceMapURL: '<%= pkg.name %>.css.map',
          sourceMapFilename: '<%= appconfig.dist %>/css/<%= pkg.name %>.css.map'
        },
        files: {
          '<%= appconfig.dist %>/css/<%= pkg.name %>.css': 'less/styles.less'
        }
      }
    },

    autoprefixer: {
      options: {
        browsers: [
          'Android 2.3',
          'Android >= 4',
          'Chrome >= 20',
          'Firefox >= 24', // Firefox 24 is the latest ESR
          'Explorer >= 8',
          'iOS >= 6',
          'Opera >= 12',
          'Safari >= 6'
        ]
      },
      core: {
        options: {
          map: true
        },
        src: '<%= appconfig.dist %>/css/<%= pkg.name %>.css'
      }
    },

    csslint: {
      options: {
        csslintrc: 'less/.csslintrc'
      },
      src: '<%= appconfig.dist %>/css/<%= pkg.name %>.css'
    },

    cssmin: {
      options: {
        compatibility: 'ie8',
        keepSpecialComments: '*',
        noAdvanced: true
      },
      core: {
        files: {
          '<%= appconfig.dist %>/css/<%= pkg.name %>.min.css': 'dist/css/<%= pkg.name %>.css'
        }
      }
    },

    csscomb: {
      sort: {
        options: {
          config: 'less/.csscomb.json'
        },
        files: {
          '<%= appconfig.dist %>/css/<%= pkg.name %>.css': ['dist/css/<%= pkg.name %>.css']
        }
      }
    },

    criticalcss: {
        frontpage: {
            options: {
                url: 'localhost:8499',
                width: 1200,
                height: 900,
                outputfile: '<%= appconfig.dist %>/css/critical.css',
                filename: '<%= pkg.name %>.min.css'
            }
        }
    },

    copy: {
      fontawesome: {
        expand: true,
        flatten: true,
        cwd: 'bower_components/',
        src: ['font-awesome/fonts/*'],
        dest: '<%= appconfig.dist %>/assets/fonts/'
      },
      //fonts: {
      //  expand: true,
      //  flatten: true,
      //  src: ['assets/font/*'],
      //  dest: '<%= appconfig.dist %>/assets/fonts/'
      //},
      //css: {
      //  expand: true,
      //  flatten: true,
      //  src: ['assets/css/*'],
      //  dest: '<%= appconfig.dist %>/assets/css/'
      //},
      images: {
        expand: true,
        flatten: true,
        src: ['assets/img/*'],
        dest: '<%= appconfig.dev %>/assets/img/'
      },
      ico: {
        expand: true,
        flatten: true,
        src: ['assets/ico/*'],
        dest: '<%= appconfig.dev %>/assets/ico/'
      }
    },

    imagemin: {
      dynamic: {
        files: [{
          expand: true,
          cwd: 'assets/img/',
          src: ['**/*.{png,jpg,gif}'],
          dest: '<%= appconfig.dist %>/assets/img/'
        }]
      }
    },

    filerev: {
      options: {
        encoding: 'utf8',
        algorithm: 'md5',
        length: 8
      },
      assets: {
          src: [
            '<%= appconfig.dist %>/js/{,*/}*.js',
            '<%= appconfig.dist %>/css/{,*/}*.css'
          ],
          dest: '<%= appconfig.dist %>/assets'
      },
      files: {
          src: [
            '<%= appconfig.dist %>/assets/img/{,*/}*.{png,jpg,jpeg,gif,webp,svg}',
            '<%= appconfig.dist %>/assets/fonts/*'
          ]
      }
    },

    filerev_replace: {
      options: {
        assets_root: '<%= appconfig.dist %>'
      },
      views: {
        src: '<%= appconfig.dist %>/**/*.html'
      }
    },

    qunit: {
      options: {
        inject: 'js/tests/unit/phantom.js'
      },
      files: ['js/tests/*.html']
    },

    jekyll: {
      theme: {
        options: {
          config: '_config.yml',
        }
      },
      server: {
        options: {
          serve: true,
          server_port: 8000,
          auto: true
        }
      }
    },

    htmlmin: {
      dist: {
        options: {
          removeComments: true,
          collapseWhitespace: true,
          removeOptionalTags: true
        },
        files: [{
          expand: true,
          cwd: '<%= appconfig.dev %>',
          src: ['*.html', '{,*/}*.html'],
          dest: '<%= appconfig.dist %>'
        }]
        //files: {
        //  '<%= appconfig.dist %>/index.html': '_site/index.html',
        //  '<%= appconfig.dist %>/theme.html': '_site/theme/index.html',
        //  '<%= appconfig.dist %>/signin.html': '_site/signin/index.html',
        //  '<%= appconfig.dist %>/signup.html': '_site/signup/index.html',
        //}
      },
    },

    sed: {
      cleanAssetsPath: {
        path: '<%= appconfig.dist %>/',
        pattern: '../../assets/',
        replacement: '../assets/',
        recursive: true
      },
      cleanCSS: {
        path: '<%= appconfig.dist %>/',
        pattern: '../../<%= appconfig.dist %>/css/<%= pkg.name %>.css',
        replacement: '<%= appconfig.dist %>/css/<%= pkg.name %>.min.css',
        recursive: true
      },
      cleanCSSFrontpage: {
        path: '<%= appconfig.dist %>/',
        pattern: '../<%= appconfig.dist %>/css/<%= pkg.name %>.css',
        replacement: '<%= appconfig.dist %>/css/<%= pkg.name %>.min.css',
        recursive: true
      },
      cleanJSFrontpage: {
        path: '<%= appconfig.dist %>/',
        pattern: '../<%= appconfig.dist %>/js/<%= pkg.name %>.min.js',
        replacement: 'dist/js/<%= pkg.name %>.min.js',
        recursive: true
      },
      cleanJS: {
        path: '<%= appconfig.dist %>/',
        pattern: '../../<%= appconfig.dist %>/js/<%= pkg.name %>.min.js',
        replacement: 'dist/js/<%= pkg.name %>.min.js',
        recursive: true
      },
      cleanImgPath: {
        path: '<%= appconfig.dist %>',
        pattern: '../assets/img/',
        replacement: 'assets/img/',
        recursive: true
      },
    },

    validation: {
      options: {
        charset: 'utf-8',
        doctype: 'HTML5',
        failHard: true,
        reset: true,
        relaxerror: [
          'Bad value X-UA-Compatible for attribute http-equiv on element meta.',
          'Element img is missing required attribute src.'
        ]
      },
      files: {
        src: ['<%= appconfig.dev %>/**/*.html']
      }
    },

    // Watches files for changes and runs tasks based on the changed files
    watch: {
      js: {
        files: ['js/{,*/}*.js'],
        tasks: ['newer:jshint:all'],
        options: {
          livereload: true
        }
      },
      styles: {
        files: ['<%= appconfig.dev %>/styles/{,*/}*.css'],
        tasks: ['newer:copy:styles', 'autoprefixer']
      },
      less: {
        files: 'less/*.less',
        tasks: ['less'],
        options: {
          spawn: false
        }
      },
      gruntfile: {
        files: ['Gruntfile.js']
      },
      livereload: {
        options: {
          livereload: '<%= connect.options.livereload %>'
        },
        files: [
          '<%= appconfig.dev %>/{,*/}*.html',
          '<%= appconfig.dist %>/css/{,*/}*.css'
        ]
      }
    },
    // The actual grunt server settings
    connect: {
      options: {
        port: 9000,
        // Change this to '0.0.0.0' to access the server from outside.
        hostname: 'localhost',
        livereload: 35729,
        base: '<%= appconfig.dev %>'
      },
      livereload: {
        options: {
          open: true,
          base: [
            '.tmp',
            '<%= appconfig.dist %>'
          ]
        }
      },
      dist: {
        options: {
          base: '<%= appconfig.dist %>'
        }
      }
    },

    concurrent: {
      cj: ['less', 'copy', 'concat', 'uglify'],
      ha: ['jekyll:theme', 'copy-templates', 'sed'],
      dev: ['less:compileTheme', 'jekyll:theme', 'concat:dist']
    }

  });


  // -------------------------------------------------
  // These are the available tasks provided
  // Run them in the Terminal like e.g. grunt dist-css
  // -------------------------------------------------

  // Prepare distrubution
  grunt.registerTask('dist-init', '', function () {
    grunt.file.mkdir('<%= appconfig.dist %>/assets/');
  });

  grunt.registerTask('serve', function (target) {
    if (target === 'dist') {
      return grunt.task.run(['build', 'connect:dist:keepalive']);
    }

    grunt.task.run([
      //'clean:server',
      //'bower-install',
      //'concurrent:server',
      'autoprefixer',
      'connect:livereload',
      'watch'
    ]);
  });

  // Docs HTML validation task
  grunt.registerTask('validate-html', ['jekyll', 'validation']);

  // Javascript Unittests
  grunt.registerTask('unit-test', ['qunit']);

  // Test task.
  var testSubtasks = ['dist-css', 'jshint', 'validate-html'];

  grunt.registerTask('test', testSubtasks);

  // JS distribution task.
  grunt.registerTask('dist-js', ['concat', 'uglify']);

  // CSS distribution task.
  grunt.registerTask('less-compile', ['less:compileTheme']);
  grunt.registerTask('dist-css', ['less-compile', 'autoprefixer', 'csscomb', 'cssmin']);

  // Assets distribution task.
  grunt.registerTask('dist-assets', ['newer:copy', 'newer:imagemin']);

  // Cache buster distribution task.
  grunt.registerTask('dist-cb', ['filerev', 'filerev_replace']);

  // Template distribution task.
  grunt.registerTask('dist-html', ['jekyll:theme', 'htmlmin', 'sed']);

  // Concurrent distribution task
  grunt.registerTask('dist-cc', ['test', 'concurrent:cj', 'concurrent:ha']);

  // Development task.
  grunt.registerTask('dev', [
    'jekyll:theme',
    'less:compileTheme',
    'concat:dist'
  ]);

  // Full distribution task.
  grunt.registerTask('dist', [
    'clean',
    'dist-css',
    'dist-js',
    'dist-html',
    'dist-assets'
  ]);

  // Shim theme compilation alias
  grunt.registerTask('compile-theme', ['dist']);

  // Default task.
  grunt.registerTask('default', ['dev']);

};