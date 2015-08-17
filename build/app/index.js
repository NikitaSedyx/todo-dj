;(function(){
  angular
    .module("todo", ["ngResource",
                     "ui.router",
                     "ui.bootstrap",
                     "nm-widgets",
                     "monospaced.elastic",
                     "infinite-scroll",
                     "downloaders"])
})()

;(function(){
  angular
    .module("downloaders", [])
})()

;(function(){
  angular
    .module("nm-widgets", [])
})()

;(function(){
  angular
    .module("todo")

    .config(function($httpProvider){
      $httpProvider.defaults.xsrfCookieName = "csrftoken"
      $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken"
    })

    .config(function($httpProvider, $injector){
      $httpProvider.interceptors.push(function($q, $injector){
        return {
          responseError: function(rejection){
            if (rejection.status !== 401){
              return rejection
            }
            var state = $injector.get("$state")
            state.go("login")
            return $q.reject(rejection)
          }
        }
      })
    })
})()

;(function(){
  angular
    .module("todo")

    .constant("API", {
      BASE: "/api/v1",
      AUTH: "/auth/",
      REGISTRATION:"/registration/",
      GROUP: "/group/",
      EXPORT: "/export/",
      USER: "/user/",
      ITEM: "/item/"
    })
})()

;(function(){
  angular
    .module("todo")

    .config(RouterConfig)

    RouterConfig.$injector = ["$stateProvider", "$urlRouterProvider"]

    function RouterConfig($stateProvider, $urlRouterProvider){
      $urlRouterProvider.otherwise("/groups")

      $stateProvider
        .state("groups", {
          abstract: true,
          templateUrl: "app/views/components/groups/groups.html",
          controller: "GroupController"
        })
        .state("groups.list", {
          url: "/groups",
          views: {
            "list": {
              templateUrl: "app/views/components/groups/group-list/group-list.html",
              controller: "GroupListController"
            },
            "panel": {
              templateUrl: "app/views/components/groups/group-panel/group-panel.html",
              controller: "GroupPanelController"
            }
          }
        })
        .state("edit-group", {
          url: "/edit_group/:id",
          templateUrl: "app/views/components/groups/group-edit/edit-group.html",
          controller: "EditGroupController",
          resolve: {
            groupId: function($stateParams, $state){
              return $stateParams.id
            }
          }
        })
    }
})()

;(function(){
  angular
    .module("todo")

    .service("ItemResource", ItemResource)

    ItemResource.$inject = ["API", "$resource"]

    function ItemResource(API, $resource){
      return $resource(API.BASE + API.ITEM + "/:id/", {id: "@id"}, {
        getItem: {
          method: "GET"
        },
        createItem: {
          method: "POST"
        },
        updateItem: {
          method: "PUT"
        },
        deleteItem: {
          method: "DELETE"
        }
      })
    }
})()

;(function(){
  angular
    .module("todo")

    .controller("LogoutController", LogoutController)

    LogoutController.$inject = ["$scope"]

    function LogoutController($scope){
      $scope.user = null
    }
})()

;(function(){
  angular
    .module("todo")

    .factory("UserResource", UserResource)

    UserResource.$inject = ["API", "$resource"]

    function UserResource(API, $resource){
      return $resource(API.BASE + API.USER + ":id/", {id: "@id"}, {
        getUsers: {
          method: "GET",
          params: {id: null}
        },
        getUser: {
          method: "GET"
        },
        createUser: {
          method: "POST"
        },
        updateUser: {
          method: "PUT"
        },
        deleteUser: {
          method: "DELETE"
        }
      })
    }
})()

;(function(){
  angular
    .module("todo")
    //inject session storage
    .service("GroupStorage", function(GroupResource){
      var self = this
      self.groups = {
        data: [],
        totalItems: 0
      }
      self.loadData = loadData
      
      var loaders = {
        "list": listLoader,
        "panel": panelLoader
      }

      function loadData(params){
        //instead of view use SessionUser.user.groupView 
        //var view = "list" 
        var view = "panel"
        loaders[view](params)
      }

      function listLoader(params){
        GroupResource.getGroups(params).$promise
        .then(function(response){
          self.groups.data = response.objects
          self.groups.totalItems = response.meta.total_count
        })  
      }

      function panelLoader(params){
        GroupResource.getGroups(params).$promise
        .then(function(response){
          _.forEach(response.objects, function(group){
            self.groups.data.push(group)
          })
        })  
      }
    })
})()

;(function(){
  angular
    .module("todo")

    .controller("GroupController", GroupController)

    GroupController.$inject = ["GroupStorage", "$scope"]

    function GroupController(GroupStorage, $scope){
      $scope.groupView = "list"
      $scope.groups = GroupStorage.groups
      $scope.params = {
        offset: 0
      }
      $scope.changeGroupView = changeGroupView
      function changeGroupView(){
        $scope.params.offset = 0
        GroupStorage.groups.data = []
      }
    }
})()

;(function(){
  angular
    .module("todo")

    .service("GroupResource", function($resource, API){
      return $resource(API.BASE + API.GROUP + ":id/", {id: "@id"}, {
        getGroups: {
          method: "GET",
          params: {id: null}
        },
        getGroup: {
          method: "GET"
        },
        createGroup: {
          method: "POST"
        },
        editGroup: {
          method: "PUT"
        },
        deleteGroup: {
          method: "DELETE"
        }
      })
    })
})()

;(function(){
  angular
    .module("downloaders")

    .factory("XlsDownloader", XlsDownloader)

    XlsDownloader.$inject = ["$http", "$window"]

    function XlsDownloader($http, $window){
      function download(url){
        $http({
          url: url,
          method: "GET",
          responseType: "arraybuffer"
        }).then(function(response){
          var type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          var blob = new Blob([response.data], {type: type})
          var objectUrl = URL.createObjectURL(blob)
          $window.open(objectUrl)
        })
      }
      return {
        download: download
      }
    }
})()

;(function(){
  angular
    .module("todo")

    .controller("EditGroupController", EditGroupController)

    EditGroupController.$inject = ["API", "groupId", "GroupResource", 
      "ItemResource", "$modal", "$scope", "$state", "XlsDownloader"]

    function EditGroupController(API, groupId, GroupResource, 
      ItemResource, $modal, $scope, $state, XlsDownloader){
      getGroup()

      $scope.newTask = {}
      $scope.addTask = addTask
      $scope.apply = apply
      $scope.deleteGroup = deleteGroup
      $scope.deleteTask = deleteTask
      $scope.editContributors = editContributors
      $scope.updateGroup = updateGroup
      $scope.xlsExport = xlsExport

      function addTask(){
        $scope.group.items.push($scope.newTask)
        $scope.newTask = {}
        updateGroup()
      }

      function apply(){
        updateGroup()
        $state.go("groups.list")
      }

      function deleteGroup(){
        $scope.group.is_deleted = true
        apply()
      }

      function deleteTask(item){
        ItemResource.deleteItem(item).$promise
        .then(function(response){
          getGroup()
        })
      }

      function editContributors(){
        var contributorsModal = $modal.open({
          templateUrl: "app/views/components/groups/edit-contributors/edit-contributors.html",
          controller: "EditContributorsController",
          windowClass: "edit-contributors-modal",
          resolve: {
            contributors: function(){
              return $scope.group.users
            }
          }
        })
        contributorsModal.result
        .then(function(contributors){
          $scope.group.users = contributors
          updateGroup()
        })
      }

      function getGroup(){
        GroupResource.getGroup({id: groupId}).$promise
        .then(function(response){
          $scope.group = response
        })    
      }

      function updateGroup(){
        GroupResource.editGroup($scope.group).$promise
        .then(function(response){
          getGroup()
        })
      }

      function xlsExport(){
        var url = API.BASE + API.EXPORT + "xls/" + groupId + "/"
        XlsDownloader.download(url)
      }
    }
})()

;(function(){
  angular
    .module("todo")

    .controller("EditContributorsController", EditContributorsController)

    EditContributorsController.$inject = ["contributors", 
      "$modalInstance", "$scope", "UserResource"]

    function EditContributorsController(contributors, $modalInstance, $scope, UserResource){
      $scope.contributors = contributors.slice()

      $scope.addContributor = addContributor
      $scope.apply = apply
      $scope.cancel = cancel
      $scope.deleteContributor = deleteContributor
      $scope.findUsers = findUsers

      function addContributor(contributor){
        if (!_.find($scope.contributors, {id: contributor.id})){
          $scope.contributors.push(contributor)
        }
      }

      function apply(){
        $modalInstance.close($scope.contributors)
      }

      function cancel(){
        $modalInstance.dismiss("cancel")
      }

      function deleteContributor(index){
        $scope.contributors.splice(index, 1)
      } 

      function findUsers(){
        var params = {
          limit: 0,
          username__icontains: $scope.username
        }
        UserResource.getUsers(params).$promise
        .then(function(response){
          $scope.users = response.objects
        })
      }
    } 
})()

;(function(){
  angular
    .module("todo")

    .controller("GroupListController", GroupListController)

    GroupListController.$inject = ["GroupStorage", "$scope"]

    function GroupListController(GroupStorage, $scope){
      $scope.params.limit = 10
      GroupStorage.loadData($scope.params)

      $scope.paginatorConfig = {
        currentPage: 1,
        changePage: function(){
          var currentPage = $scope.paginatorConfig.currentPage - 1
          $scope.params.offset = currentPage * $scope.params.limit
          GroupStorage.loadData($scope.params)
        }
      }
    }
})()

;(function(){
  angular
    .module("todo")

    .controller("GroupPanelController", GroupPanelController)

    GroupPanelController.$inject = ["GroupStorage", "$scope"]

    function GroupPanelController(GroupStorage, $scope){
      $scope.params.limit = 50

      $scope.loadData = loadData
      loadData()

      function loadData(){
        $scope.params.offset = $scope.groups.data.length
        GroupStorage.loadData($scope.params)
      }
    }
})()

;(function(){
  angular
    .module("nm-widgets")

    .controller("MasonryController", MasonryController)

    MasonryController.$inject = ["$scope"]

    function MasonryController($scope){
      return $scope.$watch(function(e){
        $scope.masonry.reloadItems()
        return $scope.masonry.layout()
      })
    }
})()

;(function(){
  angular
    .module("nm-widgets")

    .directive("masonry", function(){
      return{
        restrict: "A",
        link: link,
        controller: "MasonryController"
      }
    })

    function link($scope, element, attrs){
      var container = element[0]
      var options = ""
      return $scope.masonry = new Masonry(container, options)
    }
})()
