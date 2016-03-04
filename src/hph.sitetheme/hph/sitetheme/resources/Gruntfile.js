module.exports = function (grunt) {
    'use strict';
    require('time-grunt')(grunt);
    require('jit-grunt')(grunt);
    var config = {
        app: 'app',
        dev: '_site',
        dist: 'dist',
        diazoPrefix: '/++theme++<%= pkg.name %>.sitetheme',
        modules: 'node_modules'
    };
    grunt.initConfig({
        config: config,
        pkg: grunt.file.readJSON('package.json'),
        banner: '/*!\n' + '* <%= pkg.name %> v<%= pkg.version %> by Ade25\n' + '* Copyright <%= pkg.author %>\n' + '* Licensed under <%= pkg.licenses %>.\n' + '*\n' + '* Designed and built by ade25\n' + '*/\n',
        jqueryCheck: 'if (typeof jQuery === "undefined") { throw new Error("We require jQuery") }\n\n',
        jshint: {
            options: { jshintrc: '<%= config.app %>/js/.jshintrc' },
            grunt: { src: 'Gruntfile.js' },
            src: { src: ['<%= config.app %>/js/*.js'] }
        },
        jscs: {
            options: { config: '<%= config.app %>/js/.jscsrc' },
            grunt: { src: '<%= jshint.grunt.src %>' },
            src: { src: '<%= jshint.src.src %>' }
        },
        concat: {
            options: {
                banner: '<%= banner %>',
                stripBanners: false
            },
            dist: {
                src: [
                  '<%= config.modules %>/jquery/dist/jquery.js',
                  '<%= config.modules %>/modernizr/modernizr.js',
                  '<%= config.modules %>/tether/dist/js/tether.min.js',
                  '<%= config.modules %>/bootstrap/dist/js/bootstrap.js',
                  '<%= config.modules %>/mailcheck/src/mailcheck.js',
                  '<%= config.modules %>/JVFloat/jvfloat.js',
                  '<%= config.modules %>/hideShowPassword/hideShowPassword.js',
                  '<%= config.modules %>/lazysizes/plugins/ls.parent-fit.js',
                  '<%= config.modules %>/lazysizes/plugins/ls.bgset.js',
                  '<%= config.modules %>/lazysizes/plugins/ls.unveilhooks.js',
                  '<%= config.modules %>/lazysizes/lazysizes.js',
                  '<%= config.modules %>/respimage/respimage.js',
                  '<%= config.app %>/scripts/main.js'
                ],
                dest: '<%= config.dist %>/scripts/<%= pkg.name %>.js'
            },
            theme: {
                options: {
                    banner: "require(['jquery'], function($) {'use strict';",
                    footer: "});",
                    stripBanners: true
                },
                src: [
                    '<%= config.modules %>/tether/dist/js/tether.min.js',
                    '<%= config.modules %>/bootstrap/dist/js/bootstrap.js',
                    '<%= config.modules %>/lazysizes/plugins/ls.parent-fit.js',
                    '<%= config.modules %>/lazysizes/plugins/ls.bgset.js',
                    '<%= config.modules %>/lazysizes/plugins/ls.unveilhooks.js',
                    '<%= config.modules %>/lazysizes/lazysizes.js',
                    '<%= config.modules %>/respimage/respimage.js',
                    '<%= config.app %>/scripts/main.js'
                ],
                dest: '<%= config.dist %>/scripts/main.js'
            }
        },
        uglify: {
            options: { banner: '<%= banner %>' },
            dist: {
                src: ['<%= concat.dist.dest %>'],
                dest: '<%= config.dist %>/scripts/<%= pkg.name %>.min.js'
            }
        },
        // Generates a custom Modernizr build that includes only the tests you
        // reference in your app
        modernizr: {
            dist: {
                devFile: '<%= config.modules %>/modernizr/modernizr.js',
                outputFile: '<%= config.dist %>/scripts/vendor/modernizr.js',
                files: {
                    src: [
                        '<%= config.dist %>/scripts/{,*/}*.js',
                        '<%= config.dist %>/stypes/{,*/}*.css',
                        '!<%= config.dist %>/scripts/vendor/*'
                    ]
                },
                uglify: true
            }
        },
        // Compiles Sass to CSS and generates necessary files if requested
        sass: {
            options: {
                sourceMap: true,
                includePaths: ['<%= config.modules %>'],
                loadPath: '<%= config.modules %>'
            },
            dist: {
                files: { '<%= config.dist %>/styles/<%= pkg.name %>.css': '<%= config.app %>/sass/main.scss' }
            },
            server: {
                files: { '<%= config.dist %>/styles/<%= pkg.name %>.css': '<%= config.app %>/sass/main.scss' }
            }
        },
        autoprefixer: {
            options: {
                browsers: ['last 2 versions']
            },
            core: {
                options: { map: true },
                src: '<%= config.dist %>/styles/<%= pkg.name %>.css'
            }
        },
        csslint: {
            options: { csslintrc: '<%= config.app %>/sass/.csslintrc' },
            src: '<%= config.dist %>/styles/<%= pkg.name %>.css'
        },
        cssmin: {
            options: {
                compatibility: 'ie8',
                keepSpecialComments: '*',
                advanced: false
            },
            core: { files: { '<%= config.dist %>/styles/<%= pkg.name %>.min.css': '<%= config.dist %>/styles/<%= pkg.name %>.css' } }
        },
        csscomb: {
            sort: {
                options: { config: '<%= config.app %>/sass/.csscomb.json' },
                files: { '<%= config.dist %>/styles/<%= pkg.name %>.css': ['<%= config.dist %>/styles/<%= pkg.name %>.css'] }
            }
        },
        criticalcss: {
            frontpage: {
                options: {
                    url: 'http://localhost:8499/<%= pkg.name %>',
                    width: 1200,
                    height: 900,
                    outputfile: '<%= config.app %>/assets/css/critical-lp.css',
                    filename: '<%= config.dist %>/css/<%= pkg.name %>.css'
                }
            },
            theme: {
                options: {
                    url: 'http://localhost:8499/rms/stellplatz-am-wassersportzentrum',
                    width: 1200,
                    height: 900,
                    outputfile: '<%= config.app %>/assets/styles/critical.css',
                    filename: '<%= config.dist %>/styles/<%= pkg.name %>.css'
                }
            }
        },
        copy: {
            ionicons: {
                expand: true,
                flatten: true,
                cwd: '<%= config.modules %>/',
                src: ['ionicons/fonts/*'],
                dest: '<%= config.dist %>/assets/fonts/'
            },
            showPassword: {
                expand: true,
                flatten: true,
                cwd: '<%= config.modules %>/',
                src: ['hideShowPassword/images/*'],
                dest: '<%= config.dist %>/assets/img/'
            },
            ico: {
                expand: true,
                flatten: true,
                cwd: '<%= config.modules %>/',
                src: ['bootstrap/assets/ico/*'],
                dest: '<%= config.dist %>/assets/ico/'
            },
            favicon: {
                expand: true,
                flatten: true,
                src: ['<%= config.app %>/assets/ico/*'],
                dest: '<%= config.dist %>/assets/ico/'
            }
        },
        imagemin: {
            dynamic: {
                options: {
                    optimizationLevel: 5,
                    svgoPlugins: [{ removeViewBox: false }]
                },
                files: [{
                    expand: true,
                    cwd: '<%= config.app %>/assets/img',
                    src: ['*.{png,jpg,gif}'],
                    dest: '<%= config.dist %>/assets/img/'
                }]
            }
        },
        svgmin: {
            dist: {
                files: [{
                    expand: true,
                    cwd: '<%= config.app %>/assets/img/',
                    src: '{,*/}*.svg',
                    dest: '<%= config.dist %>/assets/img/'
                }]
            }
        },
        filerev: {
            options: {
                encoding: 'utf8',
                algorithm: 'md5',
                length: 12
            },
            assets: {
                src: [
                    '<%= config.dist %>/scripts/<%= pkg.name %>.min.js',
                    '<%= config.dist %>/styles/<%= pkg.name %>.min.css'
                ]
            },
            files: {
                src: [
                    '<%= config.dist %>/assets/img/{,*/}*.{png,jpg,jpeg,gif,webp,svg}',
                    '<%= config.dist %>/assets/fonts/*'
                ]
            }
        },
        usemin: {
            html: ['<%= config.dist %>/{,*/}*.html'],
            htmlcustom: ['<%= config.dist %>/{,*/}*.html'],
            css: ['<%= config.dist %>/styles/*.css'],
            options: {
                assetsDirs: [
                    '<%= config.dist %>',
                    '<%= config.dist %>/styles',
                    '<%= config.dist %>/assets'
                ],
                patterns: {
                    htmlcustom: [
                        [
                            /(?:src=|url\(\s*)['"]?([^'"\)(\?|#)]+)['"]?\s*\)?/gm,
                            'Replacing src references in inline javascript'
                        ],
                        [
                            /(?:loadCSS\(|url\(\s*)['"]?([^'"\)(\?|#)]+)['"]?\s*\)?/gm,
                            'Update the load css source with the new img filenames'
                        ],
                        [
                            /(?:data-src=|url\(\s*)['"]?([^'"\)(\?|#)]+)['"]?\s*\)?/gm,
                            'Update the img data-src attributes with the new img filenames'
                        ]
                    ]
                }
            }
        },
        qunit: {
            options: { inject: 'js/tests/unit/phantom.js' },
            files: ['js/tests/*.html']
        },
        jekyll: {
            theme: { options: { config: '_config.yml' } },
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
                    conservativeCollapse: true,
                    removeEmptyAttributes: true,
                    removeOptionalTags: true,
                    removeRedundantAttributes: true,
                    useShortDoctype: true,
                    keepClosingSlash: true,
                    minifyCSS: true,
                    minifyJS: true
                },
                files: [{
                    expand: true,
                    cwd: '<%= config.dev %>',
                    src: [
                        '*.html',
                        '{,*/}*.html'
                    ],
                    dest: '<%= config.dist %>'
                }]
            }
        },
        replace: {
            server: {
                options: {
                    patterns: [
                        {
                            match: '../assets/',
                            replacement: 'assets/'
                        },
                        {
                            match: '../../assets/',
                            replacement: '../assets/'
                        },
                        {
                            match: '../../<%= config.dist %>/styles/<%= pkg.name %>.min.css',
                            replacement: '../styles/<%= pkg.name %>.min.css'
                        },
                        {
                            match: '../<%= config.dist %>/styles/<%= pkg.name %>.min.css',
                            replacement: 'styles/<%= pkg.name %>.min.css'
                        },
                        {
                            match: '../../<%= config.dist %>/scripts/<%= pkg.name %>.min.js',
                            replacement: '../scripts/<%= pkg.name %>.min.js'
                        },
                        {
                            match: '../<%= config.dist %>/scripts/<%= pkg.name %>.min.js',
                            replacement: 'scripts/<%= pkg.name %>.min.js'
                        }
                    ],
                    usePrefix: false,
                    preserveOrder: true
                },
                files: [{
                    expand: true,
                    cwd: '<%= config.dev %>',
                    src: [
                        '*.html',
                        '{,*/}*.html'
                    ],
                    dest: '<%= config.dev %>'
                }]
            },
            diazo: {
                options: {
                    patterns: [
                        {
                            match: '../assets/',
                            replacement: 'assets/'
                        },
                        {
                            match: 'assets/',
                            replacement: 'http://<%= connect.options.hostname %>:<%= connect.options.port %>/assets/'
                        },
                        {
                            match: '../styles/',
                            replacement: 'styles/'
                        },
                        {
                            match: 'styles/',
                            replacement: 'http://<%= connect.options.hostname %>:<%= connect.options.port %>/styles/'
                        },
                        {
                            match: '../scripts/<%= pkg.name %>',
                            replacement: 'scripts/<%= pkg.name %>'
                        },
                        {
                            match: 'scripts/<%= pkg.name %>',
                            replacement: 'http://<%= connect.options.hostname %>:<%= connect.options.port %>/scripts/<%= pkg.name %>'
                        }
                    ],
                    usePrefix: false,
                    preserveOrder: true
                },
                files: [{
                    expand: true,
                    cwd: '<%= config.dist %>',
                    src: [
                        '*.html',
                        '{,*/}*.html'
                    ],
                    dest: '<%= config.dist %>'
                }]
            },
            pat: {
                options: {
                    patterns: [
                        {
                            match: '../assets/',
                            replacement: 'assets/'
                        },
                        {
                            match: 'assets/',
                            replacement: '<%= config.diazoPrefix %>/<%= config.dist %>/assets/'
                        },
                        {
                            match: '../styles/',
                            replacement: 'styles/'
                        },
                        {
                            match: 'styles/',
                            replacement: '<%= config.diazoPrefix %>/<%= config.dist %>/styles/'
                        },
                        {
                            match: '../scripts/<%= pkg.name %>',
                            replacement: 'scripts/<%= pkg.name %>'
                        },
                        {
                            match: 'scripts/<%= pkg.name %>',
                            replacement: '<%= config.diazoPrefix %>/<%= config.dist %>/scripts/<%= pkg.name %>'
                        }
                    ],
                    usePrefix: false,
                    preserveOrder: true
                },
                files: [{
                    expand: true,
                    cwd: '<%= config.dist %>',
                    src: [
                        '*.html',
                        '{,*/}*.html'
                    ],
                    dest: '<%= config.dist %>'
                }]
            },
            dist: {
                options: {
                    patterns: [
                        {
                            match: '../assets/',
                            replacement: 'assets/'
                        },
                        {
                            match: 'assets/',
                            replacement: '/assets/'
                        },
                        {
                            match: '../styles/<%= pkg.name %>',
                            replacement: 'styles/<%= pkg.name %>'
                        },
                        {
                            match: 'styles/<%= pkg.name %>',
                            replacement: '/styles/<%= pkg.name %>'
                        },
                        {
                            match: '../scripts/<%= pkg.name %>',
                            replacement: 'scripts/<%= pkg.name %>'
                        },
                        {
                            match: 'scripts/<%= pkg.name %>',
                            replacement: '/scripts/<%= pkg.name %>'
                        }
                    ],
                    usePrefix: false,
                    preserveOrder: true
                },
                files: [{
                    expand: true,
                    cwd: '<%= config.dist %>',
                    src: [
                        '*.html',
                        '{,*/}*.html'
                    ],
                    dest: '<%= config.dist %>'
                }]
            }
        },
        clean: {
            dist: {
                files: [{
                    dot: true,
                    src: ['<%= config.dist %>']
                }]
            },
            revved: {
                files: [{
                    dot: true,
                    src: [
                        '<%= config.dist %>/scripts/*.min.*.js',
                        '<%= config.dist %>/styles/*.min.*.css'
                    ]
                }]
            },
            assets: {
                files: [{
                    dot: true,
                    src: ['<%= config.dist %>/assets/*']
                }]
            },
            server: {
                files: [{
                    dot: true,
                    src: [
                        '<%= config.dist %>/*',
                        '!<%= config.dist %>/assets'
                    ]
                }]
            }
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
            files: { src: ['<%= config.dev %>/**/*.html'] }
        },
        watch: {
            js: {
                files: ['<%= config.app %>/scripts/{,*/}*.js'],
                tasks: ['concat', 'uglify'],
                options: { livereload: true }
            },
            html: {
                files: ['<%= config.app %>/{,*/}*.html'],
                tasks: ['jekyll:theme', 'replace:server', 'htmlmin']
            },
            sass: {
                files: ['<%= config.app %>/sass/{,*/}*.{scss,sass}'],
                tasks: ['sass:server', 'autoprefixer', 'csscomb', 'cssmin'],
                options: { livereload: true }
            }
        },
        connect: {
            options: {
                port: 9499,
                hostname: 'localhost',
                livereload: 35729,
                base: '<%= config.dev %>'
            },
            livereload: {
                options: {
                    open: true,
                    base: [
                        '.tmp',
                        '<%= config.dist %>'
                    ]
                }
            },
            dist: {
                options: {
                    open: false,
                    base: '<%= config.dist %>'
                }
            }
        },
        concurrent: {
            server: [
                'sass:server',
                'concat'
            ],
            dev: [
                'less-compile',
                'autoprefixer',
                'csscomb',
                'cssmin',
                'concat',
                'uglify'
            ],
            dist: [
                'jekyll:theme',
                'uglify',
                'csscomb'
            ]
        },
        pagespeed: {
            options: {
                nokey: true
            },
            dist: {
                options: {
                    url: 'http://aha.kreativkombinat.de',
                    paths: ['/', '/licht', '/raum'],
                    locale: 'de_DE',
                    strategy: 'desktop',
                    threshold: 80
                }
            }
        }
    });
    grunt.registerTask('dist-init', '', function () {
        grunt.file.mkdir('<%= config.dist %>/assets/');
    });
    grunt.registerTask('serve', function (target) {
        if (target === 'diazo') {
            return grunt.task.run([
                'diazo',
                'connect:dist',
                'watch'
            ]);
        }
        grunt.task.run([
            'html',
            'js',
            'css',
            'replace:diazo',
            'connect:livereload',
            'watch'
        ]);
    });
    grunt.registerTask('validate-html', [
        'jekyll',
        'validation'
    ]);
    grunt.registerTask('test', [
        'css',
        'jshint',
        'validate-html'
    ]);
    grunt.registerTask('static-assets', [
        'newer:copy',
        'newer:imagemin'
    ]);
    grunt.registerTask('templates', [
        'jekyll:theme'
    ]);
    grunt.registerTask('html', [
        'templates',
        'replace:server',
        'htmlmin'
    ]);
    grunt.registerTask('js', [
        'concat',
        'uglify'
    ]);
    grunt.registerTask('less-compile', ['less:compileTheme']);
    grunt.registerTask('css', [
        'sass:dist',
        'autoprefixer',
        'csscomb',
        'cssmin'
    ]);
    grunt.registerTask('cb', [
        'clean:revved',
        'filerev:assets',
        'usemin'
    ]);
    grunt.registerTask('dev', [
        'html',
        'css',
        'js'
    ]);
    grunt.registerTask('diazo', [
        'html',
        'css',
        'replace:diazo'
    ]);
    grunt.registerTask('pat', [
        'html',
        'css',
        'replace:pat'
    ]);
    grunt.registerTask('dist', [
        'clean:server',
        'html',
        'css',
        'js',
        'cb',
        'replace:dist'
    ]);
    grunt.registerTask('build', [
        'clean:server',
        'css',
        'js',
        'html',
        'filerev:assets',
        'usemin'
    ]);
    grunt.registerTask('compile-theme', ['dist']);
    grunt.registerTask('default', ['dev']);
};
