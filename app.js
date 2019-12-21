var mouseclicksysApp = angular.module('mouseclicksysApp', ['ngRoute','smart-table','ui.multiselect','datatables','moment-picker','angular.filter']);

mouseclicksysApp.directive('fileModel', ['$parse', function($parse) {
 return {
  restrict: 'A',
  link: function(scope, element, attrs) {
   var model = $parse(attrs.fileModel);
   var modelSetter = model.assign;

   element.bind('change', function() {
    scope.$apply(function() {
      console.log(attrs.fileModel);

     modelSetter(scope, element[0].files[0]);
     /*if (attrs.fileModel == "amcExcelFile") {
      scope.uploadAmcExcel();    
     }*/
    });
   });
  }
 };
}]);

mouseclicksysApp.directive('stSelectDistinct', [function() {
      return {
        restrict: 'E',
        require: '^stTable',
        scope: {
          collection: '=',
          predicate: '@',
          predicateExpression: '='
        },
        template: '<select ng-model="selectedOption" ng-change="optionChanged(selectedOption)" ng-options="opt for opt in distinctItems"></select>',
        link: function(scope, element, attr, table) {
          var getPredicate = function() {
            var predicate = scope.predicate;
            if (!predicate && scope.predicateExpression) {
              predicate = scope.predicateExpression;
            }
            return predicate;
          }

          scope.$watch('collection', function(newValue) {
            var predicate = getPredicate();

            if (newValue) {
              var temp = [];
              scope.distinctItems = ['All'];

              angular.forEach(scope.collection, function(item) {

                var value = item[predicate].toString();                

                if (value && value.trim().length > 0 && temp.indexOf(value) === -1) {
                  temp.push(value.toString());
                }
              });
              temp.sort();

              scope.distinctItems = scope.distinctItems.concat(temp);
              scope.selectedOption = scope.distinctItems[0];
              scope.optionChanged(scope.selectedOption);
            }
          }, true);

          scope.optionChanged = function(selectedOption) {
            var predicate = getPredicate();

            var query = {};

            query.distinct = selectedOption;

            if (query.distinct === 'All') {
              query.distinct = '';
            }

            table.search(query, predicate);
          };
        }
      }
    }]);
    



mouseclicksysApp.filter('unique', function() {
    return function (arr, field) {
        console.log(field);
        var o = {}, i, l = arr.length, r = [];
        for(i=0; i<l;i+=1) {
            o[arr[i][field]] = arr[i];
        }
        for(i in o) {
            r.push(o[i]);
        }

/*        console.log(r);
*/        return r;
    };
  });


mouseclicksysApp.filter('customFilter', ['$filter', function($filter) {
      var filterFilter = $filter('filter');
      var standardComparator = function standardComparator(obj, text) {
        text = ('' + text).toLowerCase();
        return ('' + obj).toLowerCase().indexOf(text) > -1;
      };

      return function customFilter(array, expression) {
        function customComparator(actual, expected) {

          var isBeforeActivated = expected.before;
          var isAfterActivated = expected.after;
          var isLower = expected.lower;
          var isHigher = expected.higher;
          var higherLimit;
          var lowerLimit;
          var itemDate;
          var queryDate;

          if (angular.isObject(expected)) {
            //exact match
            if (expected.distinct) {
              if (!actual || actual.toLowerCase() !== expected.distinct.toLowerCase()) {
                return false;
              }

              return true;
            }

            //matchAny
            if (expected.matchAny) {
              if (expected.matchAny.all) {
                return true;
              }

              if (!actual) {
                return false;
              }

              for (var i = 0; i < expected.matchAny.items.length; i++) {
                if (actual.toLowerCase() === expected.matchAny.items[i].toLowerCase()) {
                  return true;
                }
              }

              return false;
            }

            //date range
            if (expected.before || expected.after) {
              try {
                if (isBeforeActivated) {
                  higherLimit = expected.before;

                  itemDate = new Date(actual);
                  queryDate = new Date(higherLimit);

                  if (itemDate > queryDate) {
                    return false;
                  }
                }

                if (isAfterActivated) {
                  lowerLimit = expected.after;


                  itemDate = new Date(actual);
                  queryDate = new Date(lowerLimit);

                  if (itemDate < queryDate) {
                    return false;
                  }
                }

                return true;
              } catch (e) {
                return false;
              }

            } else if (isLower || isHigher) {
              //number range
              if (isLower) {
                higherLimit = expected.lower;

                if (actual > higherLimit) {
                  return false;
                }
              }

              if (isHigher) {
                lowerLimit = expected.higher;
                if (actual < lowerLimit) {
                  return false;
                }
              }

              return true;
            }
            //etc

            return true;

          }
          return standardComparator(actual, expected);
        }

        var output = filterFilter(array, expression, customComparator);
        return output;
      };
    }]);

mouseclicksysApp.filter('titlecase', function() {
     return function(input) {
      var smallWords = /^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/i;

      input = input.toLowerCase();
      return input.replace(/[A-Za-z0-9\u00C0-\u00FF]+[^\s-]*/g, function(match, index, title) {
       if (index > 0 && index + match.length !== title.length &&
        match.search(smallWords) > -1 && title.charAt(index - 2) !== ":" &&
        (title.charAt(index + match.length) !== '-' || title.charAt(index - 1) === '-') &&
        title.charAt(index - 1).search(/[^\s-]/) < 0) {
        return match.toLowerCase();
       }

       if (match.substr(1).search(/[A-Z]|\../) > -1) {
        return match;
       }

       return match.charAt(0).toUpperCase() + match.substr(1);
      });
     }
    });

    mouseclicksysApp.config(function($sceProvider) {
        $sceProvider.enabled(false);
    });

mouseclicksysApp.config(function($sceProvider) {
    $sceProvider.enabled(false);
});

mouseclicksysApp.config(function($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl : 'login.html',
        controller : 'homeController'
    })
    .when('/home', {
        templateUrl : 'views/home.html',
        controller : 'homeController'
    })
    .when('/viewAmc', {
        templateUrl : 'views/admin/viewAmc.html',
        controller : 'homeController'
    })
    .when('/viewClients', {
        templateUrl : 'views/admin/viewClients.html',
        controller : 'homeController'
    })
    .when('/viewFamilies', {
      templateUrl : 'views/admin/viewFamily.html',
      controller : 'homeController'
    })
    // .when('/viewDaywise', {
    //     templateUrl : 'views/admin/viewDaywise.html',
    //     controller : 'homeController'
    // })
    .when('/newviewDaywise', {
        templateUrl : 'views/admin/newviewDaywise.html',
        controller : 'homeController'
    })
    // .when('/listDaywise', {
    //     templateUrl : 'views/admin/listdaywisefilter.html',
    //     controller : 'homeController'
    // })
    .when('/viewResidue', {
        templateUrl : 'views/admin/viewResidue.html',
        controller : 'homeController'
    })
    .when('/viewToday', {
        templateUrl : 'views/admin/viewToday.html',
        controller : 'homeController'
    })
    .when('/chqueIn', {
        templateUrl : 'views/admin/viewChqIn.html',
        controller : 'homeController'
    })
    .when('/assignedCheques', {
        templateUrl : 'views/admin/assignedCheques.html',
        controller : 'homeController'
    })
    .when('/dishonoredCheques', {
        templateUrl : 'views/admin/dishonoredCheques.html',
        controller : 'homeController'
    })
    .when('/switchoutLiquid', {
        templateUrl : 'views/admin/switchoutLiquid.html',
        controller : 'homeController'
    })
    .when('/redemptionLiquid', {
        templateUrl : 'views/admin/redemptionLiquid.html',
        controller : 'homeController'
    })
    .when('/viewLiquid', {
        templateUrl : 'views/admin/viewLiquid.html',
        controller : 'homeController'
    })
    .when('/valuationReport', {
        templateUrl : 'views/admin/viewValuationReport.html',
        controller : 'homeController'
    })
    .when('/aumReport', {
        templateUrl : 'views/admin/viewAumReport.html',
        controller : 'homeController'
    });
});

mouseclicksysApp.controller('homeController', function($scope,$http,$route,$templateCache,$window,$location,$timeout,$filter,$rootScope) 
{
	$scope.mainsection = true;
	$scope.section2 = false;
	$scope.section3 = false;

    $scope.showAssign = false;
    $scope.showAssignlqd = false;
    $scope.editslip = false;
    $scope.showAssignlist = true;
    $scope.department = localStorage.department;
    console.log("in homeController");
    
    
    $scope.toggleAssignChqlist = function()
    {
        if($scope.showAssignlist == false)
        {
            $scope.showAssignlist = true;
        }
        else
        {
            $scope.showAssignlist = false;
        }
    }

    $scope.toggleAssignChq = function()
    {
        if($scope.showAssign == false)
        {
            $scope.showAssign = true;
        }
        else
        {
            $scope.showAssign = false;
        }
    }

    $scope.toggleAssignLqd = function()
    {
        if($scope.showAssignlqd == false)
        {
            $scope.showAssignlqd = true;
        }
        else
        {
            $scope.showAssignlqd = false;
        }
    }
    /*$scope.test = function()
    {
        var param = JSON.stringify({
            "msg" : "from app.js"
        });

        $http.post("http://159.89.193.43:9876/test",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {                   
                iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                location.reload();
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });

    }*/

    $scope.calctotalamtarr = []
    $scope.calctotalamt = function(id,arr)
    {
    	var total = 0;
    	var total2 = 0;
    	$scope.calctotalamtarr.total = 0;
    	$scope.calctotalamtarr.total2 = 0;
    	if (id == "Family") {
    		angular.forEach($scope[arr], function(x){
    			// if (x.Family == $scope.calctotalamtarr.family) {
    			// 	total += parseInt(x.Amount)
    			// }
    			if (x.Family.toLowerCase().indexOf($scope.calctotalamtarr.family.toLowerCase()) != -1) {
    				total += parseInt(x.Amount);
    				total2 += parseInt(x.pnl);
    				console.log(total);
    			}
    		});
    		
    		console.log(total);
    		$scope.calctotalamtarr.total = total;
    		$scope.calctotalamtarr.total2 = total2;
    	}

		if (id == "SchemeName") {
    		angular.forEach($scope[arr], function(x){
    			// if (x.Family == $scope.calctotalamtarr.family) {
    			// 	total += parseInt(x.Amount)
    			// }
    			if (x.SchemeName.toLowerCase().indexOf($scope.calctotalamtarr.sname.toLowerCase()) != -1) {
    				total += parseInt(x.Amount);
    				total2 += parseInt(x.pnl);
    				console.log(total);
    			}
    		});
    		
    		console.log(total);
    		$scope.calctotalamtarr.total = total;
    		$scope.calctotalamtarr.total2 = total2;
    	}    	


    	if (id == "UCC") {
    		angular.forEach($scope[arr], function(x){
    			if (x.UCC.toLowerCase().indexOf($scope.calctotalamtarr.ucc.toLowerCase()) != -1) {
    				total += parseInt(x.Amount);
    				total2 += parseInt(x.pnl);
    			}
    		});

    		$scope.calctotalamtarr.total = total;
    		$scope.calctotalamtarr.total2 = total2;
    	}
    }


    $scope.getDep = function()
    {
        $http.post("http://159.89.193.43:9876/getalldep")
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.depList=data.deps;                 
                // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
            } else {
                iziToast.info({title: 'Info',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    $scope.changeDepartment = function() {
    	console.log($scope.department);
    	localStorage.department = $scope.department;
    	$route.reload();
    }

    $scope.getAmc = function()
    {
        $http.post("http://159.89.193.43:9876/getallamcs")
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headers = data.headers;
                $scope.amcList=data.amcs;                 
                // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    $scope.getAccNo = function()
     {
         console.log('inside function acc no');
      if($scope.chqIn.Bank==$scope.clientData["Bank1"])
      {
          console.log('inside if 1');
        $scope.chqIn.AccountNo=$scope.clientData["Acc1"];
      }
       if($scope.chqIn.Bank==$scope.clientData["Bank2"])
      {
        $scope.chqIn.AccountNo=$scope.clientData["Acc2"];
      }
       if($scope.chqIn.Bank==$scope.clientData["Bank3"])
      {
        $scope.chqIn.AccountNo=$scope.clientData["Acc3"];
      }
    }

    $scope.getClients = function()
    {
        $http.post("http://159.89.193.43:9876/getallclients")
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headers = data.headers;
                $scope.clists=data.clists;                 
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    $scope.getUCC = function()
    {
        $http.post("http://159.89.193.43:9876/getallucc")
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                // $scope.headers = data.headers;
                $scope.uccs=data.uccs;           
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    $scope.getFamilyHeads = function()
    {
        $http.post("http://159.89.193.43:9876/getFamilyHeads")
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headers = data.headers;
                $scope.familyheads = data.familyheads;               
                // iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };


    $scope.getFamilyNames = function()
    {
        $http.post("http://159.89.193.43:9876/getfamilynames")
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.familynames = data.fnames;                 
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    
    $scope.getChqIns = function()
    {
    	var param = JSON.stringify({
            'Dep' : $scope.department
    	});

        $http.post("http://159.89.193.43:9876/getChqIns",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headers = data.headers;
                $scope.chqinList=data.chqinlist;    
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }


    $scope.getTodays = function()
    {
    	var param = JSON.stringify({
            'Dep' : $scope.department
    	});

        $http.post("http://159.89.193.43:9876/getTodays",param)
        	.success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headers = data.headers;
                $scope.todaylist = data.todaylist;        
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };
       
    $scope.getallswitchout = function()
    {
    	var param = JSON.stringify({
            'Dep' : $scope.department
    	});

        $http.post("http://159.89.193.43:9876/getallswitchout",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headersso = data.headers;
                $scope.solist = data.so;          
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    $scope.getdw = [];
    $scope.getdaywisewithfilter = function()
    {
    	console.log($scope.getdw);
    	if ($scope.getdw['family']) {
    		var familyfordw = $scope.getdw['family'];
    	}
    	else
    	{
    		var familyfordw = "none";
    	}

    	if ($scope.getdw['ucc']) {
    		var uccfordw = $scope.getdw['ucc']['UCC']
    	}
    	else
    	{
    		var uccfordw = "none";
    	}

    	if ($scope.getdw['date']) {
    		var datefordw = $scope.getdw['date'];
    	}
    	else
    	{
    		var datefordw = "none";
    	}

    	if ($scope.getdw['dep'] != 'all') {
    		var depfordw = $scope.getdw['dep'];
    	}
    	else
    	{
    		var depfordw = "none";
    	}


    	var param = JSON.stringify({
            'UCC': uccfordw,
            'family': familyfordw,
            'Date' : datefordw,
            'Dep' : depfordw
    	});

    	console.log(param);

        $http.post("http://159.89.193.43:9876/getdaywisewithfilter",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.dwheaders = data.headers;
                $scope.daywisefilter = data.daywiselist;
                $scope.amounttotal = data.amounttotal;
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };



    $scope.getDaywiseLiquid = function()
    {
    	var param = JSON.stringify({
            'Dep' : $scope.department
    	});

        $http.post("http://159.89.193.43:9876/getDaywiseliquid",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headers = data.headers;
                $scope.daywiseliquidlist = data.liquidlist;          
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    
    $scope.getResidue = function()
    {
        $http.post("http://159.89.193.43:9876/getResidue")
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headers = data.headers;
                $scope.residuelist = data.residuelist;          
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };


    $scope.getDaywise = function()
    {
        $http.post("http://159.89.193.43:9876/getDaywise")
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headers = data.headers;
                $scope.daywiselist = data.daywiselist;          
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };


    $scope.addNewAMC = function()
    {
      
        var param = JSON.stringify(
            $scope.newamc
        );

      console.log(param);

        $http.post("http://159.89.193.43:9876/addNewAMC",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                location.reload();
                iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };


    $scope.addNewClient = function()
    {

      var param = JSON.stringify(
            $scope.client
        );

      console.log(param);

        $http.post("http://159.89.193.43:9876/addNewClient",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                location.reload();
                iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    $scope.editClient = function()
    {

      var param = JSON.stringify(
            $scope.clientData
        );

      console.log(param);

        $http.post("http://159.89.193.43:9876/editClient",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                location.reload();
                iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    $scope.getClientByucc = function(ucc)
    {

      var param = JSON.stringify({
            "ucc" : ucc
      });

      console.log(param);

        $http.post("http://159.89.193.43:9876/getClientByucc",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.clientData = data.clientData;
                $scope.chqIn.Bank=$scope.clientData['Bank1'];
                $scope.getAccNo();
                //location.reload();
                //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };


    $scope.makeFamilyhead = function(ucc,family)
    {
      
    // console.log(ucc);

      var param = JSON.stringify({
        "ucc" : ucc,
        "family" : family
    });

      iziToast.question({
        timeout: 20000,
        close: false,
        overlay: true,
        toastOnce: true,
        id: 'question',
        zindex: 999,
        title: 'Hey',
        message: 'Are you sure about this?',
        position: 'center',
        buttons: [
            ['<button><b>YES</b></button>', function (instance, toast) {
     
                instance.hide({ transitionOut: 'fadeOut' }, toast, 'button');

                $http.post("http://159.89.193.43:9876/editFamilyhead",param)
                  .success(function (data) {
                      console.log(data);
                      if (data.success == "true") {             
                          iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                          location.reload();
                          /*jQuery('#editAmc').modal('hide');
                          $scope.getAmc();*/
                      } else {
                          iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
                      }
                  })
                  .error(function (err) {
                      iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
                  });
            }, true],
            ['<button>NO</button>', function (instance, toast) {
     
                instance.hide({ transitionOut: 'fadeOut' }, toast, 'button');
     
            }],
        ],
        onClosing: function(instance, toast, closedBy){
            console.info('Closing | closedBy: ' + closedBy);
        },
        onClosed: function(instance, toast, closedBy){
            console.info('Closed | closedBy: ' + closedBy);
        }
    });
    }

    $scope.saveEditedAmc=function(id)
    {
        console.log('in saveEditedAmc');
        console.log($scope.amcData);
        delete $scope.amcData._id;

        var param = JSON.stringify({
            "info" : $scope.amcData,
            "id" :id
        });

        console.log(param);

        $http.post("http://159.89.193.43:9876/editamc",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {             
                iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                location.reload();
                /*jQuery('#editAmc').modal('hide');
                $scope.getAmc();*/
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }

    $scope.getAmcDetails = function(id)
    {
        console.log(id);
        $scope.amcData = $filter('filter')($scope.amcList, {'_id':id});
        $scope.amcData=JSON.parse(angular.toJson($scope.amcData))
        $scope.amcData = $scope.amcData[0];
        console.log($scope.amcData);
    }

    $scope.deleteAmc = function(id)
    {
      var param = JSON.stringify({
            "id" :id
        });

      iziToast.question({
        timeout: 20000,
        close: false,
        overlay: true,
        toastOnce: true,
        id: 'question',
        zindex: 999,
        title: 'Hey Admin',
        message: 'Are you sure about this?',
        position: 'center',
        buttons: [
            ['<button><b>YES</b></button>', function (instance, toast) {
     
                instance.hide({ transitionOut: 'fadeOut' }, toast, 'button');

                $http.post("http://159.89.193.43:9876/deleteamc",param)
                    .success(function (data) {
                        console.log(data);
                        if (data.success == "true") {             
                            iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                            location.reload();
                            /*jQuery('#editAmc').modal('hide');
                            $scope.getAmc();*/
                        } else {
                            iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
                        }
                    })
                    .error(function (err) {
                        iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
                    });
            }, true],
            ['<button>NO</button>', function (instance, toast) {
     
                instance.hide({ transitionOut: 'fadeOut' }, toast, 'button');
     
            }],
        ],
        onClosing: function(instance, toast, closedBy){
            console.info('Closing | closedBy: ' + closedBy);
        },
        onClosed: function(instance, toast, closedBy){
            console.info('Closed | closedBy: ' + closedBy);
        }
    });
        
        

    };



    $scope.exportswitchdone = function()
    {
    	iziToast.question({
                drag: false,
                close: false,
                overlay: true,
                title: 'SwitchDate',
                message: 'Enter Date for SwitchDone:',
                position: 'center',
                inputs: [
                    ['<input type="date">', 'keyup', function (instance, toast, input, e) {
                        console.info(input.value);
                    }, true],
                ],
                buttons: [
                    ['<button><b>Confirm</b></button>', function (instance, toast, button, e, inputs) {
                        // alert('First field: ' + inputs[0].value)
                        instance.hide({ transitionOut: 'fadeOut' }, toast, 'button');

                        var param = JSON.stringify({
                            'sodate': inputs[0].value,
                            'Dep' : $scope.department
                        });

                        console.log(param);

                        $http.post("http://159.89.193.43:9876/exportswitchdone",param)
                          .success(function (data) {
                              console.log(data);
                              if (data.success == "true") {
                                  $window.open("http://159.89.193.43/mouseclicksys/switchout.xlsx",'_blank');
                                  // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                                  // location.reload();
                                  /*jQuery('#editAmc').modal('hide');
                                  $scope.getAmc();*/
                              } else {
                                  iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
                              }
                          })
                          .error(function (err) {
                              iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
                          });
                    }, false], // true to focus
                ]
            });
    }



    $scope.exportTodays = function()
    {
		// console.log($scope.f);

      if ($scope.f == undefined)
      {
      	iziToast.info({title: 'Info',message: "Please select date for excel!", position: 'topRight'});
      }
      else{

      var param = JSON.stringify({
          'todaydate': $scope.f.BuyDate,
          'Dep' : $scope.department
      });

      console.log(param);

      $http.post("http://159.89.193.43:9876/exportTodays",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $window.open("http://159.89.193.43/mouseclicksys/today.xlsx",'_blank');
                // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                // location.reload();
                /*jQuery('#editAmc').modal('hide');
                $scope.getAmc();*/
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });

      // iziToast.question({
      //           drag: false,
      //           close: false,
      //           overlay: true,
      //           title: 'TodayDate',
      //           message: 'Enter Date for today:',
      //           position: 'center',
      //           inputs: [
      //               ['<input type="date">', 'keyup', function (instance, toast, input, e) {
      //                   console.info(input.value);
      //               }, true],
      //           ],
      //           buttons: [
      //               ['<button><b>Confirm</b></button>', function (instance, toast, button, e, inputs) {
      //                   instance.hide({ transitionOut: 'fadeOut' }, toast, 'button');

      //                   var param = JSON.stringify({
      //                       'todaydate': inputs[0].value
      //                   });

      //                   console.log(param);

      //                   $http.post("http://159.89.193.43:9876/exportTodays",param)
      //                     .success(function (data) {
      //                         console.log(data);
      //                         if (data.success == "true") {
      //                             $window.open("http://159.89.193.43/mouseclicksys/today.xlsx",'_blank');
      //                             // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
      //                             // location.reload();
      //                             /*jQuery('#editAmc').modal('hide');
      //                             $scope.getAmc();*/
      //                         } else {
      //                             iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
      //                         }
      //                     })
      //                     .error(function (err) {
      //                         iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
      //                     });
      //               }, false], // true to focus
      //           ]
      //       });
    }
}



    $scope.uploadswitchoutexcel = function()
    {
    	waitingDialog.show("...Please wait");
        console.log('in uploadsoExcel');
        var uploadUrl = "http://159.89.193.43:9876/uploadsofile";
        var file = $scope.switchoutexcelfile;
        if (file != undefined) {
          var fd = new FormData();
          fd.append('file', file);
  
          $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {
              'Content-Type': undefined
            }
          })
          .success(function(data) {
  
            if (data.success == "true") {
              waitingDialog.hide();
              iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
              file = undefined;
              $scope.switchoutexcelfile = undefined;
              location.reload();
              //$('#uploadAmcExcel').modal('hide');
  
            }
            else 
            {
              waitingDialog.hide();
              location.reload();
              //$('#uploadAmcExcel').modal('hide');
              iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
              file = undefined;
              $scope.todayexcelfile = undefined;
            }
          })
          .error(function() {
            waitingDialog.hide();
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
            file = undefined;
          });
        }
    }

    $scope.uploadtodayexcel = function()
    {
        waitingDialog.show("...Please wait");
        console.log('in uploadAmcExcel');
        var uploadUrl = "http://159.89.193.43:9876/uploadtodayfile";
        var file = $scope.todayexcelfile;
        if (file != undefined) {
          var fd = new FormData();
          fd.append('file', file);
  
          $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {
              'Content-Type': undefined
            }
          })
          .success(function(data) {
  
            if (data.success == "true") {
              waitingDialog.hide();
              iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
              file = undefined;
              $scope.todayexcelfile = undefined;
              location.reload();
              //$('#uploadAmcExcel').modal('hide');
  
            }
            else 
            {
              waitingDialog.hide();
              location.reload();
              //$('#uploadAmcExcel').modal('hide');
              iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
              file = undefined;
              $scope.todayexcelfile = undefined;
            }
          })
          .error(function() {
            waitingDialog.hide();
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
            file = undefined;
          });
        }  
    }

    $scope.uploadAmcExcel = function()
    {
      waitingDialog.show("...Please wait");
      console.log('in uploadAmcExcel');
      var uploadUrl = "http://159.89.193.43:9876/uploaddailyamc";
      var file = $scope.amcExcelFile;
      if (file != undefined) {
        var fd = new FormData();
        fd.append('file', file);

        $http.post(uploadUrl, fd, {
          transformRequest: angular.identity,
          headers: {
            'Content-Type': undefined
          }
        })
        .success(function(data) {

          if (data.success == "true") {
            waitingDialog.hide();
            iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
            file = undefined;
            $scope.amcExcelFile = undefined;
            location.reload();
            //$('#uploadAmcExcel').modal('hide');

          }
          else 
          {
            waitingDialog.hide();
            location.reload();
            //$('#uploadAmcExcel').modal('hide');
            iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            file = undefined;
            $scope.amcExcelFile = undefined;
          }
        })
        .error(function() {
          waitingDialog.hide();
          iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
          file = undefined;
        });
      }
    };

    $scope.uploadclientlistexcel = function()
    {
      waitingDialog.show("...Please wait");
      console.log('in uploadclientlistexcel');
      var uploadUrl = "http://159.89.193.43:9876/uploadclientlist";
      var file = $scope.clistexcel;
      if (file != undefined) {
        var fd = new FormData();
        fd.append('file', file);

        $http.post(uploadUrl, fd, {
          transformRequest: angular.identity,
          headers: {
            'Content-Type': undefined
          }
        })
        .success(function(data) {

          if (data.success == "true") {
            waitingDialog.hide();
            iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
            file = undefined;
            $scope.clistexcel = undefined;
            location.reload();
            //$('#uploadAmcExcel').modal('hide');

          }
          else 
          {
            waitingDialog.hide();
            location.reload();
            //$('#uploadAmcExcel').modal('hide');
            iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            file = undefined;
            $scope.clistexcel = undefined;
          }
        })
        .error(function() {
          waitingDialog.hide();
          iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
          file = undefined;
        });
      }
    };


    $scope.uploadchequinexcel = function()
    {
        waitingDialog.show("...Please wait");
        console.log('in uploadchequinexcel');
        var uploadUrl = "http://159.89.193.43:9876/uploadchequinexcel";
        var file = $scope.chqinlistexcel;
        if (file != undefined) {
          var fd = new FormData();
          fd.append('file', file);
  
          $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {
              'Content-Type': undefined
            }
          })
          .success(function(data) {
  
            if (data.success == "true") {
              waitingDialog.hide();
              iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
              file = undefined;
              $scope.chqinlistexcel = undefined;
              location.reload();
              //$('#uploadAmcExcel').modal('hide');
  
            }
            else 
            {
              waitingDialog.hide();
              location.reload();
              //$('#uploadAmcExcel').modal('hide');
              iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
              file = undefined;
              $scope.chqinlistexcel = undefined;
            }
          })
          .error(function() {
            waitingDialog.hide();
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
            file = undefined;
          });
        }
    };

    $scope.getChequeDetails = function(ucc,chq)
    {
        $scope.CheqData = $filter('filter')($scope.chqinList, {'UCC':ucc,'ChqNo':chq});
        $scope.CheqData=JSON.parse(angular.toJson($scope.CheqData))
        $scope.CheqData = $scope.CheqData[0];
        $scope.getClientByucc($scope.CheqData.UCC);
        console.log($scope.CheqData);
    };

    $scope.saveChequeIn = function()
    {

        console.log($scope.CheqData);
        delete $scope.CheqData._id;

        var param = JSON.stringify(
            $scope.CheqData
        );

        console.log(param);

        $http.post("http://159.89.193.43:9876/editchqin",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {             
                iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                location.reload();
                /*jQuery('#editAmc').modal('hide');
                $scope.getAmc();*/
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    $scope.addChqueIn = function()
    {

        // console.log($scope.CheqData);
        // delete $scope.CheqData._id;
        $scope.chqIn['Dep'] = $scope.department;

        var param = JSON.stringify(
            $scope.chqIn
        );

        console.log(param);

        $http.post("http://159.89.193.43:9876/addnewchqin",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {             
                iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                location.reload();
                /*jQuery('#editAmc').modal('hide');
                $scope.getAmc();*/
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    };

    $scope.chequelist = { selected : {}};

    $scope.preassign = function()
    {
        console.log($scope.chequelist);
        var param = JSON.stringify(
            $scope.chequelist.selected
        );
        console.log(param);

        $http.post("http://159.89.193.43:9876/preassign",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                //iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                location.reload();
                /*jQuery('#editAmc').modal('hide');
                $scope.getAmc();*/
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }


    $scope.preassignlqdremove = function(orderno)
    {
        // console.log($scope.chequelist);
        var param = JSON.stringify({
            'orderno':orderno
            });
        console.log(param);

        $http.post("http://159.89.193.43:9876/preassignlqdremove",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                //iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                location.reload();
                /*jQuery('#editAmc').modal('hide');
                $scope.getAmc();*/
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }



    $scope.preassignremove = function(chqno)
    {
        console.log($scope.chequelist);
        var param = JSON.stringify({
            'chqno':chqno
            });
        console.log(param);

        $http.post("http://159.89.193.43:9876/preassignremove",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                //iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                location.reload();
                /*jQuery('#editAmc').modal('hide');
                $scope.getAmc();*/
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }

    
    $scope.getuccamcwisenewschemes = function(ucc,amc)
    {
        delete $scope.newschemelist.selected;
        delete $scope.uccamcnewscheme;

        var param = JSON.stringify({
            'UCC':ucc,
            'AMC':amc
        });

        // console.log(param);

        $http.post("http://159.89.193.43:9876/getuccamcwisenewschemes",param)
        .success(function (data) {
            // console.log(data);
            if (data.success == "true") {
                $scope.uccamcnewscheme = data.uccamcnewscheme;
                $scope.newschemehead = data.newschemehead;
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }


    $scope.getuccwisenewschemes = function(ucc)
    {
        delete $scope.newschemelist.selected;
        delete $scope.uccnewscheme;
        console.log(ucc);
        var param = JSON.stringify({
            'UCC':ucc
        });

        console.log(param);

        $http.post("http://159.89.193.43:9876/getuccwisenewschemes",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.uccnewscheme = data.uccnewscheme;
                $scope.newschemehead = data.newschemehead;
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }

    

    $scope.getuccdatafromdaywiseamc = function(ucc,amc)
    {
        delete $scope.uccdaywiseamc;
        console.log(ucc);
        var param = JSON.stringify({
            'UCC':ucc,
            'AMC':amc
        });

        console.log(param);

        $http.post("http://159.89.193.43:9876/getuccdatafromdaywiseamc",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.uccdaywiseamc = data.uccdaywiseamc;
                $scope.uccheadersamc = data.uccheadersamc;
            } else {
                iziToast.info({title: 'Info',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }

    $scope.getuccdatafromdaywise = function(ucc)
    {

        delete $scope.uccdaywise;
        console.log(ucc);
        var param = JSON.stringify({
            'UCC':ucc
        });

        console.log(param);

        $http.post("http://159.89.193.43:9876/getuccdatafromdaywise",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.uccdaywise = data.uccdaywise;
                $scope.uccheaders = data.uccheaders;
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }

    $scope.chequeamount = 0;

    $scope.setchequeamount = function(amt)
    {
        $scope.chequeamount = amt;
    }

    $scope.updateTotal = function(){
        var total = 0;
        angular.forEach($scope.uccdaywise, function(x){
            if(x.values != undefined)
            {
                
                if(x.values.length!=0)
                {
                    // console.log(x.values);
                    total += parseInt(x.values);
                    if($scope.chequeamount < total)
                    {
                        iziToast.error({title: 'Error',message: "Cheque Amount Exceeded !", position: 'topRight'});
                    }
                }
               
            }
      //  console.log(total);
      
       // console.log(parseInt(x.values));
        /*    if(x.values != "undefined" || x.values !=NaN||x.values!="")
            {
                console.log(x.values);
            total += parseInt(x.values);
            if($scope.chequeamount < total)
            {
                iziToast.error({title: 'Error',message: "Cheque Amount Exceeded !", position: 'topRight'});
            }
            }*/
      //  console.log(total);
        });
        
        // console.log(total+0);
        $scope.total = parseInt(total);
      };

      $scope.finalassigncheque = function()
      {
        // console.log(parseInt($scope.chequeamount));
        // console.log(parseInt(total));

        if( parseInt($scope.chequeamount) != parseInt($scope.total))
        {
            iziToast.error({title: 'Error',message: "Cheque Amount Does Not Match !", position: 'topRight'});
        }
        else
        {
            console.log($scope.assignchqinfo);
            console.log($scope.uccdaywise);

            // iziToast.success({title: 'Success',message: "Cheque Assgined Successfully!", position: 'topRight'});
            iziToast.question({
                drag: false,
                close: false,
                overlay: true,
                title: 'BuyDate',
                message: 'Enter Deposited Date :',
                position: 'center',
                inputs: [
                    ['<input type="date">', 'keyup', function (instance, toast, input, e) {
                        console.info(input.value);
                    }, true],
                ],
                buttons: [
                    ['<button><b>Confirm</b></button>', function (instance, toast, button, e, inputs) {
                        // alert('First field: ' + inputs[0].value)
                        instance.hide({ transitionOut: 'fadeOut' }, toast, 'button');

                        var param = JSON.stringify({
                            'UCC':$scope.assignchqinfo['assignucc'],
                            'Family':$scope.assignchqinfo['assignfamily'],
                            'ChqNo':$scope.assignchqinfo['assignchqno'],
                            'daywiseuccdata': $scope.uccdaywise,
                            'BuyDate': inputs[0].value,
                            'Dep' : $scope.department
                        });

                        console.log(param);

                        $http.post("http://159.89.193.43:9876/finalassigncheque",param)
                            .success(function (data) {
                                console.log(data);
                                if (data.success == "true") {             
                                    iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                                    location.reload();
                                } else {
                                    iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
                                }
                            })
                            .error(function (err) {
                                iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
                            });

                    }, false], // true to focus
                ]
            });
        }
      }

      $scope.assignchqinfo = [];

      $scope.getAssignedCheques = function()
      {
        delete $scope.finas;
        var param = JSON.stringify({
            'Dep' : $scope.department
        });
        $http.post("http://159.89.193.43:9876/getAssignedCheques",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headers = data.headers;
                $scope.finas=data.finas;
                // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
      }

      $scope.getDishonChqs = function()
      {
        delete $scope.dishonlist;
        var param = JSON.stringify({
            'Dep' : $scope.department
        });
        $http.post("http://159.89.193.43:9876/getDishonChqs",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.headers = data.headers;
                $scope.dishonlist=data.dishonlist;
                // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
            } else {
                iziToast.info({title: 'Info',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
      }

      $scope.getsliplesscheques = function()
      {
      	var param = JSON.stringify({
            'Dep' : $scope.department
        });

        $http.post("http://159.89.193.43:9876/getsliplesscheques",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                // $scope.headers = data.headers;
                $scope.slipless=data.slipless;
                // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
            } else {
                iziToast.info({title: 'Info',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
      }

      $scope.addslipnumber = function()
      {
          console.log($scope.slipless);
          var param = JSON.stringify(
            $scope.slipless
        );

        $http.post("http://159.89.193.43:9876/addslipnumber",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                // $scope.headers = data.headers;
                delete $scope.slipless;
                $scope.getAssignedCheques();
                $("#assignslip").hide();
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();
                // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
      }
    
      $scope.toggleslipedit = function()
      {
          if($scope.editslip == true)
          {
            $scope.editslip = false;
          }
          else
          {
            $scope.editslip = true;
          }
      }
    
      $scope.newschemelist = [];

      $scope.addnewschemesforucc = function(ucc)
      {
          
        // console.log($scope.uccdaywise);
        // console.log($scope.newschemelist);
        // console.log($scope.uccnewscheme);
        // delete $scope.newschemelist;
        delete $scope.finaldata;

        var param = JSON.stringify({
            'UCC':ucc,
            'newschemeamc':$scope.newschemelist.selected
        });

      $http.post("http://159.89.193.43:9876/getamcwiseuccdata",param)
        .success(function (data) {
            // console.log(data);
            if (data.success == "true") {
                $scope.finaldata=data.finaldata;
                // console.log($scope.finaldata);
                for(var i=0;i<$scope.finaldata.length;i++)
                {
                    $scope.uccdaywise.push($scope.finaldata[i]);
                };
                // $scope.uccdaywise.push($scope.finaldata);
                console.log($scope.uccdaywise);
                // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
      }



      $scope.newschemelistamc = [];

      $scope.addnewschemesforuccamc = function(ucc,amc)
      {
          
        // console.log($scope.uccdaywise);
        // console.log($scope.newschemelist);
        // console.log($scope.uccnewscheme);
        // delete $scope.newschemelist;
        delete $scope.finaldataamc;

        var param = JSON.stringify({
            'UCC':ucc,
            'AMC':amc,
            'schemenames':$scope.newschemelistamc.selected
        });
        console.log(param);

      $http.post("http://159.89.193.43:9876/getamcwiseuccdataamc",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                $scope.finaldataamc=data.finaldataamc;
                console.log($scope.finaldataamc);
                for(var i=0;i<$scope.finaldataamc.length;i++)
                {
                    $scope.uccdaywiseamc.push($scope.finaldataamc[i]);
                };
                // $scope.uccdaywise.push($scope.finaldata);
                console.log($scope.uccdaywiseamc);
                // iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
      }



      $scope.dishonchqdata = [];

      $scope.getuccdatewisetransactions = function(ucc,date)
      {
          delete $scope.rejtrans;
          var param = JSON.stringify({
              'UCC':ucc,
              'Date':date
          });

          $http.post("http://159.89.193.43:9876/getuccdatewisetransactions",param)
            .success(function (data) {
                if (data.success == "true") {
                    $scope.rejtrans=data.rejtrans;
                    $scope.rejtranheaders = data.headers;
                } else {
                    iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
                }
            })
            .error(function (err) {
                iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
            });
      }

      $scope.rejecttranslist = [];
      $scope.dishonourcheque = function()
      {
          console.log($scope.dishonchqdata);
          console.log($scope.rejecttranslist);

        var param = JSON.stringify({
            'UCC' : $scope.dishonchqdata['UCC'],
            'Slip' : $scope.dishonchqdata['Slip'],
            'ChqNo' : $scope.dishonchqdata['ChqNo'],
            'rejlist' : $scope.rejecttranslist.selected
        });

        $http.post("http://159.89.193.43:9876/dishonourcheque",param)
            .success(function (data) {
                if (data.success == "true") {
                    location.reload();
                } else {
                    iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
                }
            })
            .error(function (err) {
                iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
            });

      }


    $scope.liquidlist = { selected : {}};

    $scope.preassignLqd = function()
    {
        // console.log($scope.chequelist);
        var param = JSON.stringify(
            $scope.liquidlist.selected
        );
        console.log(param);

        $http.post("http://159.89.193.43:9876/preassignLqd",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                //iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                location.reload();
                /*jQuery('#editAmc').modal('hide');
                $scope.getAmc();*/
            } else {
                iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }

    $scope.assignlqdinfo = [];

    $scope.liquidamount = 0;

    $scope.setliquidamount = function(amt)
    {
        $scope.liquidamount = amt;
    }


    $scope.updateTotallqd = function(){
        var total = 0;
        angular.forEach($scope.uccdaywiseamc, function(x){
            if(x.values != undefined)
            {
                
                if(x.values.length!=0)
                {
                    // console.log(x.values);
                    total += parseInt(x.values);
                    if($scope.liquidamount < total)
                    {
                        iziToast.error({title: 'Error',message: "Liquid Amount Exceeded !", position: 'topRight'});
                    }
                }
               
            }
        });
        
        // console.log(total+0);
        $scope.total = parseInt(total);
      };

      $scope.updateTotalpartlqd = function()
      {
          if(parseInt($scope.partamt) > parseInt($scope.assignlqdinfo['assignpartamt']))
          {
            iziToast.error({title: 'Error',message: "Amount Exceeded !", position: 'topRight'});
          }
      }
    
      $scope.finalassignliquid = function()
      {
        // console.log(parseInt($scope.chequeamount));
        // console.log(parseInt(total));

        if( parseInt($scope.liquidamount) != parseInt($scope.total))
        {
            iziToast.error({title: 'Error',message: "Liquid Amount Does Not Match !", position: 'topRight'});
        }
        else
        {
            console.log($scope.assignlqdinfo);
            console.log($scope.uccdaywiseamc);
            // console.log($scope.assignlqdinfo['assignpartamt']);

            // iziToast.success({title: 'Success',message: "Cheque Assgined Successfully!", position: 'topRight'});
            iziToast.question({
                drag: false,
                close: false,
                overlay: true,
                title: 'SwitchDate',
                message: 'Enter Switch Date :',
                position: 'center',
                inputs: [
                    ['<input type="date">', 'keyup', function (instance, toast, input, e) {
                        console.info(input.value);
                    }, true],
                ],
                buttons: [
                    ['<button><b>Confirm</b></button>', function (instance, toast, button, e, inputs) {
                        // alert('First field: ' + inputs[0].value)
                        instance.hide({ transitionOut: 'fadeOut' }, toast, 'button');

                        var param = JSON.stringify({
                            'UCC':$scope.assignlqdinfo['assignucc'],
                            'AMC':$scope.assignlqdinfo['assignamc'],
                            'OrderNo':$scope.assignlqdinfo['assignorderno'],
                            'origamt':$scope.assignlqdinfo['assignpartamt'],
                            'uccdaywiseamc': $scope.uccdaywiseamc,
                            'liquidamount' : $scope.liquidamount,
                            'SwitchDate': inputs[0].value
                        });

                        console.log(param);

                        $http.post("http://159.89.193.43:9876/finalassignliquid",param)
                            .success(function (data) {
                                console.log(data);
                                if (data.success == "true") {             
                                    iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                                    location.reload();
                                } else {
                                    iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
                                }
                            })
                            .error(function (err) {
                                iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
                            });

                    }, false], // true to focus
                ]
            });
        }
      }


    $scope.todayseldate = new Date();


    $scope.valuation = {};
    $scope.generateValuationReport = function()
    {
    	var param = JSON.stringify(
    		$scope.valuation
    	);
        if ($scope.valuation['ucc']) {
          console.log(param);
        }

        $http.post("http://159.89.193.43:9876/generateValuationReport",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
                //iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                // location.reload();
                /*jQuery('#editAmc').modal('hide');
                $scope.getAmc();*/
                $scope.daywisereport = data.result1;
                $scope.chqueInreport = data.result2;
                $scope.reptamt1 = 0;
                var total = 0;
                $scope.reptpnl1 = 0;
                var total2 = 0;
                $scope.reptamt2 = 0;
                var total3 = 0;
                $scope.reptval1 = 0;

                angular.forEach($scope.daywisereport, function(x){
                  total += parseInt(x.Amount);  
                  total2 += parseInt(x.pnl);
                  x['val'] = parseInt(x.Amount) + parseInt(x.pnl)
                });

                angular.forEach($scope.chqueInreport, function(x){
                  total3 += parseInt(x.Amount);
                  // total2 += parseInt(x.pnl);  
                });

                $scope.reptamt1 = total;
                $scope.reptpnl1 = total2;
                $scope.reptamt2 = total3;
                $scope.reptval1 = total+total2;

            } else {
                iziToast.info({title: 'Info',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }

    $scope.aum = {};
    $scope.generateAUMReport = function()
    {
      var param = JSON.stringify(
        $scope.aum
      );

        $http.post("http://159.89.193.43:9876/generateAUMReport",param)
        .success(function (data) {
            console.log(data);
            if (data.success == "true") {
              $scope.aumrep = data.aumrep;
              $scope.headaum = data.headaum;
                //iziToast.show({theme: 'dark',title:'Success',message: data.message,position: 'topRight',icon: 'fa fa-user',progressBarColor: 'rgb(0, 255, 184)'});
                // location.reload();
                /*jQuery('#editAmc').modal('hide');
                $scope.getAmc();*/
                // $scope.daywisereport = data.result1;
                // $scope.chqueInreport = data.result2;
                // $scope.reptamt1 = 0;
                // var total = 0;
                // $scope.reptpnl1 = 0;
                // var total2 = 0;
                // $scope.reptamt2 = 0;
                // var total3 = 0;

                // angular.forEach($scope.daywisereport, function(x){
                //   total += parseInt(x.Amount);  
                //   total2 += parseInt(x.pnl);  
                // });

                // angular.forEach($scope.chqueInreport, function(x){
                //   total3 += parseInt(x.Amount);
                //   // total2 += parseInt(x.pnl);  
                // });

                // $scope.reptamt1 = total;
                // $scope.reptpnl1 = total2;
                // $scope.reptamt2 = total3;

            } else {
                iziToast.info({title: 'Info',message: data.message, position: 'topRight'});
            }
        })
        .error(function (err) {
            iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
        });
    }

});


