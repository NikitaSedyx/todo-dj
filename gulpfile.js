var gulp = require("gulp")
var jade = require("gulp-jade")
var concat = require("gulp-concat")
var csso = require("gulp-csso")
var rename = require("gulp-rename")
var uglify = require("gulp-uglify")
var jshint = require("gulp-jshint")
var karma = require('gulp-karma')
var sass = require('gulp-sass')
var gulpIgnore = require('gulp-ignore')
var clean = require('gulp-clean')

gulp.task("test", function(){
  var testFiles = [
    "./assets/libs/jquery/dist/jquery.min.js",
    "./assets/libs/masonry/dist/masonry.pkgd.js",
    "./assets/libs/angular/angular.js",
    "./assets/libs/angular-mocks/angular-mocks.js",
    "./assets/libs/angular-resource/angular-resource.min.js",
    "./assets/libs/angular-ui-router/release/angular-ui-router.min.js",
    "./assets/libs/angular-bootstrap/ui-bootstrap.min.js",
    "./assets/libs/angular-elastic/elastic.js",
    "./assets/libs/ngInfiniteScroll/build/ng-infinite-scroll.min.js",
    "./assets/libs/underscore/underscore-min.js",
    "./app/**/*.module.js",
    "./app/**/*.js",
    "./test/mocks/**/*.js",
    "./test/**/*.js"
  ]
  
  gulp.src(testFiles)
  .pipe(karma({
    configFile: "karma.conf.js",
    action: "watch"
  }))
})

gulp.task("lint", function(){
  gulp.src("./app/**/*.js")
    .pipe(jshint())
    .pipe(jshint.reporter("default"));
});

gulp.task("concat-js", ["lint"], function(){
  gulp.src(["./app/**/*.module.js", "./app/**/*.js"]) 
    .pipe(concat("index.js"))
    .pipe(gulp.dest("./build/app"))
    .pipe(rename("index.min.js"))
    .pipe(uglify())
    .pipe(gulp.dest("./build/app")) 
})

gulp.task("compile-index-jade", function(){
  gulp.src("./index.jade")
    .pipe(jade({
      pretty:true
    }))
    .on("error", console.log)
    .pipe(gulp.dest("./build"))
})

gulp.task("compile-views-jade", function(){
  gulp.src("./app/**/*.jade")
  .pipe(jade({
    pretty:true
  }))
  .on("error", console.log)
  .pipe(gulp.dest("./build/app/views"))
})

gulp.task("compile-sass", function(){
  gulp.src("./assets/sass/**/*.sass")
    .pipe(sass().on("error", sass.logError))
    .pipe(concat("index.css"))
    .pipe(gulp.dest("./build/assets/css"))
    .pipe(rename("index.min.css"))
    .pipe(csso())
    .pipe(gulp.dest("./build/assets/css"))
})

gulp.task("copy-libs", function(){
  gulp.src("./assets/libs/**/*")
    .pipe(gulp.dest("./build/assets/libs"))
})

gulp.task("watch", function(){
  gulp.watch("./app/**/*.jade", function(){
    gulp.run("compile-views-jade")
  })

  gulp.watch("./index.jade", function(){
    gulp.run("compile-index-jade")
  })

  gulp.watch("./assets/sass/**/*.sass", function(){
    gulp.run("compile-sass")
  })

  gulp.watch("./app/**/*.js", function(){
    gulp.run("concat-js")
  })
})

gulp.task("default", ["test", "lint", "concat-js", "compile-views-jade", 
  "compile-index-jade", "compile-sass", "copy-libs", "watch"])
