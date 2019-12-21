var overheadsApp = angular.module('overheadsApp', ['ngRoute','smart-table','ui.multiselect','datatables','moment-picker']);

overheadsApp.directive('fileModel', ['$parse', function($parse) {
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


overheadsApp.filter('num', function() {
    return function(input) {
       return parseInt(input, 10);
    }
});

overheadsApp.directive('stSelectDistinct', [function() {
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
    



overheadsApp.filter('unique', function() {
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


overheadsApp.filter('customFilter', ['$filter', function($filter) {
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

overheadsApp.filter('titlecase', function() {
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

    overheadsApp.config(function($sceProvider) {
        $sceProvider.enabled(false);
    });

overheadsApp.config(function($sceProvider) {
    $sceProvider.enabled(false);
});

overheadsApp.config(function($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl : 'views/home.html',
        controller : 'homeController'
    })
    .when('/editSheet', {
        templateUrl : 'views/editSheet.html',
        controller : 'homeController'
    })
    .when('/sheetData', {
        templateUrl : 'views/sheetData.html',
        controller : 'homeController'
    });
});

overheadsApp.controller('homeController', function($compile,$scope,$http,$route,$templateCache,$window,$location,$timeout,$filter,$rootScope) 
{
  console.log('in overheadsApp controller');

  $scope.getAllUCC = function()
  {
    $http.post("http://159.89.193.43:9876/getallucc")
    .success(function (data) {
      console.log(data);
      if (data.success == "true") {
        $scope.uccList=data.uccs;           
      } else {
        iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
      }
    })
    .error(function (err) {
      iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
    });
  };

  $scope.addDepartment = function(){
    $scope.departments=true;
    console.log($scope.deptName);
    if ($scope.deptName==undefined) {
      iziToast.error({title: 'Error',message: "Please Enter Name !", position: 'topRight'});
    }
    else{
      $scope.depCount +=1;
      var deptRow = angular.element(document.querySelector( '#departments' ));
      deptRow.append('<div class="col"><div class="card"><div class="card-header bg-warning">Col '+$scope.depCount+' :  '+$scope.deptName+'<button class="btn btn-sm btn-success ml-5" ng-click="addColumn('+$scope.depCount+');testval=9999;">+</button></div><div class="card-body">body</div></div></div>');
      $compile(deptRow.contents())($scope);
      $scope.deptName="";

    }    
  };

  $scope.addColumn = function(depNo){
    console.log('in addColumn');    
    console.log(depNo);

  };

  $scope.saveSheet=function() {
    var flag = 0;
    if ($scope.sheet.ucc==undefined) {
      iziToast.error({title: 'Error',message:"Please Select UCC", position: 'topRight'});

    }
    else if($scope.sheet.sheetName==undefined)
    {
      iziToast.error({title: 'Error',message:"Please Select Number Of Installment", position: 'topRight'});
    }
    else if($scope.sheet.NoOfDepartments==undefined)
    {
      iziToast.error({title: 'Error',message:"Please Select Number Of departments", position: 'topRight'});
    }
    else{
      console.log('in else');
      
      for (var i = 0; i < $scope.sheet.NoOfDepartments; i++) {
        var cCnt = parseInt($scope.sheet.department[i].colCount);
        for (var j = 0; j < cCnt; j++) {
        	if ($scope.sheet.department[i].col[j].isFormula==true) {
        	 
        		if ($scope.sheet.department[i].col[j].formula != "" && $scope.sheet.department[i].col[j].formula != undefined) {
        			flag = 1;
        			// console.log($scope.sheet.department[i].col[j].formula);
        		}
        		else
        		{
        		  /*console.log("flg 0 condiition");
        		   console.log($scope.sheet.department[i].col[j].colName);*/
        			flag=0;
        			break;
        		}
        		
        	}
        	else{
        		flag=1;}
        	//console.log();	
        }
        if(flag==0)
        {
        	break;
        }
      }
    }

    if (flag==0) {
      iziToast.error({title: 'Error',message:"Please Fill Data", position: 'topRight'});
    }
    else{
      console.log('in saveSheet');
      var param = JSON.stringify(
              $scope.sheet
          );
      console.log($scope.sheet);

      $http.post("http://159.89.193.43:2840/saveSheet",param)
      .success(function (data) {
        if (data.success == "true") {
          iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
          location.reload();          
        } else {
          iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
        }
      })
      .error(function (err) {
        iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
      });
    }
  };

  $scope.getSheetByUcc = function(uccData)
  {
  	var param = JSON.stringify({
  		"id":uccData._id
  	});

      $http.post("http://159.89.193.43:2840/getSheetByUcc",param)
      .success(function (data) {
        if (data.success == "true") {
        	console.log(data);
        	$scope.sheetList=data.Sheets;
          $scope.sheetToBeEdited={};
          $scope.sheetData=true;
          //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
                     
        } else {
          iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
          $scope.sheetToBeEdited={};
          $scope.sheetList=[];
          $scope.sheetData=false;
        }
      })
      .error(function (err) {
        $scope.sheetToBeEdited={};
        $scope.sheetList=[];
        $scope.sheetData=false;
        iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
      });
  };

  $scope.selectSheet = function(selectedSheet)
  {
    $scope.colArray=[];
  	console.log(selectedSheet);
  	$scope.sheetToBeEdited=selectedSheet;
  	$scope.sheetDataDiv=true;
  	/*$scope.depCount=parseInt($scope.sheetToBeEdited.NoOfDepartments);

    for (var i = 0; i < $scope.depCount; i++) {
      // console.log('in for');
      // console.log($scope.sheetToBeEdited.department[i].colCount);
      var len=parseInt($scope.sheetToBeEdited.department[i].colCount);
      $scope.colArray.push(len);
    }*/
  };


  $scope.saveEditedSheet=function()
  {
    var param = JSON.parse(angular.toJson($scope.sheetToBeEdited));
    console.log(param);

      $http.post("http://159.89.193.43:2840/saveEditedSheet",param)
      .success(function (data) {
        if (data.success == "true") {
          iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
          location.reload();      	   
        } else {
          iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
        }
      })
      .error(function (err) {
        iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
      });

  };

  $scope.addColumnEditSheet = function()
  {
    console.log('in addColumnEditSheet');
  };

  $scope.addDepartmentEditSheet =function()
  {
    console.log('in addDepartmentEditSheet');
    console.log($scope.sheetToBeEdited);
    if ($scope.sheetToBeEdited.NoOfDepartments == 5) {
      iziToast.error({title: 'Error',message: "Connot Be Exceeded !", position: 'topRight'});
    }
    else{

    	var newArray=[];
    	for (var i = 0; i < $scope.sheetToBeEdited.date.length; i++) {
    		newArray.push("");
    	}

    	for (var i = 0; i < $scope.newDept.colCount; i++) {
    		$scope.newDept.col[i].data=newArray;	
    	}
    	$scope.sheetToBeEdited.department.push($scope.newDept);
        iziToast.show({theme: 'light',title:'Success',message: 'Department Added Successfully',position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
        var cnt =1 + parseInt($scope.sheetToBeEdited.NoOfDepartments);
        $scope.sheetToBeEdited.NoOfDepartments=cnt+"";
      	//console.log($scope.sheetToBeEdited);
      	//$scope.saveEditedSheet();
    }
  };

  $scope.getSheetData= function(sheetSchema)
  {
    console.log(sheetSchema);
    $scope.sheetSchema=sheetSchema;

    var param = JSON.stringify({
      "id":sheetSchema._id
    });

    $http.post("http://159.89.193.43:2840/getSheetDataById",param)
      .success(function (data) {
        if (data.success == "true") {
          console.log(data);
          $scope.sheetData=data.sheetdata;
          console.log($scope.sheetData);
          //iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
                     
        } else {
          iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
        }
      })
      .error(function (err) {
        iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
      });
  };
 $scope.calculateSheet= function(schema,data)
  {
   // console.log(schema);
    for (var i = 0; i < $scope.sheetSchema.NoOfDepartments; i++) {
        var cCnt = parseInt($scope.sheetSchema.department[i].colCount);
        for (var j = 0; j < cCnt; j++) {
          if ($scope.sheetSchema.department[i].col[j].isFormula==true) {
            for(k=0;k<$scope.sheetData[0].date.length;k++)
            {
              f=$scope.sheetSchema.department[i].col[j].formula;
              for(c=0;c<cCnt;c++)
              {

              		if($scope.sheetData[0].department[i].col[c].data[k]=="")
	                {
	                  val="0";
	                }else{val=$scope.sheetData[0].department[i].col[c].data[k];}
              	
                
                f=f.replace($scope.sheetSchema.department[i].col[c].colName,val);
              }
              if($scope.sheetSchema.department[i].col[j].isCarryForward==true)
              {
              	console.log("sjh");
              	if(k==0)
		        {
		        	console.log($scope.sheetData[0]);
		        	f=f.replace("opening",$scope.sheetData[0].department[i].col[j].opening);
		        }else
		        {
		        f=f.replace("opening",$scope.sheetData[0].department[i].col[j].data[k-1]);	
		        }
              }
              /**/
              console.log(f);
              $scope.sheetData[0].department[i].col[j].data[k]=eval(f);
            }         
          }
        }
      }
      console.log($scope.sheetSchema);
      console.log($scope.sheetData);
    };


    $scope.saveCalculatedSheet = function()
    {

      var param = JSON.stringify({
      "sheetData":$scope.sheetData
      });

    $http.post("http://159.89.193.43:2840/saveCalculatedSheet",param)
      .success(function (data) {
        if (data.success == "true") {
          iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
                     
        } else {
          iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
        }
      })
      .error(function (err) {
        iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
      });

    };

    $scope.createNewSheet =function(id)
    {
      console.log($scope.createSheetmonth);
      console.log(id);

      var param = JSON.stringify({
      "id":id,
      "month":$scope.createSheetmonth
      });

      $http.post("http://159.89.193.43:2840/createNewSheet",param)
      .success(function (data) {
        if (data.success == "true") {
          iziToast.show({theme: 'light',title:'Success',message: data.message,position: 'topRight',transitionIn: 'bounceInLeft',icon: 'fa fa-user',progressBarColor: '#dc3545', iconColor: '#007bff'});
                     
        } else {
          iziToast.error({title: 'Error',message: data.message, position: 'topRight'});
        }
      })
      .error(function (err) {
        iziToast.error({title: 'Error',message: "Server Error !", position: 'topRight'});
      });

    };

});


