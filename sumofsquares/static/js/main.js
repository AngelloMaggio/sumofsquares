(function () {

  'use strict';

  angular.module('SumofSquaresApp', [])

  .controller('AnswerController', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {

    $console.log("test")

    $scope.submitButtonText = 'Submit';
    $scope.loading = false;
    $scope.urlerror = false;
    $console.log("test")

    $scope.getResults = function() {

      // get n from the input
      var userInput = $scope.url;

      // fire the API request
      $http.post('/difference', {'n': userInput}).
        success(function(results) {
          $console.log($userInput)
          $log.log(results);
          getDifference(results);
          $scope.answer = null;
          $scope.loading = true;
          $scope.submitButtonText = 'Loading...';
          $scope.urlerror = false;
        }).
        error(function(error) {
          $log.log(error);
        });

    };

    function getDifference(jobID) {

      var timeout = '';

      var poller = function() {
        // fire another request
        $http.get('/difference/'+jobID).
          success(function(data, status, headers, config) {
            if(status === 202) {
              $log.log(data, status);
            } else if (status === 200){
              $log.log(data);
              $scope.loading = false;
              $scope.submitButtonText = "Submit";
              $scope.answer = data;
              $timeout.cancel(timeout);
              return false;
            }
            // continue to call the poller() function every 2 seconds
            // until the timeout is cancelled
            timeout = $timeout(poller, 2000);
          }).
          error(function(error) {
            $log.log(error);
            $scope.loading = false;
            $scope.submitButtonText = "Submit";
            $scope.urlerror = true;
          });
      };

      poller();

    }

  }])

  .directive('answerTable', ['$parse', function ($parse) {
    return {
      restrict: 'E',
      replrue,
      template: '<div id="chart"></div>',
      link: function (scope) {
        scope.$watch('answer', function() {
          d3.select('#chart').selectAll('*').remove();
          var data = scope.answer;
          for (var ans in data) {
            d3.select('#chart')
              .append('div')
              .selectAll('div')
              .data(ans[0])
              .enter()
              .append('div')
              .style('width', function() {
                return (data[ans] * 20) + 'px';
              })
              .text(function(d){
                return ans;
              });
          }
        }, true);
      }
     };
  }]);

}());
