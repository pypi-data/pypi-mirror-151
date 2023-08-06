console.log("A112");
'use strict';

angular.module('codenerixVendingsControllers', [])
//.controller('codenerixVendingsCtrl', ['$scope', '$state', '$stateParams', '$timeout', '$uibModal', '$http', 'Register', '$rootScope', '$location', 'ListMemory', '$window', '$templateCache', 'hotkeys', '$uibModalInstance',
//    function($scope, $state, $stateParams, $timeout, $uibModal, $http, Register, $rootScope, $location, ListMemory, $window, $templateCache, hotkeys, $uibModalInstance) {

.controller('codenerixVendingsCtrl', 
    ['$scope', '$rootScope', '$timeout', '$location', '$uibModal', '$templateCache', '$http', '$state', 'Register', 'ListMemory', 'hotkeys',
    function($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory, hotkeys) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
//        multilist($scope, $rootScope, $timeout, $location, $uibModal, $templateCache, $http, $state, Register, ListMemory, 0, "/"+ws_entry_point, undefined, undefined, hotkeys);

        $scope.wsbase = "/" + ws_entry_point;

        $scope.sale_registered_users = function () {
            $scope.ws = $scope.wsbase + "/sale_registered_users";
            var functions = function(scope) { };
            var callback = function(scope, answer) {
                if ('__pk__' in answer){
                    $location.path(url_budget).hash(answer['__pk__']);
                    window.location.href = $location.url();
                }else{
                    alert(answer);
                    console.log(answer);
                }
            };
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
        };

        $scope.sale_employees_users = function () {
            $scope.ws = $scope.wsbase + "/sale_employees_users";
            var functions = function(scope) { };
            var callback = function(scope, answer) {
                if ('__pk__' in answer){
                    $location.path(url_budget).hash(answer['__pk__']);
                    window.location.href = $location.url();
                }else{
                    alert(answer);
                    console.log(answer);
                }
            };
            openmodal($scope, $timeout, $uibModal, 'lg', functions, callback);
        };

        $scope.sale_default_user = function(){
            var url = $scope.wsbase + '/sale_default_users';
            function successCallback(response){
                var answer = response['data'];
                if ('__pk__'  in answer){
                    // $location.path(url_budget).hash(answer['__pk__']);
                    url_budget_tmp = url_budget.replace('CNDX_VENDING_LINES', answer['__pk__']);
                    // $location.path(url_budget + "/" + answer['__pk__']);
                    $location.path(url_budget_tmp);
                    window.location.href = $location.url();
                }else{
                    alert(answer['error']);
                    console.log(response);
                }
            }
            function errorCallback(response){
                if (cnf_debug){
                    alert(response['statusText'] + ": " + response['config']['url']);
                }else{
                    alert(response['statusText']);
                }
            }
            $http.post(url, {}).then(successCallback, errorCallback);
        };
    }
]);