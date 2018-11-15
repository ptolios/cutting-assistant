document.addEventListener('DOMContentLoaded', function() {
  var sidenavs = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(sidenavs, {});
  var collapsibles = document.querySelectorAll('.collapsible');
  var instances = M.Sidenav.init(collapsibles, {});
});
M.AutoInit();
