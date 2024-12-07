document.getElementById('type-image-select').addEventListener('change', function(e) {
    // Update the image field for display
    // https://stackoverflow.com/questions/17138244/how-to-display-selected-image-without-sending-data-to-server

    // Create a new file reader for the file selected
    let fileReader = new FileReader();
    
    // Identify the <img> to be updated by it's id
    let imageBox;
    if (document.getElementById('type-image') != null) {
        imageBox = document.getElementById('type-image');
    } else {
        imageBox = document.getElementById('item-image-id');
    }

	// Identify the <input> which shows the filename/location
	let imageURLField = document.getElementById('image-input-id');

    // When the file load is complete run the function which will change the
    // src to be of the result of this file selection.
    fileReader.onload = function() {
      imageBox.src = this.result;
	  imageURLField.className = "rounded-0 textinput form-control text-danger"
      imageURLToShow = (e.target.files[0].name).replace('/media\//g', "")
	  imageURLField.value = `${imageURLToShow}	** Not Uploaded! **`;
    }

    console.log(fileReader);
    console.log(imageBox);
    console.log(fileReader);

    // This tells the file reader how to read the file loaded. readAsDataURL turns the file
    // into a base64 encoded string which is the required way for an image (Blob data)
    fileReader.readAsDataURL(e.target.files[0]);
});

