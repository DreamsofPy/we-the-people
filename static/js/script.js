(function() {

}).call(this);

$("#contests").submit(function (evt) {
  evt.preventDefault();
  var data = $("#contests").serialize();
  var name = $(".candidate-name option:selected")[0].value;
  var issues = $(".issue:checked");
  var iss_arr = [];



  var url = "http://localhost:4567/candidate?name=" + name
  for(var i= 0 ; i< issues.length; i++) {
    iss_arr[i] = issues[i].value;
    url += '&issues=' + issues[i].value
  }
  $.ajax({
    type: "GET",
    url: url,
  }).done(function (data) {
    $("#contests").hide();
    console.log(data);
    var news = data.news
    var newsList = '<dl>'
    for(var i = 0; i < news.length; i++) {
      newsList += '<dd> '
    }
  });
});

$("#elections").change(function () {
  var office = $("#elections option:selected")[0].value;
  var eid = $("#eid")[0].value;
  var address = $("#address")[0].value;
  // http://localhost:4567/api/candidates?address=NJ+07302&election_id=4000&office_name=U.S.+Senate
  if(office !== "default") {
    var url = "http://localhost:4567/api/candidates?address=" + encodeURIComponent(address) + "&election_id="  + encodeURIComponent(eid) + "&office_name=" + encodeURIComponent(office);
    $.ajax({
      url: url,
    }).done(function (data) {
      var candidates = data.candidates;
      $("#candidates-info").remove();
      $(".candidates").append("<div id='candidates-info'>");
      var candSelect = "<select class='candidate-name'>";

      for(var i = 0; i < candidates.length; i++) {
        var candidate = candidates[i]
        var candidateDiv = "<option name=" + candidate.name +" id=" + i + "value=" + candidate.name + '>' + candidate.name + "</option>"
        candSelect = candSelect + candidateDiv;
      }
      candSelect = candSelect + '<select>'
      $("#candidates-info").append(candSelect);
    });
  }
})
