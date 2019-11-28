// Modal Image Gallery

function changeText(th){
	var exist = th.value.lastIndexOf("\\");

	if (th.value != ""){
        if(exist == -1){
            document.getElementById('upload_file_button').innerText = th.value;
        }
        else{
            document.getElementById('upload_file_button').innerText = th.value.substring(exist + 1);
        }
        document.getElementById('confirm_upload').style.display = "";
	}

}

function chooseFile() {
document.getElementById('upload_file').click()
}

function UpladFile() {
      document.getElementById('confirm_upload').innerHTML = 'please waiting <i class="fa fa-spinner fa-spin"></i>'
  var fileObj = document.getElementById("upload_file").files[0];

  var url =  "http://localhost:1919" + "/upload_file";
  var form = new FormData();
  form.append("file", fileObj);
  xhr = new XMLHttpRequest();
  xhr.open("post", url, true);
  xhr.send(form);
  xhr.onreadystatechange=(e)=>{
            if (xhr.readyState === 4){
                var extra_json = xhr.responseText;
                <!--alert(extra_json)-->
                location.reload();
                };
            };
}

window.onload = function get_all_file() {
var Http = new XMLHttpRequest();
        var url = "/storage/get_file"
        Http.open("GET",url);
        Http.send();
        Http.onreadystatechange=(e)=>{
            if (Http.readyState === 4){
            var extra_json = Http.responseText;
            jsonObj = JSON.parse(extra_json);
            show_all_file(jsonObj)


            };
        }
}
function show_all_file(jsonObj) {
    var col = 0
    for (each_file_index in jsonObj){
        var new_file=document.createElement("img");
        new_file.setAttribute("src",jsonObj[each_file_index]["src"]);
        new_file.setAttribute("style","width:100%" );
        new_file.setAttribute("onclick","window.open(' "+jsonObj[each_file_index]["link"]+" ')" );
        col = col + 1
        if (col == 5){col=1}
        document.getElementById('grid'+col).appendChild(new_file);
//        if (each_file_index%4 == 0){
//        document.getElementById('grid4').appendChild(new_file);
//        }else if (each_file_index%3 == 0){
//        document.getElementById('grid3').appendChild(new_file);
//        }else if (each_file_index%2 == 0){
//        document.getElementById('grid2').appendChild(new_file);
//        }else{
//        document.getElementById('grid1').appendChild(new_file);
//        }



    }

}
