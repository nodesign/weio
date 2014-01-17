require.config({
    baseUrl: '../../../../libs/'
});

// load libs in exact order
// code from 
// http://stackoverflow.com/questions/11581611/load-files-in-specific-order-with-requirejs

var requireQueue = function(modules) {
  function load(queue, results) {
    if (queue.length) {
      require([queue.shift()], function(result) {
        results.push(result);
        load(queue, results);
      });
    }
  }
  load(modules, []);
};

requireQueue([
  'jquery/jquery-2.0.2.min',
  'sockJS/sockjs-0.3.min',
  'weio/weioApi'
  //'chartJS/Chart.min',
  //'bootstrap/js/bootstrap.min',
  //'weio/wifi',
  //'weio/dashboard',
  //'weio/updater'
]);