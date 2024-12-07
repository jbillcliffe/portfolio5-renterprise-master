// Function to update height and width
function updateSize() {
    /* <div id="rest-of-sidebar" class="nav nav-list collapse"> */
    if (window.innerWidth >= 576) {
        {/* <div id="rest-of-sidebar" class="nav nav-list collapse"> */}
        let sidebar = document.getElementById('rest-of-sidebar');
        sidebar.className = "nav nav-list collapse";
    }
}

// Add event listener for window resize
window.addEventListener('resize', updateSize);