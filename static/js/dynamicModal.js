
function loadDynamicModal(fileName) {
    const xhttp = new XMLHttpRequest();
    let xmlUrl = window.location.origin+"/static/xml/"+fileName;
    xhttp.onload = function() {displayXMLResult(this);}
    xhttp.open("GET", xmlUrl);
    xhttp.send();
}
  
function displayXMLResult(xml) {
    const xmlDoc = xml.responseXML;
    // Gets HTMLCollections
    const modalTitle = xmlDoc.getElementsByTagName("modaltitle");
    const modalBody = xmlDoc.getElementsByTagName("modalbody");
    const modalFooter = xmlDoc.getElementsByTagName("modalfooter");
    // The first node of each object will always be the data.
    // there is only one node in each opject called
    document.getElementById("id-modal-title").innerHTML = modalTitle.item(0).innerHTML;
    document.getElementById("id-modal-body").innerHTML = modalBody.item(0).innerHTML;
    document.getElementById("id-modal-footer").innerHTML = modalFooter.item(0).innerHTML;
}

// Clear the modal data each time to prevent duplications.
$("#id-renterprise-modal").on('hide.bs.modal', function(){
    document.getElementById("id-modal-title").innerHTML = "";
    document.getElementById("id-modal-body").innerHTML = "";
    document.getElementById("id-modal-footer").innerHTML = "";
  });