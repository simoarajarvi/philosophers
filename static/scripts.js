
function resetPage(){
    var expertCards = document.getElementById("expert-cards"); 
    if (expertCards != null) {
        expertCards.innerHTML = ''
    }

    document.getElementById("question_box").value = ''
}

function getCardHTML(card_list) {
html_txt = ''
for (var i = 0; i < card_list.length; i++) {
    pic = card_list[i][0]
    expert = card_list[i][1]
    desc = card_list[i][2]
    persSummary = card_list[i][3]
    starCount = card_list[i][4]
  
    persSummary = persSummary.replace(/'/g, "\\'");
    persSummary = persSummary.replace(/"/g, '');
    persSummary = persSummary.replace(/\n/g, "\\n");
    
    stars = ''
    for (var j = 0; j < starCount; j++) {
      stars += '&starf;'
    }
    
    html_txt += '<div class="row">'
    html_txt += '<div class="col expert-card">'
    html_txt += '<div class="container">'
    html_txt += '<div class="row">'
    html_txt += '<div class="col">'
    html_txt += '<img onclick="openModal([\''+expert+'\',\''+pic+'\',\''+persSummary+'\']);" width="50" height="50" align="left" style="border:2px solid gray; cursor: pointer;" src="/static/'+pic+'"  />' 
    html_txt += '<div class="expert-name">'
    html_txt += '<span class="expert-name" onclick="openModal([\''+expert+'\',\''+pic+'\',\''+persSummary+'\']);">'+expert+'</span>'  
    html_txt += '</div></div>'
    html_txt += '<div class="col stars-box">'+stars
    html_txt += '</div></div>'
    html_txt += '<div class="row score-explanations">'
    html_txt += '<div class="col">'
    html_txt += '<textarea readonly id="expert1"  name="expert1" rows="5" cols="120" style="border: none;outline:none;">'+desc+'</textarea>'
    html_txt += '</div></div></div></div></div>'
  }

  return html_txt
}


  function handleQuery() {

    var expertCards = document.getElementById("expert-cards"); 
    if (expertCards != null) {
        expertCards.innerHTML = ''
    }

    document.body.style.backgroundImage = "radial-gradient(circle farthest-corner at center, #3C4B57 0%, #1C262B 100%)"
    $('#loader').show(); 
    var query = document.getElementById("question_box").value;
    var numExperts = document.getElementById("num-experts").value;
    var expertCards = document.getElementById("expert-cards"); 
    var server_data = [
      {"query": query, "numExperts": numExperts}
    ];
    $.ajax({
      type: "POST",
      url: "/query",
      data: JSON.stringify(server_data),
      contentType: "application/json",
      dataType: 'json',
      success: function(result) {

      document.body.style.backgroundImage = "none"; 
      $('#loader').hide(); 
      expertCards.innerHTML = getCardHTML(result);

      }
    });
  }

  