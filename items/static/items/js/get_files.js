document.getElementById('edit-type-image-select').addEventListener('change', function(e) {
    if (e.target.files[0]) {
      console.log('You selected ' + e.target.files[0].name);
    }
  });